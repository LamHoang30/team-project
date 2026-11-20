import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.calibration import calibration_curve

from utils.data_loader import ROOT, meta, SPECS, AGES
from utils.ui import DISCLAIMER, html, simulator, GLUCOMETER_SVG

m = meta()
metrics = m["test_metrics"]
cm_raw = metrics["confusion_matrix"]
tn, fp = int(cm_raw[0][0]), int(cm_raw[0][1])
fn, tp = int(cm_raw[1][0]), int(cm_raw[1][1])

accuracy = (tn + tp) / max(metrics["n"], 1)
prec_0 = tn / (tn + fn) if (tn + fn) else 0.0
rec_0 = tn / (tn + fp) if (tn + fp) else 0.0
f1_0 = 2 * prec_0 * rec_0 / (prec_0 + rec_0) if (prec_0 + rec_0) else 0.0
prec_1 = float(metrics["precision"])
rec_1 = float(metrics["recall"])
f1_1 = float(metrics["f1"])


def svg(path, size=18, color="#007B8A"):
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'style="display:block;flex:0 0 {size}px">{path}</svg>'
    )


IC_DB = svg('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3"/>', 20)
IC_CPU = svg('<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>', 20)
IC_CHART = svg('<path d="M3 3v18h18"/><rect x="7" y="10" width="3" height="7" rx="1"/><rect x="12" y="6" width="3" height="11" rx="1"/><rect x="17" y="13" width="3" height="4" rx="1"/>', 19)
IC_TARGET = svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>', 16)
IC_SCALE = svg('<path d="M12 3v18M5 7h14"/><path d="M5 7l-2.5 6a3 3 0 0 0 5 0L5 7zM19 7l-2.5 6a3 3 0 0 0 5 0L19 7z"/><path d="M8 21h8"/>', 16)
IC_REFRESH = svg('<path d="M21 12a9 9 0 0 0-15.5-6.3L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 15.5 6.3L21 16"/><path d="M21 21v-5h-5"/>', 16)
IC_TREND = svg('<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>', 16)
IC_BULB = svg('<path d="M9 18h6M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>', 19)
IC_INFO = svg('<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>', 17, "#1F3A5F")

st.markdown("""
<style>
.st-key-about_hero{
    background:linear-gradient(120deg,#FFFFFF 0%,#EDF8FA 55%,#CBEAF0 100%);
    border:1px solid #DFEBE3;
    border-radius:24px;
    padding:1.8rem 2rem;
}
.st-key-about_card{
    background:#FFFFFF;
    border:1px solid #DFEBE3;
    border-radius:20px;
    padding:1.4rem 1.6rem;
    box-shadow:0 4px 18px rgba(27,94,67,.04);
}
.pill-ai{
    display:inline-block;
    background:#007B8A;
    color:#FFFFFF;
    font-size:.72rem;
    font-weight:700;
    letter-spacing:.6px;
    padding:4px 12px;
    border-radius:999px;
    margin-bottom:.6rem;
}
.about-h1{font-size:2.3rem;font-weight:800;color:#11241B;letter-spacing:-1px;line-height:1.1;margin:0 0 .5rem}
.about-sub{font-size:1.05rem;font-weight:700;color:#11241B;margin-bottom:.45rem}
.about-p{font-size:.93rem;color:#475E52;line-height:1.55;margin-bottom:1rem;max-width:34rem}
.mini-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mini-card{
    display:flex;gap:12px;align-items:center;
    background:rgba(255,255,255,.88);
    border:1px solid #D7E8DD;
    border-radius:14px;
    padding:12px 14px;
}
.mini-card .mic{
    width:40px;height:40px;border-radius:11px;background:#DDF0E4;
    display:flex;align-items:center;justify-content:center;flex:0 0 40px
}
.mini-card .mt{font-weight:700;font-size:.9rem;color:#11241B;line-height:1.2}
.mini-card .md{font-size:.79rem;color:#62786D;margin-top:2px;line-height:1.35}
.sec-hdr{display:flex;align-items:center;gap:10px;font-size:1.1rem;font-weight:800;color:#11241B;margin-bottom:.3rem}
.sec-sub{font-size:.86rem;color:#62786D;margin-bottom:1rem}
.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:1rem}
.kpi-box{background:#F7FBF8;border:1px solid #E3EFE7;border-radius:14px;padding:14px 12px;text-align:center}
.kpi-top{display:flex;align-items:center;justify-content:center;gap:6px;font-size:.84rem;color:#52685B;font-weight:600}
.kpi-val{font-size:1.65rem;font-weight:800;color:#11241B;margin-top:4px;line-height:1.1}
.crep{width:100%;border-collapse:collapse;font-size:.86rem;margin-top:.35rem}
.crep th{color:#52685B;font-weight:700;text-align:center;padding:10px 8px;border-bottom:1px solid #DCE7E0;background:#F7FBF8}
.crep th:first-child{text-align:left}
.crep td{padding:10px 8px;text-align:center;color:#11241B;border-bottom:1px solid #EFF5F1}
.crep td:first-child{text-align:left;font-weight:700}
@media(max-width:768px){
    .mini-cards,.kpi-grid{grid-template-columns:1fr 1fr}
    .about-h1{font-size:1.85rem}
}
</style>
""", unsafe_allow_html=True)

