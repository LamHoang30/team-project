import streamlit as st

LANGUAGES = {
    "vi": "🇻🇳 Tiếng Việt",
    "en": "🇬🇧 English",
    "fr": "🇫🇷 Français",
    "zh": "🇨🇳 中文 (简体)",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어",
    "es": "🇪🇸 Español",
}

TEXTS = {
    "nav_home": {"vi": "Trang chủ", "en": "Home", "fr": "Accueil", "zh": "首页", "ja": "ホーム", "ko": "홈", "es": "Inicio"},
    "nav_assess": {"vi": "Đánh giá nguy cơ", "en": "Risk Assessment", "fr": "Évaluation du risque", "zh": "风险评估", "ja": "リスク評価", "ko": "위험도 평가", "es": "Evaluación de riesgo"},
    "nav_results": {"vi": "Kết quả", "en": "Results", "fr": "Résultats", "zh": "评估结果", "ja": "評価結果", "ko": "평가 결과", "es": "Resultados"},
    "nav_clinics": {"vi": "Cơ sở y tế gần nhất", "en": "Nearby Clinics & Hospitals", "fr": "Centres médicaux proches", "zh": "附近医疗机构", "ja": "近隣の医療機関", "ko": "가까운 의료기관", "es": "Centros médicos cercanos"},
    "nav_understand": {"vi": "Hiểu kết quả", "en": "Understanding", "fr": "Comprendre les résultats", "zh": "结果解读", "ja": "結果の理解", "ko": "결과 이해하기", "es": "Comprender"},
    "nav_about": {"vi": "Về mô hình (giảng viên)", "en": "About Model", "fr": "À propos du modèle", "zh": "关于模型", "ja": "モデルについて", "ko": "모델 정보", "es": "Sobre el modelo"},
    "hero_sub": {
        "vi": "Hiểu rõ nguy cơ của bạn.<br>Chủ động bước tiếp theo.",
        "en": "Understand your risk.<br>Take informed steps.",
        "fr": "Comprenez votre risque.<br>Agissez de manière éclairée.",
        "zh": "了解您的健康风险。<br>迈出明智的下一步。",
        "ja": "リスクを正しく理解し、<br>次の一歩を踏み出しましょう。",
        "ko": "나의 위험도를 이해하고,<br>현명한 다음 단계를 준비하세요.",
        "es": "Comprende tu riesgo.<br>Toma decisiones informadas.",
    },
    "hero_p": {
        "vi": "Công cụ học máy ước tính nguy cơ tiểu đường, gợi ý xét nghiệm đường huyết và kết nối cơ sở y tế chuyên khoa gần bạn.",
        "en": "A smart tool to estimate your diabetes risk, guide blood sugar testing, and locate nearby specialized clinics.",
        "fr": "Un outil intelligent pour estimer votre risque de diabète, orienter le dépistage glycémique et localiser les cliniques proches.",
        "zh": "智能糖尿病风险评估工具，提供血糖检测建议并查找附近的专科医疗机构。",
        "ja": "糖尿病リスクを推定し、血糖検査の目安と近隣の専門医療機関を案内する教育ツールです。",
        "ko": "당뇨병 위험도를 추정하고 혈당 검사 안내 및 가까운 전문 의료기관 위치를 제공하는 도구입니다.",
        "es": "Una herramienta inteligente para estimar tu riesgo de diabetes, orientar pruebas de glucosa y ubicar clínicas cercanas.",
    },
    "start_btn": {"vi": "Bắt đầu đánh giá", "en": "Start Risk Assessment", "fr": "Démarrer l'évaluation", "zh": "开始风险评估", "ja": "リスク評価を始める", "ko": "위험도 평가 시작", "es": "Iniciar evaluación"},
    "clinics_btn": {"vi": "Tìm cơ sở y tế gần nhất", "en": "Find Nearby Clinics", "fr": "Trouver un centre médical", "zh": "查找附近医院", "ja": "近くの医療機関を探す", "ko": "가까운 병원 찾기", "es": "Buscar centros médicos"},
    "feat_1": {"vi": "Nhanh &<br>dễ dàng", "en": "Quick & Easy<br>Assessment", "fr": "Évaluation<br>rapide et simple", "zh": "快速且<br>简单易用", "ja": "迅速＆<br>簡単チェック", "ko": "빠르고<br>간편한 평가", "es": "Evaluación<br>rápida y fácil"},
    "feat_2": {"vi": "Hiểu rõ<br>nguy cơ", "en": "Understand<br>Your Risk", "fr": "Comprendre<br>votre risque", "zh": "清晰了解<br>自身风险", "ja": "リスク要因を<br>わかりやすく", "ko": "위험 요인<br>명확히 이해", "es": "Comprende<br>tu riesgo"},
    "feat_3": {"vi": "Kết nối cơ sở<br>y tế gần nhất", "en": "Locate Nearby<br>Medical Centers", "fr": "Centres médicaux<br>à proximité", "zh": "定位附近<br>专科医院", "ja": "近隣の専門<br>医療機関案内", "ko": "가까운 전문<br>의료기관 안내", "es": "Centros médicos<br>cercanos"},
    "privacy_title": {"vi": "Quyền riêng tư của bạn", "en": "Your privacy matters", "fr": "Votre vie privée compte", "zh": "您的隐私至关重要", "ja": "プライバシーの保護", "ko": "개인정보 보호", "es": "Tu privacidad importa"},
    "home_privacy": {
        "vi": "Thông tin bạn nhập chỉ được xử lý tạm thời trong phiên làm việc hiện tại để tính toán và không lưu trữ lên máy chủ bên ngoài.",
        "en": "Your answers are processed temporarily in your current session only and are never stored on external servers.",
        "fr": "Vos réponses sont traitées temporairement uniquement durant votre session actuelle et ne sont jamais enregistrées sur des serveurs externes.",
        "zh": "您输入的信息仅在当前会话中临时处理用于计算，不会保存至任何外部服务器。",
        "ja": "入力された情報は現在のセッション内でのみ一時的に処理され、外部サーバーには保存されません。",
        "ko": "입력하신 정보는 현재 세션에서만 일시적으로 처리되며 외부 서버에 저장되지 않습니다.",
        "es": "Tus respuestas se procesan temporalmente solo en esta sesión y nunca se guardan en servidores externos.",
    },
    "home_diag": {
        "vi": "Lưu ý y khoa: Đây là công cụ hỗ trợ nhận thức giáo dục (Đồ án ECON 495 - EIU), không thay thế chẩn đoán của bác sĩ hay xét nghiệm máu.",
        "en": "Medical notice: This is an educational awareness tool (ECON 495 Project - EIU) and does not replace a doctor's diagnosis or blood tests.",
        "fr": "Avis médical : Ceci est un outil éducatif (Projet ECON 495 - EIU) qui ne remplace pas un diagnostic médical ni une analyse sanguine.",
        "zh": "医疗提示：本工具仅用于健康教育参考（EIU ECON 495 课程项目），不能替代医生诊断或血液检测。",
        "ja": "医療上の注意：本ツールは教育目的の参考情報（EIU ECON 495 プロジェクト）であり、医師の診断や血液検査に代わるものではありません。",
        "ko": "의료 안내: 본 도구는 교육용 참고 자료(EIU ECON 495 프로젝트)이며 의사의 진단이나 혈액 검사를 대체하지 않습니다.",
        "es": "Aviso médico: Esta es una herramienta educativa (Proyecto ECON 495 - EIU) y no reemplaza el diagnóstico médico ni los análisis de sangre.",
    },
    "disclaimer": {
        "vi": "Dự án giáo dục EIU — không dùng cho chẩn đoán lâm sàng. Mô hình ước tính nhãn khảo sát tự báo cáo và không chẩn đoán bệnh tiểu đường.",
        "en": "EIU educational project — not for clinical use. This model estimates a self-reported survey label and does not diagnose diabetes.",
        "fr": "Projet éducatif EIU — non destiné à un usage clinique. Ce modèle estime une étiquette d'enquête et ne diagnostique pas le diabète.",
        "zh": "EIU 教育研究项目 — 不可用于临床诊断。本模型仅估算自我报告的调查标签，不构成糖尿病诊断。",
        "ja": "EIU 教育プロジェクト — 臨床診断には使用できません。自己申告調査ラベルを推定するものであり、糖尿病を診断するものではありません。",
        "ko": "EIU 교육용 프로젝트 — 임상 진단용이 아닙니다. 자가 보고 설문 레이블을 추정하며 당뇨병을 진단하지 않습니다.",
        "es": "Proyecto educativo EIU — no apto para uso clínico. Este modelo estima una etiqueta de encuesta y no diagnostica diabetes.",
    },
    "assess_title": {"vi": "Đánh giá nguy cơ", "en": "Risk Assessment", "fr": "Évaluation du risque", "zh": "风险评估", "ja": "リスク評価", "ko": "위험도 평가", "es": "Evaluación de riesgo"},
    "assess_sub": {"vi": "Trả lời 6 câu hỏi ngắn để nhận gợi ý xét nghiệm đường huyết.", "en": "Answer 6 short questions for blood sugar testing guidance.", "fr": "Répondez à 6 courtes questions pour obtenir des conseils de dépistage glycémique.", "zh": "回答 6 个简短问题，获取血糖检测建议。", "ja": "6つの簡単な質問に答えて、血糖検査の目安を確認しましょう。", "ko": "6가지 간단한 질문에 답하고 혈당 검사 안내를 받아보세요.", "es": "Responde 6 preguntas breves para recibir orientación sobre pruebas de glucosa."},
    "step_q": {"vi": "Nhập thông tin", "en": "Questions", "fr": "Questions", "zh": "填写信息", "ja": "質問入力", "ko": "정보 입력", "es": "Preguntas"},
    "step_r": {"vi": "Xem kết quả", "en": "Results", "fr": "Résultats", "zh": "查看结果", "ja": "結果表示", "ko": "결과 확인", "es": "Resultados"},
    "about_you": {"vi": "Xác nhận đối tượng sử dụng", "en": "Eligibility check", "fr": "Vérification d'éligibilité", "zh": "适用人群确认", "ja": "対象者の確認", "ko": "대상자 확인", "es": "Confirmación de elegibilidad"},
    "about_you_note": {"vi": "Từ 18 tuổi trở lên và chưa từng chẩn đoán tiểu đường.", "en": "18+ and never diagnosed with diabetes or prediabetes.", "fr": "18 ans et plus, jamais diagnostiqué diabétique ou prédiabétique.", "zh": "年满 18 周岁且从未被诊断为糖尿病或糖尿病前期。", "ja": "18歳以上で、これまでに糖尿病または予備軍と診断されたことがない方。", "ko": "만 18세 이상이며 당뇨병 또는 전단계 진단을 받은 적이 없는 경우.", "es": "Mayor de 18 años y sin diagnóstico previo de diabetes o prediabetes."},
    "age": {"vi": "Nhóm tuổi của bạn", "en": "Your age group", "fr": "Votre tranche d'âge", "zh": "您的年龄段", "ja": "年齢層", "ko": "연령대", "es": "Grupo de edad"},
    "age_note": {"vi": "Chọn khoảng tuổi hiện tại của bạn.", "en": "Select your current age range.", "fr": "Sélectionnez votre tranche d'âge actuelle.", "zh": "请选择您当前的年龄范围。", "ja": "現在の年齢区分を選択してください。", "ko": "현재 해당하는 연령대를 선택하세요.", "es": "Selecciona tu rango de edad actual."},
    "age_ph": {"vi": "Chọn nhóm tuổi...", "en": "Select age range...", "fr": "Choisir une tranche d'âge...", "zh": "请选择年龄段...", "ja": "年齢層を選択...", "ko": "연령대 선택...", "es": "Selecciona edad..."},
    "hw_title": {"vi": "Chiều cao và cân nặng", "en": "Height and weight", "fr": "Taille et poids", "zh": "身高与体重", "ja": "身長と体重", "ko": "신장 및 체중", "es": "Estatura y peso"},
    "hw_note": {"vi": "BMI sẽ được tính tự động và hiển thị ở trang kết quả.", "en": "BMI is calculated automatically and shown on the results page.", "fr": "L'IMC est calculé automatiquement et affiché sur la page des résultats.", "zh": "系统将自动计算 BMI 并在结果页面显示。", "ja": "BMIは自動計算され、結果ページに表示されます。", "ko": "BMI는 자동으로 계산되어 결과 페이지에 표시됩니다.", "es": "El IMC se calcula automáticamente y se muestra en los resultados."},
    "height": {"vi": "Chiều cao (cm)", "en": "Height (cm)", "fr": "Taille (cm)", "zh": "身高 (cm)", "ja": "身長 (cm)", "ko": "신장 (cm)", "es": "Estatura (cm)"},
    "weight": {"vi": "Cân nặng (kg)", "en": "Weight (kg)", "fr": "Poids (kg)", "zh": "体重 (kg)", "ja": "体重 (kg)", "ko": "체중 (kg)", "es": "Peso (kg)"},
    "bp_q": {"vi": "Đã từng được báo huyết áp cao?", "en": "Ever told you have high blood pressure?", "fr": "Vous a-t-on déjà dit que vous aviez de l'hypertension ?", "zh": "医生是否曾告知您患有高血压？", "ja": "これまでに高血圧と言われたことはありますか？", "ko": "고혈압 진단을 받은 적이 있습니까?", "es": "¿Alguna vez le dijeron que tiene presión arterial alta?"},
    "bp_note": {"vi": "Không tính lúc mang thai hoặc chỉ hơi cao.", "en": "Exclude pregnancy-only or borderline readings.", "fr": "Exclure les valeurs liées uniquement à la grossesse ou limites.", "zh": "不包括仅在怀孕期间出现或临界偏高的情况。", "ja": "妊娠中のみの場合や境界域の数値は除きます。", "ko": "임신 중 일시적 상승이나 경계성 수치는 제외합니다.", "es": "Excluya lecturas solo durante el embarazo o valores límite."},
    "chol_q": {"vi": "Đã từng được báo mỡ máu cao?", "en": "Ever told you have high cholesterol?", "fr": "Vous a-t-on déjà dit que vous aviez un taux de cholestérol élevé ?", "zh": "医生是否曾告知您胆固醇（血脂）偏高？", "ja": "これまでにコレステロールが高いと言われたことはありますか？", "ko": "고지혈증(높은 콜레스테롤) 진단을 받은 적이 있습니까?", "es": "¿Alguna vez le dijeron que tiene colesterol alto?"},
    "chol_note": {"vi": 'Chọn "Tôi không biết" nếu chưa đo hoặc không chắc.', "en": "Choose 'I do not know' if unchecked or unsure.", "fr": "Choisissez « Je ne sais pas » si non vérifié ou incertain.", "zh": "如果从未检查或不确定，请选择“我不知道”。", "ja": "未検査または不明な場合は「わからない」を選択してください。", "ko": "검사한 적이 없거나 잘 모르면 '모르겠음'을 선택하세요.", "es": "Elija 'No lo sé' si no se ha revisado o no está seguro."},
    "health_q": {"vi": "Bạn tự đánh giá sức khỏe tổng quát của mình thế nào?", "en": "How would you rate your general health?", "fr": "Comment évalueriez-vous votre santé générale ?", "zh": "您如何评价自己的总体健康状况？", "ja": "ご自身の全体的な健康状態をどう評価しますか？", "ko": "전반적인 건강 상태를 어떻게 평가하십니까?", "es": "¿Cómo calificaría su salud general?"},
    "yes": {"vi": "Có", "en": "Yes", "fr": "Oui", "zh": "是", "ja": "はい", "ko": "예", "es": "Sí"},
    "no": {"vi": "Không", "en": "No", "fr": "Non", "zh": "否", "ja": "いいえ", "ko": "아니요", "es": "No"},
    "unknown": {"vi": "Tôi không biết", "en": "I do not know", "fr": "Je ne sais pas", "zh": "我不知道", "ja": "わからない", "ko": "모르겠음", "es": "No lo sé"},
    "submit": {"vi": "Xem kết quả", "en": "See Results", "fr": "Voir les résultats", "zh": "查看评估结果", "ja": "結果を見る", "ko": "결과 보기", "es": "Ver resultados"},
    "back": {"vi": "Quay lại", "en": "Back", "fr": "Retour", "zh": "返回", "ja": "戻る", "ko": "뒤로", "es": "Volver"},
    "err_adult": {"vi": "Công cụ này chỉ dành cho người từ 18 tuổi trở lên và chưa từng được chẩn đoán tiểu đường.", "en": "This tool is only intended for adults aged 18+ without a prior diabetes diagnosis.", "fr": "Cet outil est uniquement destiné aux adultes de 18 ans et plus sans diagnostic préalable de diabète.", "zh": "本工具仅适用于 18 岁及以上且未被诊断为糖尿病的成年人。", "ja": "このツールは18歳以上で糖尿病の診断歴がない成人を対象としています。", "ko": "이 도구는 당뇨병 진단 이력이 없는 만 18세 이상 성인 전용입니다.", "es": "Esta herramienta es solo para adultos mayores de 18 años sin diagnóstico previo de diabetes."},
    "err_missing": {"vi": "Vui lòng trả lời đầy đủ tất cả các câu hỏi trước khi xem kết quả.", "en": "Please answer all questions before viewing your results.", "fr": "Veuillez répondre à toutes les questions avant de consulter vos résultats.", "zh": "请先回答所有问题，然后再查看结果。", "ja": "結果を表示する前にすべての質問に回答してください。", "ko": "결과를 확인하기 전에 모든 질문에 답변해 주세요.", "es": "Por favor responda todas las preguntas antes de ver los resultados."},
    "warn_unknown": {"vi": "Bạn chọn 'Tôi không biết' ở mục huyết áp hoặc mỡ máu. Mô hình cần giá trị xác định (Có/Không) để ước tính chính xác — bạn nên kiểm tra huyết áp và mỡ máu tại cơ sở y tế.", "en": "You selected 'I do not know' for blood pressure or cholesterol. The model requires a known Yes/No answer — consider getting a basic checkup.", "fr": "Vous avez sélectionné « Je ne sais pas » pour la tension ou le cholestérol. Le modèle nécessite une réponse connue (Oui/Non).", "zh": "您在血压或血脂项选择了“我不知道”。模型需要明确的“是/否”信息进行估算，建议您先进行基础体检。", "ja": "血圧またはコレステロールで「わからない」が選択されています。推定には「はい/いいえ」の回答が必要なため、健康診断での確認をおすすめします。", "ko": "혈압 또는 콜레스테롤 항목에서 '모르겠음'을 선택하셨습니다. 정확한 추정을 위해 확인 후 다시 입력해 주세요.", "es": "Seleccionó 'No lo sé' en presión arterial o colesterol. El modelo requiere una respuesta conocida (Sí/No); considere realizarse un chequeo básico."},
    "wz_calc": {"vi": "Đang phân tích dữ liệu và tính toán...", "en": "Calculating your risk profile...", "fr": "Calcul de votre profil de risque en cours...", "zh": "正在分析数据并计算...", "ja": "リスクプロファイルを計算中...", "ko": "위험도 프로필 계산 중...", "es": "Calculando su perfil de riesgo..."},
    "err_range": {"vi": "Giá trị chiều cao hoặc cân nặng tạo ra chỉ số BMI nằm ngoài phạm vi hợp lệ của mô hình (12–98).", "en": "Height and weight yield a BMI outside the valid model range (12–98).", "fr": "La taille et le poids donnent un IMC en dehors de la plage valide du modèle (12–98).", "zh": "输入的身高和体重计算出的 BMI 超出模型有效范围 (12–98)。", "ja": "入力された身長と体重から算出されたBMIがモデルの有効範囲（12〜98）外です。", "ko": "입력한 신장과 체중으로 계산된 BMI가 모델 유효 범위(12–98)를 벗어납니다.", "es": "La estatura y el peso generan un IMC fuera del rango válido del modelo (12–98)."},
}

