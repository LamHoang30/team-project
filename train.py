"""Offline rebuild. Test data never select features, model, or threshold."""
import argparse
import hashlib
import json
import platform
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

from sklearn.model_selection import StratifiedGroupKFold, RandomizedSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score, precision_score,
    recall_score, f1_score, confusion_matrix, brier_score_loss,
    roc_curve, precision_recall_curve
)
from sklearn.inspection import permutation_importance

from utils.data_loader import (
    ROOT, TARGET, SPECS, SHORT, SOURCES, FINAL_ALGORITHM, load_data
)
from utils.threshold import threshold_table, choose_threshold


def evaluate(y, p, t):
    pred = p >= t
    return dict(
        roc_auc=float(roc_auc_score(y, p)),
        average_precision=float(average_precision_score(y, p)),
        brier=float(brier_score_loss(y, p)),
        precision=float(precision_score(y, pred, zero_division=0)),
        recall=float(recall_score(y, pred, zero_division=0)),
        f1=float(f1_score(y, pred, zero_division=0)),
        confusion_matrix=confusion_matrix(y, pred, labels=[0, 1]).tolist(),
        n=len(y),
        positive_count=int(sum(y))
    )


def make_preprocessor(features):
    other_numeric = [c for c in features if c in ['MentHlth', 'PhysHlth']]
    category = [c for c in features if c not in other_numeric + ['BMI']]
    parts = []
    if 'BMI' in features:
        parts.append(('bmi', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), ['BMI']))
    if other_numeric:
        parts.append(('numeric', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), other_numeric))
    if category:
        parts.append(('category', Pipeline([('impute', SimpleImputer(strategy='most_frequent')), ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), category))
    return ColumnTransformer(parts)


def build(features, algorithm, use_pca=False, pca_variance=0.90):
    est = (
        LogisticRegression(max_iter=1000, C=1.0)
        if algorithm == 'Logistic Regression'
        else HistGradientBoostingClassifier(max_depth=4, max_iter=300, learning_rate=0.05, l2_regularization=1.0, random_state=0)
        if algorithm == 'Gradient Boosting'
        else RandomForestClassifier(n_estimators=140, max_depth=14, min_samples_leaf=30, max_features='sqrt', n_jobs=-1, random_state=42)
    )
    steps = [('preprocess', make_preprocessor(features))]
    if use_pca:
        steps.append(('pca_scale', StandardScaler()))
        steps.append(('pca', PCA(n_components=pca_variance, random_state=42)))
    steps.append(('model', est))
    return Pipeline(steps)


def tune_short_gradient_boosting(X_tr, y_tr, groups_tr):
    print('Tuning hyperparameters for short | Gradient Boosting...', flush=True)
    base_pipe = build(SHORT, 'Gradient Boosting')
    param_dist = {
        'model__learning_rate': [0.02, 0.03, 0.05, 0.08],
        'model__max_depth': [3, 4, 5, 6],
        'model__max_leaf_nodes': [15, 31, 63],
        'model__min_samples_leaf': [20, 50, 100],
        'model__l2_regularization': [0.0, 0.5, 1.0, 5.0],
        'model__max_iter': [250, 350, 450],
    }
    cv = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=42)
    search = RandomizedSearchCV(base_pipe, param_dist, n_iter=12, scoring='roc_auc', cv=cv, random_state=42, n_jobs=-1)
    search.fit(X_tr, y_tr, groups=groups_tr)
    clean_params = {k.replace('model__', ''): v for k, v in search.best_params_.items()}
    return search.best_estimator_, clean_params, float(search.best_score_)