with st.container(key="about_hero"):
    h_left, h_right = st.columns([6.2, 4.2], vertical_alignment="center", gap="large")
    with h_left:
        html(f"""
        <div class="pill-ai">FACULTY & TECHNICAL REVIEW</div>
        <div class="about-h1">Behind GlucoGuide</div>
        <div class="about-sub">ECON 495 — Data Mining with Applications to Health Care</div>
        <div class="about-p">
            Trained on {m['rows']:,} US CDC BRFSS 2015 survey records using leak-free 5-fold StratifiedGroupKFold
            validation, hyperparameter tuning, and exact Shapley explanations.
        </div>
        <div class="mini-cards">
            <div class="mini-card">
                <div class="mic">{IC_DB}</div>
                <div>
                    <div class="mt">Training Data</div>
                    <div class="md">BRFSS 2015 ({m['rows']:,} records)</div>
                </div>
            </div>
            <div class="mini-card">
                <div class="mic">{IC_CPU}</div>
                <div>
                    <div class="mt">Selected Model</div>
                    <div class="md">{m['algorithm']} (5 features)</div>
                </div>
            </div>
        </div>
        """)
    with h_right:
        html(f'<div style="text-align:center">{GLUCOMETER_SVG}</div>')

st.write("")

tabs = st.tabs([
    "Performance & Factors",
    "Calibration & Risk Deciles",
    "Threshold & Costs",
    "Fairness Audit",
    "Data, Tuning & PCA",
    "Full Model Card",
])

