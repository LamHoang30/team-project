import datetime
import streamlit as st

from utils.data_loader import meta
from utils.prediction import load_pipeline, predict
from utils.explanation import explain
from utils.i18n import t, age_labels, health_labels
from utils.ui import html, tr, render_eiu_header, page_header, stepper, ring

render_eiu_header()
S = st.session_state
m = meta()

IC_REPORT = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><rect x="7" y="10" width="3" height="7" rx="1"/><rect x="12" y="6" width="3" height="11" rx="1"/><rect x="17" y="13" width="3" height="4" rx="1"/></svg>'

if "answers" not in S or "probability" not in S:
    st.warning(tr(
        "Bạn chưa nhập thông tin đánh giá. Vui lòng hoàn thành bảng câu hỏi trước.",
        "No assessment data found yet. Please complete the questionnaire first.",
        fr="Aucune donnée d'évaluation trouvée. Veuillez d'abord remplir le questionnaire.",
        zh="尚未找到评估数据，请先完成问卷调查。",
        ja="まだ評価データが入力されていません。先に質問票に回答してください。",
        ko="아직 평가 데이터가 없습니다. 먼저 설문을 완료해 주세요.",
        es="Aún no hay datos de evaluación. Por favor complete el cuestionario primero.",
    ))
    if st.button(t("start_btn") + "  →", type="primary"):
        st.switch_page("pages/1_Risk_Assessment.py")
    st.stop()

answers = S["answers"]
prob = float(S["probability"])
thresh = float(S.get("active_threshold", m["threshold"]))
flagged = prob >= thresh
bmi = float(answers["BMI"])

if bmi < 18.5:
    bmi_cat = tr("Thiếu cân", "Underweight", "Insuffisance pondérale", "偏瘦", "低体重", "저체중", "Bajo peso")
elif bmi < 25:
    bmi_cat = tr("Bình thường", "Normal weight", "Poids normal", "正常体重", "普通体重", "정상 체중", "Peso normal")
elif bmi < 30:
    bmi_cat = tr("Thừa cân", "Overweight", "Surpoids", "超重", "過体重", "과체중", "Sobrepeso")
else:
    bmi_cat = tr("Béo phì", "Obese", "Obésité", "肥胖", "肥満", "비만", "Obesidad")

color = "#D92B2B" if flagged else "#008A6E"
status_text = tr(
    "Nên cân nhắc xét nghiệm đường huyết",
    "Consider a blood glucose test",
    fr="Envisagez un test de glycémie",
    zh="建议考虑进行血糖检测",
    ja="血糖値検査の受診をご検討ください",
    ko="혈당 검사를 고려해 보세요",
    es="Considere hacerse una prueba de glucosa",
) if flagged else tr(
    "Mức nguy cơ ước tính thấp",
    "Lower estimated risk level",
    fr="Niveau de risque estimé faible",
    zh="估算风险水平较低",
    ja="推定リスクは比較的低い水準です",
    ko="추정 위험도가 낮은 수준입니다",
    es="Nivel de riesgo estimado bajo",
)