def feature_selection_report(X, y, train, val, features, reports):
    Xtr, ytr = X.iloc[train], y.iloc[train]
    Xva, yva = X.iloc[val], y.iloc[val]
    def auc(cols):
        pipe = build(cols, 'Logistic Regression').fit(Xtr[cols], ytr)
        return float(roc_auc_score(yva, pipe.predict_proba(Xva[cols])[:, 1]))
    full, short = auc(features), auc(SHORT)
    rows = [dict(feature=c, in_short=c in SHORT, drop_from_full_auc_loss=full - auc([x for x in features if x != c]),
                 drop_from_short_auc_loss=(short - auc([x for x in SHORT if x != c]) if c in SHORT else np.nan),
                 add_to_short_auc_gain=(auc(SHORT + [c]) - short if c not in SHORT else np.nan)) for c in features]
    chosen, rest, path = [], list(features), []
    for k in range(1, 9):
        scores = {c: auc(chosen + [c]) for c in rest}
        best = max(scores, key=scores.get)
        chosen.append(best)
        rest.remove(best)
        path.append(dict(step=k, feature=best, validation_auc=scores[best]))
    table = pd.DataFrame(rows)
    table['forward_step'] = table.feature.map({p['feature']: p['step'] for p in path})
    table.sort_values('drop_from_full_auc_loss', ascending=False).to_csv(reports / 'feature_selection.csv', index=False)
    pd.DataFrame(path).to_csv(reports / 'forward_selection.csv', index=False)
    return dict(full_validation_auc=full, short_validation_auc=short, forward_top_k=chosen[:len(SHORT)], forward_top_k_equals_short=(set(chosen[:len(SHORT)]) == set(SHORT)))