AGE_BANDS = ["18–24", "25–29", "30–34", "35–39", "40–44", "45–49", "50–54", "55–59", "60–64", "65–69", "70–74", "75–79", "80+"]
HEALTH_MAP = {
    "vi": ["1 - Rất tốt", "2 - Tốt", "3 - Khá", "4 - Trung bình", "5 - Kém"],
    "en": ["1 - Excellent", "2 - Very Good", "3 - Good", "4 - Fair", "5 - Poor"],
    "fr": ["1 - Excellente", "2 - Très bonne", "3 - Bonne", "4 - Passable", "5 - Mauvaise"],
    "zh": ["1 - 极好", "2 - 很好", "3 - 良好", "4 - 一般", "5 - 较差"],
    "ja": ["1 - 最高に良い", "2 - とても良い", "3 - 良い", "4 - あまり良くない", "5 - 悪い"],
    "ko": ["1 - 매우 좋음", "2 - 아주 좋음", "3 - 좋음", "4 - 보통", "5 - 나쁨"],
    "es": ["1 - Excelente", "2 - Muy buena", "3 - Buena", "4 - Regular", "5 - Mala"],
}

def lang(): return st.session_state.get("lang", "vi")
def t(key):
    entry = TEXTS.get(key, {})
    return entry.get(lang(), entry.get("en", key))
def age_labels():
    suffix = {"vi": " tuổi", "en": " yrs", "fr": " ans", "zh": " 岁", "ja": " 歳", "ko": " 세", "es": " años"}.get(lang(), "")
    return [f"{b}{suffix}" for b in AGE_BANDS]
def health_labels(): return HEALTH_MAP.get(lang(), HEALTH_MAP["en"])
def pick_language():
    if "lang" not in st.session_state:
        st.session_state["lang"] = "vi"
    def _on_lang_change():
        st.session_state["lang"] = st.session_state["_lang_widget"]
    st.sidebar.selectbox("🌐 Language / Ngôn ngữ", options=list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(st.session_state["lang"]), format_func=lambda k: LANGUAGES[k], key="_lang_widget", on_change=_on_lang_change)