status_desc = tr(
    f"Điểm ước tính ({prob:.1%}) vượt ngưỡng gợi ý ({thresh:.1%}). Bạn nên đến cơ sở y tế chuyên khoa để xét nghiệm đường huyết lúc đói hoặc HbA1c.",
    f"Your estimated score ({prob:.1%}) is at or above the guidance threshold ({thresh:.1%}). Visit a medical facility for fasting glucose or HbA1c testing.",
    fr=f"Votre score estimé ({prob:.1%}) dépasse le seuil recommandé ({thresh:.1%}). Consultez un centre médical pour un test de glycémie ou d'HbA1c.",
    zh=f"您的估算得分 ({prob:.1%}) 达到或超过建议阈值 ({thresh:.1%})。建议前往医疗机构进行空腹血糖或 HbA1c 检测。",
    ja=f"推定スコア（{prob:.1%}）が目安のしきい値（{thresh:.1%}）以上です。医療機関で空腹時血糖やHbA1c検査をご相談ください。",
    ko=f"추정 점수({prob:.1%})가 권장 기준치({thresh:.1%}) 이상입니다. 의료기관에서 공복 혈당 또는 HbA1c 검사를 상담하세요.",
    es=f"Su puntuación estimada ({prob:.1%}) supera el umbral ({thresh:.1%}). Acuda a un centro médico para una prueba de glucosa o HbA1c.",
) if flagged else tr(
    f"Điểm ước tính ({prob:.1%}) thấp hơn ngưỡng gợi ý ({thresh:.1%}). Tiếp tục duy trì lối sống lành mạnh và kiểm tra sức khỏe định kỳ.",
    f"Your estimated score ({prob:.1%}) is below the guidance threshold ({thresh:.1%}). Maintain healthy habits and routine checkups.",
    fr=f"Votre score estimé ({prob:.1%}) est inférieur au seuil ({thresh:.1%}). Maintenez de bonnes habitudes de vie et des bilans réguliers.",
    zh=f"您的估算得分 ({prob:.1%}) 低于建议阈值 ({thresh:.1%})。请继续保持健康的生活方式并定期体检。",
    ja=f"推定スコア（{prob:.1%}）は目安のしきい値（{thresh:.1%}）未満です。健康的な生活習慣と定期健診を続けましょう。",
    ko=f"추정 점수({prob:.1%})가 권장 기준치({thresh:.1%}) 미만입니다. 건강한 생활습관과 정기 검진을 유지하세요.",
    es=f"Su puntuación estimada ({prob:.1%}) está por debajo del umbral ({thresh:.1%}). Mantenga hábitos saludables y chequeos periódicos.",
)

with st.container(key="result_sheet"):
    h1, h2 = st.columns([1.8, 1.0], vertical_alignment="center")
    with h1:
        page_header(
            IC_REPORT,
            tr("Kết quả đánh giá", "Your Risk Summary", "Résumé de votre évaluation", "您的风险评估摘要", "リスク評価結果", "위험도 평가 요약", "Resumen de resultados"),
            tr("Ước tính dựa trên mô hình học máy từ 5 chỉ số sức khỏe", "Estimated from 5 health indicators", "Estimé à partir de 5 indicateurs de santé", "基于 5 项健康指标的机器学习估算", "5つの健康指標に基づく機械学習推定", "5가지 건강 지표 기반 머신러닝 추정", "Estimado a partir de 5 indicadores de salud"),
        )
    with h2:
        stepper(1, [t("step_q"), t("step_r")])

    st.write("")
    c_ring, c_cards = st.columns([1.0, 2.1], vertical_alignment="center", gap="large")
    with c_ring:
        html(ring(prob, f"{prob:.1%}", color, tr("Điểm ước tính", "Estimated score", "Score estimé", "估算得分", "推定スコア", "추정 점수", "Puntuación")))
    with c_cards:
        k1, k2 = st.columns(2, gap="medium")
        with k1:
            html(f"""
            <div class="cat">
                <div class="k">{tr("Gợi ý hành động", "Guidance", "Recommandation", "行动建议", "推奨アクション", "권장 조치", "Orientación")}</div>
                <div class="v" style="color:{color};font-size:1.22rem;">{status_text}</div>
                <div class="d">{status_desc}</div>
            </div>
            """)
        with k2:
            html(f"""
            <div class="cat">
                <div class="k">{tr("Chỉ số BMI của bạn", "Your BMI", "Votre IMC", "您的 BMI 指数", "あなたのBMI", "나의 BMI 지수", "Tu IMC")}</div>
                <div class="v" style="color:#007B8A;">{bmi:.1f} <span style="font-size:0.95rem;font-weight:600;color:#5C7987;">kg/m²</span></div>
                <div class="d">{tr("Phân loại WHO", "WHO Category", "Catégorie OMS", "WHO 分类", "WHO分類", "WHO 분류", "Categoría OMS")}: <b>{bmi_cat}</b><br>{tr("Ngưỡng xét nghiệm", "Threshold", "Seuil", "参考阈值", "判定しきい値", "기준 임계값", "Umbral")}: <b>{thresh:.1%}</b></div>
            </div>
            """)

st.write("")