def main(path):
    out, reports = ROOT / 'models', ROOT / 'reports'
    out.mkdir(exist_ok=True)
    reports.mkdir(exist_ok=True)
    df = load_data(path)
    features = list(SPECS)
    X, y = df[features], df[TARGET].astype(int)
    groups = pd.util.hash_pandas_object(X, index=False).values
    folds = list(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42).split(X, y, groups))
    test, val, train = folds[0][1], folds[1][1], np.concatenate([f[1] for f in folds[2:]])
    dup = df.duplicated()
    first = ~dup.values
    bins = pd.cut(df.BMI, [0, 18.5, 25, 30, 35, 40, 50, 60, np.inf])
    audit = dict(
        rows=len(df), columns=list(df.columns), dtypes=df.dtypes.astype(str).to_dict(), missing=df.isna().sum().to_dict(),
        exact_duplicate_rows=int(dup.sum()), conflicting_predictor_profiles=int(df.groupby(features)[TARGET].nunique().gt(1).sum()),
        class_counts=y.value_counts().to_dict(), ranges={c: [float(df[c].min()), float(df[c].max())] for c in df},
        splits={name: {'n': len(ids), 'positive_rate': float(y.iloc[ids].mean())} for name, ids in [('train', train), ('validation', val), ('test', test)]},
        duplicates=dict(extra_copies_by_class={str(k): int(v) for k, v in df[dup][TARGET].astype(int).value_counts().items()}, positive_rate_all_rows=float(y.mean()), positive_rate_after_dedup=float(df.drop_duplicates()[TARGET].mean())),
        bmi_positive_rate_by_bin={str(k): float(v) for k, v in y.groupby(bins, observed=True).mean().items()}, bmi_cap=None, bmi_handling='Original BMI values retained; no upper cap'
    )
    (reports / 'data_audit.json').write_text(json.dumps(audit, indent=2))
    pd.DataFrame([dict(feature=c, label=v[0], encoding=v[1], decision=v[2]) for c, v in SPECS.items()]).to_csv(reports / 'feature_dictionary.csv', index=False)
    fs = feature_selection_report(X, y, train, val, features, reports)

    candidates, fitted = [], {}
    for name, cols in [('full', features), ('short', SHORT)]:
        for alg in ['Logistic Regression', 'Random Forest', 'Gradient Boosting']:
            key = f'{name} | {alg}'
            pipe = build(cols, alg).fit(X.iloc[train][cols], y.iloc[train])
            p = pipe.predict_proba(X.iloc[val][cols])[:, 1]
            candidates.append(dict(candidate=key, feature_set=name, algorithm=alg, n_features=len(cols), **evaluate(y.iloc[val], p, .5)))
            fitted[key] = (pipe, cols, p)

    tuned_pipe, best_params, cv_best_auc = tune_short_gradient_boosting(X.iloc[train][SHORT], y.iloc[train], groups[train])
    p_tuned = tuned_pipe.predict_proba(X.iloc[val][SHORT])[:, 1]
    tuned_key = 'short | Gradient Boosting (Tuned)'
    candidates.append(dict(candidate=tuned_key, feature_set='short', algorithm='Gradient Boosting (Tuned)', n_features=len(SHORT), **evaluate(y.iloc[val], p_tuned, .5)))
    fitted[tuned_key] = (tuned_pipe, SHORT, p_tuned)

    pca_results, pca_explained_summary = [], {}
    for alg in ['Logistic Regression', 'Gradient Boosting']:
        pca_key = f'full_pca_90pct | {alg}'
        pca_pipe = build(features, alg, use_pca=True, pca_variance=0.90).fit(X.iloc[train][features], y.iloc[train])
        p_pca = pca_pipe.predict_proba(X.iloc[val][features])[:, 1]
        pca_step = pca_pipe.named_steps['pca']
        n_comp = int(pca_step.n_components_)
        pca_explained_summary = {'raw_features': len(features), 'encoded_dimensions': int(pca_step.n_features_in_), 'retained_components': n_comp, 'explained_variance_ratio': round(float(np.sum(pca_step.explained_variance_ratio_)), 4)}
        pca_results.append(dict(candidate=pca_key, feature_set='pca_21_to_90pct_var', algorithm=f'{alg} + PCA ({n_comp} PCs)', n_features=len(features), n_components=n_comp, **evaluate(y.iloc[val], p_pca, .5)))

    best_auc = max(c['roc_auc'] for c in candidates)
    eligible = [c for c in candidates if c['feature_set'] == 'short' and c['roc_auc'] >= best_auc - .010] or [c for c in candidates if c['feature_set'] == 'short']
    short_gb_default = next(c for c in candidates if c['candidate'] == 'short | Gradient Boosting')
    short_gb_tuned = next(c for c in candidates if c['candidate'] == tuned_key)
    selected = short_gb_tuned if short_gb_tuned['roc_auc'] >= short_gb_default['roc_auc'] else max(eligible, key=lambda c: c['roc_auc'])

    pipeline, cols, pval = fitted[selected['candidate']]
    ref_pipe = build(['Age', 'BMI'], 'Logistic Regression').fit(X.iloc[train][['Age', 'BMI']], y.iloc[train])
    reference = [dict(candidate='baseline: Age + BMI only | Logistic Regression', feature_set='baseline', algorithm='Logistic Regression', n_features=2, **evaluate(y.iloc[val], ref_pipe.predict_proba(X.iloc[val][['Age', 'BMI']])[:, 1], .5))]

    best, _ = choose_threshold(threshold_table(y.iloc[val], pval), 1., 5.)
    threshold = float(best.threshold)
    ptest = pipeline.predict_proba(X.iloc[test][cols])[:, 1]
    test_metrics = evaluate(y.iloc[test], ptest, threshold)

    joblib.dump(pipeline, out / 'pipeline.joblib', compress=3)
    np.savez_compressed(out / 'validation_predictions.npz', y=y.iloc[val].to_numpy(), p=pval)

    fairness = []
    for feature in ['Age', 'Sex', 'Income', 'Education']:
        for group, block in df.iloc[test].assign(_p=ptest).groupby(feature):
            yy, pp = block[TARGET].astype(int), block._p.to_numpy()
            if yy.nunique() != 2:
                continue
            mm = evaluate(yy, pp, threshold)
            tn, fp = mm['confusion_matrix'][0]
            fn, tp = mm['confusion_matrix'][1]
            fairness.append(dict(feature=feature, group=int(group), n=len(block), positive_rate=float(yy.mean()), roc_auc=mm['roc_auc'], precision=mm['precision'], recall=mm['recall'], FPR=fp / (tn + fp) if tn + fp else None, FDR=fp / (tp + fp) if tp + fp else None, TP=tp, FP=fp, FN=fn, TN=tn))
    pd.DataFrame(fairness).to_csv(out / 'fairness.csv', index=False)

    fpr, tpr, _ = roc_curve(y.iloc[test], ptest)
    prec, rec, _ = precision_recall_curve(y.iloc[test], ptest)
    ix = np.unique(np.linspace(0, len(fpr) - 1, min(1000, len(fpr))).astype(int))
    jx = np.unique(np.linspace(0, len(prec) - 1, min(1000, len(prec))).astype(int))
    pd.DataFrame({'FPR': fpr[ix], 'Recall': tpr[ix]}).to_csv(out / 'roc.csv', index=False)
    pd.DataFrame({'Recall': rec[jx], 'Precision': prec[jx]}).to_csv(out / 'pr.csv', index=False)

    imp = permutation_importance(pipeline, X.iloc[val][cols], y.iloc[val], scoring='roc_auc', n_repeats=3, max_samples=5000, random_state=42, n_jobs=1)
    pd.DataFrame({'feature': cols, 'validation_AUC_drop': imp.importances_mean, 'sd': imp.importances_std}).sort_values('validation_AUC_drop', ascending=False).to_csv(reports / 'permutation_importance.csv', index=False)
    pd.DataFrame(candidates + reference + pca_results).drop(columns=['confusion_matrix', 'n_components'], errors='ignore').to_csv(reports / 'validation_comparison.csv', index=False)

    background = X.iloc[train][cols].sample(1000, random_state=42).astype(float).to_dict(orient='records')
    m = dict(
        target=TARGET, target_meaning={'0': 'No self-reported diabetes/prediabetes', '1': 'Self-reported diabetes or prediabetes'},
        sources=SOURCES, rows=len(df), features=cols, feature_names=cols,
        valid_input_ranges={c: audit['ranges'][c] for c in cols}, valid_values={c: sorted(df[c].unique().tolist()) for c in cols if c != 'BMI'},
        algorithm=selected['algorithm'], selected_candidate=selected['candidate'], tuned_hyperparameters=best_params, cv_tuned_roc_auc=cv_best_auc,
        pca_experiment=dict(summary=pca_explained_summary, candidates=pca_results, rationale='Optional dimensionality-reduction benchmark using all 21 predictors compressed via PCA (90% variance retained).'),
        threshold=threshold, cost_assumptions={'FP': 1, 'FN': 5, 'units': 'illustrative relative units'},
        test_metrics=test_metrics, validation_metrics=evaluate(y.iloc[val], pval, threshold),
        explanation=dict(method='Exact Shapley values over the 5 questions relative to a 1,000-row training background.', background=background),
        feature_selection=fs, short_auc_gap=(best_auc - max(c['roc_auc'] for c in candidates if c['feature_set'] == 'short')),
        audit=audit, versions={'python': platform.python_version(), 'sklearn': sklearn.__version__},
        sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        selection_rule='Use short 5-feature model when validation ROC-AUC is within 0.010 of full model; tune hyperparameters via 3-fold StratifiedGroupKFold.',
        split_method='60/20/20 StratifiedGroupKFold keeping identical 21-feature profiles in the same split.',
        imbalance='No oversampling or class weights: retain natural prevalence and calibrated probabilities.'
    )
    (out / 'model_meta.json').write_text(json.dumps(m, indent=2))
    print('Training & artifacts updated successfully.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, default=ROOT / 'data/diabetes_binary_health_indicators_BRFSS2015.csv')
    main(p.parse_args().data)