with tabs[0]:
    with st.container(key="about_card"):
        html(f"""
        <div class="sec-hdr">{IC_CHART}<span>Held-Out Test Set Performance</span></div>
        <div class="sec-sub">
            Evaluated on {metrics['n']:,} unseen test records at default threshold <b>{m['threshold']:.4f}</b>.
        </div>
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="kpi-top">{IC_TARGET}<span>Accuracy</span></div>
                <div class="kpi-val">{accuracy:.3f}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-top">{IC_SCALE}<span>Precision</span></div>
                <div class="kpi-val">{prec_1:.3f}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-top">{IC_REFRESH}<span>Recall</span></div>
                <div class="kpi-val">{rec_1:.3f}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-top">{IC_TREND}<span>ROC-AUC</span></div>
                <div class="kpi-val">{metrics['roc_auc']:.3f}</div>
            </div>
        </div>
        """)

        c1, c2, c3 = st.columns(3)
        c1.metric("F1-score", f"{f1_1:.3f}")
        c2.metric("Average precision", f"{metrics['average_precision']:.3f}")
        c3.metric("Brier score (lower is better)", f"{metrics['brier']:.3f}")

        st.write("")
        col_l, col_r = st.columns(2, gap="large")
        with col_l:
            st.markdown("**ROC Curve**")
            roc = pd.read_csv(ROOT / "models/roc.csv")
            fig_roc = px.line(roc, x="FPR", y="Recall", labels={"FPR": "False positive rate", "Recall": "True positive rate"})
            fig_roc.update_traces(line=dict(color="#007B8A", width=2.5))
            fig_roc.add_shape(type="line", x0=0, y0=0, x1=1, y1=1, line=dict(color="#9AA59D", dash="dot", width=1.2))
            fig_roc.update_layout(template="simple_white", height=310, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_roc, use_container_width=True)

        with col_r:
            st.markdown("**Test Confusion Matrix**")
            cm_df = pd.DataFrame([[tn, fp], [fn, tp]], index=["Actual 0", "Actual 1"], columns=["Not flagged", "Flagged"])
            fig_cm = px.imshow(cm_df, text_auto=True, color_continuous_scale=["#EEF6F0", "#C4E0CD", "#6BA583", "#007B8A"], aspect="auto")
            fig_cm.update_layout(template="simple_white", height=310, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_cm, use_container_width=True)

        st.write("")
        col_b1, col_b2 = st.columns(2, gap="large")
        with col_b1:
            st.markdown("**Classification Report (Test Set)**")
            html(f"""
            <table class="crep">
                <thead><tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Support</th></tr></thead>
                <tbody>
                    <tr><td>No diabetes label (0)</td><td>{prec_0:.3f}</td><td>{rec_0:.3f}</td><td>{f1_0:.3f}</td><td>{tn + fp:,}</td></tr>
                    <tr><td>Diabetes / prediabetes (1)</td><td>{prec_1:.3f}</td><td>{rec_1:.3f}</td><td>{f1_1:.3f}</td><td>{fn + tp:,}</td></tr>
                </tbody>
            </table>
            """)
        with col_b2:
            html(f'<div class="sec-hdr">{IC_BULB}<span>Permutation Importance (Validation ROC-AUC Drop)</span></div>')
            imp = pd.read_csv(ROOT / "reports/permutation_importance.csv")
            sub_imp = imp.sort_values("validation_AUC_drop", ascending=True)
            fig_imp = px.bar(sub_imp, x="validation_AUC_drop", y="feature", orientation="h", text=sub_imp["validation_AUC_drop"].map(lambda v: f"{v:.4f}"))
            fig_imp.update_traces(marker_color="#0B3C6D", textposition="outside", cliponaxis=False)
            fig_imp.update_layout(template="simple_white", height=250, margin=dict(l=10, r=45, t=10, b=20))
            st.plotly_chart(fig_imp, use_container_width=True)

        st.divider()
        st.markdown("**Validation Model Comparison (Baseline, Full, Short, Tuned & PCA)**")
        comparison = pd.read_csv(ROOT / "reports/validation_comparison.csv")
        st.dataframe(comparison, hide_index=True, use_container_width=True)

with tabs[1]:
    st.subheader("Probability Calibration & Risk Stratification (Decile Lift)")
    st.write(
        "Because GlucoGuide retains raw class prevalence without SMOTE/oversampling, predicted probabilities "
        "reflect true empirical risk. Below is the validation reliability curve and risk stratification by decile."
    )
    with np.load(ROOT / "models/validation_predictions.npz") as saved:
        yv, pv = saved["y"], saved["p"]

    prob_true, prob_pred = calibration_curve(yv, pv, n_bins=10, strategy="quantile")
    cal_df = pd.DataFrame({
        "Mean Predicted Probability": prob_pred,
        "Observed Positive Rate": prob_true,
    })

    c_cal1, c_cal2 = st.columns([1.2, 1.0], gap="large")
    with c_cal1:
        fig_cal = px.line(
            cal_df,
            x="Mean Predicted Probability",
            y="Observed Positive Rate",
            markers=True,
            title="Reliability Diagram (10 Quantile Bins)",
        )
        fig_cal.update_traces(line=dict(color="#007B8A", width=2.8), marker=dict(size=8))
        fig_cal.add_shape(type="line", x0=0, y0=0, x1=0.6, y1=0.6, line=dict(color="#9AA59D", dash="dot"))
        fig_cal.update_layout(template="simple_white", height=360)
        st.plotly_chart(fig_cal, use_container_width=True)

    with c_cal2:
        df_dec = pd.DataFrame({"y": yv, "p": pv})
        df_dec["Decile"] = pd.qcut(df_dec["p"], q=10, labels=[f"D{i}" for i in range(1, 11)])
        lift_tbl = df_dec.groupby("Decile", observed=True).agg(
            Count=("y", "count"),
            Pred_Mean=("p", lambda s: f"{s.mean():.1%}"),
            Actual_Rate=("y", lambda s: f"{s.mean():.1%}"),
            Lift=("y", lambda s: round(s.mean() / yv.mean(), 2)),
        ).reset_index()
        st.markdown("**Decile Risk Stratification Table**")
        st.dataframe(lift_tbl, hide_index=True, use_container_width=True)
        st.caption(f"Base prevalence in validation set: {yv.mean():.2%}. Top decile (D10) captures {lift_tbl.iloc[-1]['Lift']}× baseline prevalence.")

