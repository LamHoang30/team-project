import streamlit as st
from utils.data_loader import meta
from utils.ui import tr, render_eiu_header, page_header, DISCLAIMER

render_eiu_header()
m = meta()
thresh = float(m["threshold"])

IC_BULB = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>'

with st.container(key="hero"):
    page_header(
        IC_BULB,
        tr(
            "Hiểu rõ kết quả & Kiến thức phòng ngừa",
            "Understanding Your Results & Prevention Guide",
            fr="Comprendre vos résultats et guide de prévention",
            zh="理解评估结果与糖尿病预防指南",
            ja="評価結果の読み方と予防ガイド",
            ko="평가 결과 이해 및 예방 가이드",
            es="Comprender tus resultados y guía de prevención",
        ),
        tr(
            "Giải thích cách mô hình tính điểm, ý nghĩa chỉ số BMI và các xét nghiệm đường huyết chuẩn.",
            "Learn how the score works, what BMI ranges mean, and standard blood glucose tests.",
            fr="Découvrez comment le score est calculé, la signification de l'IMC et les tests glycémiques standard.",
            zh="了解评分原理、BMI 范围含义以及标准血糖检测项目。",
            ja="スコアの仕組み、BMI区分の意味、標準的な血糖検査について解説します。",
            ko="점수 산출 원리, BMI 범위의 의미 및 표준 혈당 검사를 안내합니다.",
            es="Aprende cómo funciona la puntuación, qué significa el IMC y las pruebas estándar de glucosa.",
        ),
    )

st.write("")

c1, c2 = st.columns(2, gap="large")
with c1:
    with st.container(border=True):
        st.markdown("#### " + tr(
            "1. Điểm phần trăm (%) có nghĩa là gì?",
            "1. What does the percentage (%) score mean?",
            fr="1. Que signifie le score en pourcentage (%) ?",
            zh="1. 百分比 (%) 得分代表什么？",
            ja="1. パーセント（%）スコアの意味は？",
            ko="1. 백분율(%) 점수는 무엇을 의미하나요?",
            es="1. ¿Qué significa la puntuación porcentual (%)?",
        ))
        st.write(tr(
            f"Con số này cho biết tỷ lệ những người có cùng đặc điểm sức khỏe như bạn từng báo cáo có tiểu đường hoặc tiền tiểu đường trong khảo sát CDC BRFSS. Ngưỡng gợi ý hiện tại là **{thresh:.1%}** (tỷ lệ phạt FN:FP = 5:1).",
            f"This represents the estimated proportion of survey respondents with similar health indicators who reported diabetes or prediabetes. Default threshold: **{thresh:.1%}** (FN:FP ratio = 5:1).",
            fr=f"Ce chiffre représente la proportion estimée de répondants ayant des indicateurs similaires ayant déclaré un diabète ou prédiabète. Seuil par défaut : **{thresh:.1%}** (ratio FN:FP = 5:1).",
            zh=f"该数字表示在 CDC BRFSS 调查中，具有相似健康特征的人群报告患有糖尿病或糖尿病前期的比例。默认建议阈值为 **{thresh:.1%}**。",
            ja=f"類似した健康指標を持つ調査回答者のうち糖尿病または予備軍と報告した人の推定割合です。デフォルトしきい値は **{thresh:.1%}** です。",
            ko=f"유사한 건강 지표를 가진 설문 응답자 중 당뇨병 또는 전단계를 보고한 비율의 추정치입니다. 기본 임계값은 **{thresh:.1%}**입니다.",
            es=f"Representa la proporción estimada de encuestados con indicadores similares que reportaron diabetes o prediabetes. Umbral: **{thresh:.1%}**.",
        ))