with st.container(border=True):
    st.markdown("### " + tr(
        "1. Yếu tố nào ảnh hưởng đến kết quả của bạn?",
        "1. What factors shaped your score?",
        fr="1. Quels facteurs ont influencé votre score ?",
        zh="1. 哪些因素影响了您的评估结果？",
        ja="1. どの要因がスコアに影響しましたか？",
        ko="1. 어떤 요인이 결과에 영향을 미쳤나요?",
        es="1. ¿Qué factores influyeron en tu puntuación?",
    ))
    pipe = load_pipeline()
    exp_df, exp_desc = explain(pipe, answers, m)
    st.caption(exp_desc)

    factor_labels = {
        "Age": tr("Nhóm tuổi", "Age group", "Tranche d'âge", "年龄段", "年齢層", "연령대", "Grupo de edad"),
        "BMI": tr("Chỉ số BMI", "Body Mass Index (BMI)", "Indice de Masse Corporelle (IMC)", "身体质量指数 (BMI)", "BMI指数", "체질량지수 (BMI)", "Índice de Masa Corporal"),
        "HighBP": tr("Huyết áp cao", "High Blood Pressure", "Hypertension artérielle", "高血压", "高血圧", "고혈압", "Presión arterial alta"),
        "HighChol": tr("Mỡ máu cao", "High Cholesterol", "Cholestérol élevé", "高胆固醇", "高コレステロール", "고콜레스테롤", "Colesterol alto"),
        "GenHlth": tr("Sức khỏe tổng quát", "General Health", "Santé générale", "总体健康状况", "全般的健康状態", "전반적 건강 상태", "Salud general"),
    }

    max_abs = max(float(exp_df["Contribution"].abs().max()), 0.01)
    for _, row in exp_df.iterrows():
        val = float(row["Contribution"])
        pct_w = min(100, int(abs(val) / max_abs * 100))
        bar_c = "#D92B2B" if val > 0 else "#008A6E"
        sign = "+" if val > 0 else ""
        fname = factor_labels.get(row["Feature"], row["Factor"])
        html(f"""
        <div class="bar-row">
            <div class="bar-name">{fname}</div>
            <div class="bar-track"><div class="bar-fill" style="width:{pct_w}%;background:{bar_c};"></div></div>
            <div class="bar-val" style="color:{bar_c};">{sign}{val*100:.2f}%</div>
        </div>
        """)

st.write("")

with st.container(border=True):
    st.markdown("### " + tr(
        "2. Mô phỏng kịch bản thay đổi (What-If Simulator)",
        "2. Interactive What-If Scenario Simulator",
        fr="2. Simulateur interactif de scénarios (What-If)",
        zh="2. 交互式健康改善模拟器 (What-If)",
        ja="2. ライフスタイル改善シミュレーション (What-If)",
        ko="2. 건강 개선 시나리오 시뮬레이터 (What-If)",
        es="2. Simulador interactivo de escenarios (What-If)",
    ))
    cur_h = float(S.get("form", {}).get("height", 160.0))
    cur_w = float(S.get("form", {}).get("weight", round(bmi * (cur_h / 100.0) ** 2, 1)))
    w_col1, w_col2 = st.columns(2, gap="medium")
    with w_col1:
        sim_weight = st.slider(
            tr("Cân nặng giả định (kg)", "Simulated weight (kg)", "Poids simulé (kg)", "模拟体重 (kg)", "シミュレーション体重 (kg)", "가상 체중 (kg)", "Peso simulado (kg)"),
            min_value=35.0, max_value=160.0, value=min(max(cur_w, 35.0), 160.0), step=0.5,
        )
    with w_col2:
        h_opts = health_labels()
        sim_health_idx = st.selectbox(
            tr("Sức khỏe tổng quát giả định", "Simulated general health", "Santé générale simulée", "模拟总体健康状况", "シミュレーション健康状態", "가상 건강 상태", "Salud general simulada"),
            options=list(range(1, 6)), index=int(answers["GenHlth"]) - 1, format_func=lambda idx: h_opts[idx - 1],
        )

    sim_bmi = sim_weight / (cur_h / 100.0) ** 2
    sim_answers = dict(answers)
    sim_answers["BMI"] = float(min(max(sim_bmi, 12.0), 98.0))
    sim_answers["GenHlth"] = int(sim_health_idx)
    sim_prob = predict(sim_answers)
    delta_p = sim_prob - prob

    m1, m2, m3 = st.columns(3)
    m1.metric(tr("BMI giả định", "Simulated BMI", "IMC simulé", "模拟 BMI", "推定BMI", "가상 BMI", "IMC simulado"), f"{sim_bmi:.1f}", f"{sim_bmi - bmi:+.1f}", delta_color="inverse")
    m2.metric(tr("Điểm nguy cơ mới", "New Risk Score", "Nouveau score", "新风险评分", "新しいリスクスコア", "새 위험도 점수", "Nueva puntuación"), f"{sim_prob:.1%}", f"{delta_p*100:+.2f}%", delta_color="inverse")
    m3.metric(
        tr("Trạng thái mới", "New Guidance", "Nouvelle orientation", "新建议状态", "新しい判定", "새 권장 상태", "Nuevo estado"),
        tr("Cân nhắc xét nghiệm", "Consider Test", "Envisager un test", "建议检测", "検査検討", "검사 권장", "Considerar prueba") if sim_prob >= thresh else tr("Nguy cơ thấp", "Lower Risk", "Risque faible", "低风险", "低リスク", "낮은 위험", "Riesgo bajo"),
    )