with tabs[2]:
    simulator(m, "about")

with tabs[3]:
    st.subheader("Group-level performance audit")
    fair = pd.read_csv(ROOT / "models/fairness.csv")
    group = st.selectbox("Audit dimension", ["Age", "Sex", "Income", "Education"])
    sub = fair[fair.feature == group].copy()

    def group_label(v):
        if group == "Age":
            return AGES[int(v) - 1]
        if group == "Sex":
            return {0: "Female (source code)", 1: "Male (source code)"}.get(int(v), str(v))
        return str(int(v))

    sub["Group label"] = sub.group.map(group_label)
    st.caption(SPECS[group][1])
    st.dataframe(sub, hide_index=True, use_container_width=True)

    fig_fair = px.bar(
        sub,
        x="Group label",
        y=["recall", "FPR"],
        barmode="group",
        range_y=[0, 1],
        title="Recall and false-positive rate by group",
        color_discrete_map={"recall": "#007B8A", "FPR": "#D97706"},
    )
    fig_fair.update_layout(template="simple_white", height=380, legend_title_text="")
    st.plotly_chart(fig_fair, use_container_width=True)

with tabs[4]:
    st.subheader("Data preparation, Hyperparameter Tuning & Optional PCA")
    st.markdown("**Data splitting**")
    st.write(m["split_method"])
    st.markdown("**Class imbalance**")
    st.write(m["imbalance"])
    st.markdown("**Model selection**")
    st.write(m["selection_rule"])

    st.divider()
    st.markdown("**Hyperparameter Tuning (Short Gradient Boosting)**")
    if "tuned_hyperparameters" in m:
        st.write(f"3-fold StratifiedGroupKFold best CV ROC-AUC: **{m.get('cv_tuned_roc_auc', 0):.4f}**")
        st.json(m["tuned_hyperparameters"])

    st.divider()
    st.markdown("**Optional Experiment: PCA on All 21 Predictors (90% Variance Retained)**")
    if "pca_experiment" in m:
        pca_info = m["pca_experiment"]
        st.info(pca_info.get("rationale", ""))
        st.json(pca_info.get("summary", {}))
        pca_cands = pca_info.get("candidates", [])
        if pca_cands:
            st.dataframe(pd.DataFrame(pca_cands).drop(columns=["confusion_matrix"], errors="ignore"), hide_index=True, use_container_width=True)

    st.divider()
    st.markdown("**Feature dictionary**")
    st.dataframe(pd.read_csv(ROOT / "reports/feature_dictionary.csv"), hide_index=True, use_container_width=True)

with tabs[5]:
    st.subheader("GlucoGuide Model Card")
    c1, c2, c3 = st.columns(3)
    c1.metric("Algorithm", m["algorithm"])
    c2.metric("Input features", len(m["features"]))
    c3.metric("Training records", f"{m['rows']:,}")
    st.write(f"**Model selection identifier:** `{m['selected_candidate']}`")
    st.write(f"**Target variable:** `{m['target']}` — {m['target_meaning']['1']}")
    st.write(f"**Default classification threshold:** `{m['threshold']:.6f}` ({m['threshold']:.2%})")

st.write("")
st.caption(DISCLAIMER)