with c2:
    with st.container(border=True):
        st.markdown("#### " + tr(
            "2. Các xét nghiệm y khoa giúp chẩn đoán chính xác",
            "2. Medical tests that confirm diabetes",
            fr="2. Examens médicaux confirmant le diabète",
            zh="2. 确诊糖尿病的医学检查",
            ja="2. 糖尿病を確定診断する医療検査",
            ko="2. 당뇨병을 확진하는 의학적 검사",
            es="2. Pruebas médicas que confirman la diabetes",
        ))
        st.markdown(tr(
            "- **Đường huyết lúc đói (FPG):** Nhịn ăn ≥ 8 giờ. Bình thường < 100 mg/dL (5.6 mmol/L).\n"
            "- **Chỉ số HbA1c:** Đường huyết trung bình 2–3 tháng. Bình thường < 5.7%.\n"
            "- **Nghiệm pháp dung nạp glucose (OGTT):** Đo đường huyết 2 giờ sau uống dung dịch đường.",
            "- **Fasting Plasma Glucose (FPG):** Fast ≥ 8 hours. Normal < 100 mg/dL (5.6 mmol/L).\n"
            "- **HbA1c Test:** 2–3 month average blood sugar. Normal < 5.7%.\n"
            "- **Oral Glucose Tolerance Test (OGTT):** 2-hour post-glucose load blood draw.",
            fr="- **Glycémie à jeun (FPG) :** Jeûne ≥ 8 h. Normale < 100 mg/dL (5,6 mmol/L).\n"
               "- **Test HbA1c :** Moyenne glycémique sur 2–3 mois. Normale < 5,7 %.\n"
               "- **Hyperglycémie provoquée par voie orale (HGPO) :** Mesure 2 h après ingestion de glucose.",
            zh="- **空腹血糖 (FPG)：** 禁食 ≥ 8 小时，正常值 < 100 mg/dL。\n"
               "- **糖化血红蛋白 (HbA1c)：** 反映 2–3 个月平均血糖，正常值 < 5.7%。\n"
               "- **口服葡萄糖耐量试验 (OGTT)：** 饮糖水 2 小时后测血糖。",
            ja="- **空腹時血糖 (FPG)：** 8時間以上絶食、正常値 100 mg/dL 未満。\n"
               "- **HbA1c検査：** 2〜3か月の平均血糖、正常値 5.7% 未満。\n"
               "- **経口ブドウ糖負荷試験 (OGTT)：** 糖液飲用2時間後の血糖測定。",
            ko="- **공복 혈당 (FPG):** 8시간 이상 금식, 정상 100 mg/dL 미만.\n"
               "- **당화혈색소 (HbA1c):** 2~3개월 평균 혈당, 정상 5.7% 미만.\n"
               "- **경구 포도당 내성 검사 (OGTT):** 포도당 섭취 2시간 후 혈당 측정.",
            es="- **Glucosa en ayunas (FPG):** Ayuno ≥ 8 h. Normal < 100 mg/dL.\n"
               "- **Prueba HbA1c:** Promedio de 2–3 meses. Normal < 5.7%.\n"
               "- **Tolerancia oral a la glucosa (OGTT):** Medición a las 2 horas.",
        ))

st.write("")