st.write("")

with st.container(border=True):
    st.markdown("### " + tr(
        "3. Tải phiếu tóm tắt & Chọn cơ sở y tế đến khám",
        "3. Download Summary & Locate Nearest Medical Facility",
        fr="3. Télécharger le résumé et trouver un centre médical",
        zh="3. 下载评估报告并查找附近医院",
        ja="3. レポート保存＆近隣の医療機関を探す",
        ko="3. 요약 보고서 다운로드 및 가까운 병원 찾기",
        es="3. Descargar resumen y ubicar centro médico cercano",
    ))
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    age_text = age_labels()[int(answers["Age"]) - 1]
    health_text = health_labels()[int(answers["GenHlth"]) - 1]
    report_txt = f"""============================================================
GLUCOGUIDE (EIU ECON 495) - PERSONAL DIABETES SCREENING SUMMARY
Generated at: {now_str}
============================================================
1. INPUT PROFILE
- Age Group: {age_text}
- Body Mass Index (BMI): {bmi:.1f} kg/m^2 ({bmi_cat})
- High Blood Pressure History: {"Yes" if answers["HighBP"] == 1 else "No"}
- High Cholesterol History: {"Yes" if answers["HighChol"] == 1 else "No"}
- Self-Rated General Health: {health_text}

2. MODEL ESTIMATION ({m["algorithm"]})
- Estimated Survey Risk Score: {prob:.2%}
- Operating Guidance Threshold: {thresh:.2%}
- Guidance Status: {"RECOMMEND DISCUSSING BLOOD GLUCOSE TEST (Fasting Glucose / HbA1c)" if flagged else "LOWER ESTIMATED RISK - MAINTAIN ROUTINE CHECKUPS"}

3. TOP CONTRIBUTING FACTORS (EXACT SHAPLEY VALUES)
""" + "\n".join(f"- {r['Factor']}: {r['Contribution']*100:+.2f}% ({r['Direction']})" for _, r in exp_df.iterrows()) + """
============================================================
"""
    dl_col1, dl_col2, dl_col3 = st.columns([1.3, 1.4, 1.1])
    with dl_col1:
        st.download_button(
            label="📥 " + tr("Tải phiếu tóm tắt (.txt)", "Download Summary (.txt)", "Télécharger le résumé", "下载摘要报告 (.txt)", "レポートを保存 (.txt)", "요약 보고서 저장 (.txt)", "Descargar resumen (.txt)"),
            data=report_txt.encode("utf-8"),
            file_name=f"GlucoGuide_Summary_{datetime.date.today()}.txt",
            mime="text/plain",
            type="secondary",
            use_container_width=True,
        )
    with dl_col2:
        if st.button("🏥 " + tr("Xem cơ sở y tế gần nhất", "Find Nearby Clinics", "Centres médicaux proches", "查看附近医疗机构", "近くの医療機関を見る", "가까운 의료기관 보기", "Ver centros médicos"), type="primary", use_container_width=True):
            st.switch_page("pages/5_Nearby_Clinics.py")
    with dl_col3:
        if st.button("🔄 " + tr("Đánh giá lại", "Re-assess", "Réévaluer", "重新评估", "再評価する", "다시 평가하기", "Reevaluar"), use_container_width=True):
            st.switch_page("pages/1_Risk_Assessment.py")