# Section 3: Interactive BMI Self-Assessment Calculator + Reference Table
with st.container(border=True):
    st.markdown("#### " + tr(
        "3. Công cụ tự đánh giá nhanh chỉ số BMI & Bảng phân loại",
        "3. Quick BMI Self-Assessment Calculator & Reference Table",
        fr="3. Calculateur rapide d'IMC & Tableau de référence",
        zh="3. BMI 快速自测工具与参考分类表",
        ja="3. BMI クイック自己評価ツール & 基準表",
        ko="3. BMI 빠른 자가 평가 도구 및 기준표",
        es="3. Calculadora rápida de IMC y tabla de referencia",
    ))

    b_col1, b_col2, b_col3 = st.columns([1, 1, 1.3], gap="medium")
    with b_col1:
        height_cm = st.number_input(
            tr("Chiều cao (cm)", "Height (cm)", fr="Taille (cm)", zh="身高 (cm)", ja="身長 (cm)", ko="신장 (cm)", es="Altura (cm)"),
            min_value=100.0, max_value=230.0, value=165.0, step=1.0, key="bmi_calc_h"
        )
    with b_col2:
        weight_kg = st.number_input(
            tr("Cân nặng (kg)", "Weight (kg)", fr="Poids (kg)", zh="体重 (kg)", ja="体重 (kg)", ko="체중 (kg)", es="Peso (kg)"),
            min_value=25.0, max_value=250.0, value=60.0, step=0.5, key="bmi_calc_w"
        )

    bmi_val = weight_kg / ((height_cm / 100.0) ** 2)
    if bmi_val < 18.5:
        bmi_cat = tr("Thiếu cân", "Underweight", fr="Insuffisance pondérale", zh="偏瘦", ja="低体重", ko="저체중", es="Bajo peso")
        bmi_color = "#0284C7"
        bmi_bg = "#E0F2FE"
    elif bmi_val < 25.0:
        bmi_cat = tr("Bình thường (Chuẩn WHO)", "Normal weight (WHO)", fr="Poids normal (OMS)", zh="正常体重 (WHO)", ja="普通体重 (WHO)", ko="정상 체중 (WHO)", es="Peso normal (OMS)")
        bmi_color = "#0F766E"
        bmi_bg = "#CCFBF1"
    elif bmi_val < 30.0:
        bmi_cat = tr("Thừa cân", "Overweight", fr="Surpoids", zh="超重", ja="過体重", ko="과체중", es="Sobrepeso")
        bmi_color = "#B45309"
        bmi_bg = "#FEF3C7"
    else:
        bmi_cat = tr("Béo phì", "Obese", fr="Obésité", zh="肥胖", ja="肥満", ko="비만", es="Obesidad")
        bmi_color = "#B91C1C"
        bmi_bg = "#FEE2E2"

    # Asian-Pacific (IDI & WPRO) note
    if bmi_val >= 23.0 and bmi_val < 25.0:
        asia_note = tr(
            "Lưu ý chuẩn Châu Á (WHO WPRO): BMI ≥ 23.0 đã thuộc ngưỡng thừa cân.",
            "Asian-Pacific (WHO WPRO) note: BMI ≥ 23.0 is classified as overweight.",
            fr="Note Asie-Pacifique (OMS) : IMC ≥ 23,0 = surpoids.",
            zh="亚太标准提示 (WHO WPRO)：BMI ≥ 23.0 即属于超重范围。",
            ja="アジア太平洋基準 (WHO WPRO)：BMI 23.0以上は過体重に分類されます。",
            ko="아시아-태평양 기준(WHO WPRO): BMI 23.0 이상은 과체중에 해당합니다.",
            es="Nota Asia-Pacífico (OMS): IMC ≥ 23.0 se considera sobrepeso.",
        )
    elif bmi_val >= 25.0:
        asia_note = tr(
            "Lưu ý chuẩn Châu Á (WHO WPRO): BMI ≥ 25.0 thuộc ngưỡng béo phì.",
            "Asian-Pacific (WHO WPRO) note: BMI ≥ 25.0 is classified as obesity.",
            fr="Note Asie-Pacifique (OMS) : IMC ≥ 25,0 = obésité.",
            zh="亚太标准提示 (WHO WPRO)：BMI ≥ 25.0 即属于肥胖范围。",
            ja="アジア太平洋基準 (WHO WPRO)：BMI 25.0以上は肥満に分類されます。",
            ko="아시아-태평양 기준(WHO WPRO): BMI 25.0 이상은 비만에 해당합니다.",
            es="Nota Asia-Pacífico (OMS): IMC ≥ 25.0 se considera obesidad.",
        )
    else:
        asia_note = tr(
            "Ngưỡng bình thường chuẩn Châu Á (WHO WPRO): 18.5 – 22.9 kg/m².",
            "Asian-Pacific (WHO WPRO) normal range: 18.5 – 22.9 kg/m².",
            fr="Plage normale Asie-Pacifique (OMS) : 18,5 – 22,9 kg/m².",
            zh="亚太正常范围 (WHO WPRO)：18.5 – 22.9 kg/m²。",
            ja="アジア太平洋正常範囲 (WHO WPRO)：18.5 – 22.9 kg/m²。",
            ko="아시아-태평양 정상 범위(WHO WPRO): 18.5 – 22.9 kg/m².",
            es="Rango normal Asia-Pacífico (OMS): 18.5 – 22.9 kg/m².",
        )

    with b_col3:
        st.markdown(
            f"""
            <div style="background:{bmi_bg};border:1px solid {bmi_color}40;border-radius:12px;padding:10px 14px;margin-top:4px;">
                <div style="font-size:0.78rem;color:#475569;font-weight:600;">{tr("Kết quả BMI của bạn", "Your Calculated BMI", fr="Votre IMC calculé", zh="您的 BMI 结果", ja="あなたのBMI結果", ko="계산된 BMI 결과", es="Tu IMC calculado")}</div>
                <div style="font-size:1.35rem;font-weight:800;color:{bmi_color};line-height:1.25;">{bmi_val:.1f} kg/m² <span style="font-size:0.9rem;font-weight:700;">({bmi_cat})</span></div>
                <div style="font-size:0.74rem;color:#334155;margin-top:3px;">{asia_note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    col_cat = tr("Phân loại", "Category", fr="Catégorie", zh="分类", ja="区分", ko="분류", es="Categoría")
    col_who = tr("BMI Quốc tế (WHO)", "Global BMI (WHO)", fr="IMC Mondial (OMS)", zh="国际 BMI (WHO)", ja="国際基準 BMI (WHO)", ko="국제 기준 BMI (WHO)", es="IMC Global (OMS)")
    col_asia = tr("BMI Châu Á (WPRO)", "Asian BMI (WPRO)", fr="IMC Asiatique (WPRO)", zh="亚太 BMI (WPRO)", ja="アジア基準 (WPRO)", ko="아시아 기준 (WPRO)", es="IMC Asiático (WPRO)")
    col_note = tr("Lưu ý sức khỏe & Nguy cơ chuyển hóa", "Health Context & Metabolic Risk", fr="Contexte santé & Risque métabolique", zh="健康提示与代谢风险", ja="健康上の留意点と代謝リスク", ko="건강 참고 사항 및 대사 위험", es="Contexto de salud y riesgo metabólico")

    st.table([
        {
            col_cat: tr("Thiếu cân", "Underweight", fr="Insuffisance pondérale", zh="偏瘦", ja="低体重", ko="저체중", es="Bajo peso"),
            col_who: "< 18.5",
            col_asia: "< 18.5",
            col_note: tr(
                "Cần đảm bảo dinh dưỡng cân đối và kiểm tra sức khỏe tổng quát.",
                "Ensure balanced nutrition and routine health checkups.",
                fr="Assurer une nutrition équilibrée et des bilans réguliers.",
                zh="注意均衡营养并定期进行全面体检。",
                ja="バランスの取れた栄養摂取と定期健診を心がけましょう。",
                ko="균형 잡힌 영양 섭취와 정기 검진이 필요합니다.",
                es="Asegure una nutrición equilibrada y chequeos generales.",
            ),
        },
        {
            col_cat: tr("Bình thường", "Normal weight", fr="Poids normal", zh="正常体重", ja="普通体重", ko="정상 체중", es="Peso normal"),
            col_who: "18.5 – 24.9",
            col_asia: "18.5 – 22.9",
            col_note: tr(
                "Duy trì vận động tối thiểu 150 phút/tuần và chế độ ăn giàu chất xơ.",
                "Maintain at least 150 mins/week of physical activity and fiber-rich meals.",
                fr="Maintenir au moins 150 min/semaine d'activité physique et des repas riches en fibres.",
                zh="每周保持至少 150 分钟中等强度运动及高纤维饮食。",
                ja="週150分以上の運動と食物繊維豊富な食事を維持しましょう。",
                ko="주 150분 이상의 유산소 운동과 식이섬유 위주 식단을 유지하세요.",
                es="Mantenga al menos 150 min/semana de actividad física y dieta rica en fibra.",
            ),
        },
        {
            col_cat: tr("Thừa cân", "Overweight", fr="Surpoids", zh="超重", ja="過体重", ko="과체중", es="Sobrepeso"),
            col_who: "25.0 – 29.9",
            col_asia: "23.0 – 24.9",
            col_note: tr(
                "Giảm 5–7% trọng lượng cơ thể giúp giảm đáng kể nguy cơ tiến triển tiểu đường tuýp 2.",
                "Losing 5–7% of body weight significantly lowers type 2 diabetes progression risk.",
                fr="Perdre 5 à 7 % du poids réduit fortement le risque de diabète de type 2.",
                zh="减轻体重的 5%–7% 可显著降低 2 型糖尿病的发病风险。",
                ja="体重の5〜7%を減量することで2型糖尿病の発症リスクが大幅に低下します。",
                ko="체중의 5~7% 감량만으로도 제2형 당뇨병 진행 위험을 크게 낮출 수 있습니다.",
                es="Perder entre 5% y 7% del peso corporal reduce significativamente el riesgo de diabetes tipo 2.",
            ),
        },
        {
            col_cat: tr("Béo phì", "Obese", fr="Obésité", zh="肥胖", ja="肥満", ko="비만", es="Obesidad"),
            col_who: "≥ 30.0",
            col_asia: "≥ 25.0",
            col_note: tr(
                "Nên tầm soát đường huyết, huyết áp và mỡ máu định kỳ cùng bác sĩ.",
                "Regular screening for blood glucose, blood pressure, and lipids is recommended.",
                fr="Un dépistage régulier de la glycémie, de la tension et des lipides est recommandé.",
                zh="建议在医生指导下定期筛查血糖、血压和血脂。",
                ja="医師の指導のもと、血糖・血圧・脂質の定期検診を推奨します。",
                ko="의료진과 상담하여 혈당, 혈압, 지질 검사를 정기적으로 받으세요.",
                es="Se recomienda detección periódica de glucosa, presión arterial y lípidos.",
            ),
        },
    ])

st.write("")
st.caption(DISCLAIMER)
