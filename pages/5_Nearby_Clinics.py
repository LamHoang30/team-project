import pandas as pd
import streamlit as st
from utils.ui import html, tr, render_eiu_header, page_header, DISCLAIMER

render_eiu_header()

IC_HOSP = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l8-4v18"/><path d="M19 21V11l-6-4"/><path d="M9 9v.01"/><path d="M9 12v.01"/><path d="M9 15v.01"/><path d="M9 18v.01"/></svg>'

with st.container(key="hero"):
    page_header(
        IC_HOSP,
        tr(
            "Hệ thống Cơ sở Y tế Chuyên khoa & Gần nhất",
            "Specialized Endocrinology & Nearby Medical Facilities",
            fr="Centres d'Endocrinologie et Établissements Médicaux Proches",
            zh="内分泌专科及附近医疗机构导航",
            ja="内分泌専門・近隣医療機関のご案内",
            ko="내분비 전문 및 가까운 의료기관 안내",
            es="Centros de Endocrinología y Clínicas Cercanas",
        ),
        tr(
            "Tra cứu nhanh bệnh viện tuyến tỉnh, trung ương có chuyên khoa Nội tiết – Đái tháo đường hoặc tìm cơ sở xét nghiệm đường huyết gần vị trí GPS của bạn.",
            "Locate accredited hospitals with Endocrinology & Diabetes departments or open a live Google Maps search near your current GPS location.",
            fr="Localisez les hôpitaux disposant d'un service d'endocrinologie ou lancez une recherche Google Maps autour de votre position GPS.",
            zh="查找设有内分泌与糖尿病专科的医院，或直接通过 Google 地图搜索您当前 GPS 位置附近的血糖检测点。",
            ja="内分泌・糖尿病科のある病院の検索、または現在地周辺の血糖検査機関をGoogleマップで検索できます。",
            ko="내분비·당뇨병 전문 진료과가 있는 병원을 찾거나 현재 GPS 위치 주변의 혈당 검사 기관을 검색하세요.",
            es="Ubique hospitales con departamentos de endocrinología o abra una búsqueda en Google Maps cerca de su ubicación GPS.",
        ),
    )

st.write("")

# Quick GPS Search Banner via Google Maps
with st.container(border=True):
    g1, g2 = st.columns([2.2, 1.0], vertical_alignment="center")
    with g1:
        st.markdown("#### " + tr(
            "📍 Tìm phòng khám / bệnh viện xét nghiệm gần vị trí hiện tại của bạn nhất",
            "📍 Find the nearest blood glucose testing facility via GPS",
            fr="📍 Trouver le centre de dépistage le plus proche via GPS",
            zh="📍 通过 GPS 查找距离您最近的血糖检测机构",
            ja="📍 現在地から最も近い血糖検査機関を検索",
            ko="📍 현재 위치에서 가장 가까운 혈당 검사 기관 찾기",
            es="📍 Buscar el centro de pruebas más cercano por GPS",
        ))
        st.caption(tr(
            "Bấm nút bên cạnh để mở Google Maps tự động định vị GPS của điện thoại/máy tính và chỉ đường tới cơ sở y tế gần nhất.",
            "Click the button to open Google Maps with your device's live GPS and get turn-by-turn directions to the nearest clinic.",
            fr="Cliquez sur le bouton pour ouvrir Google Maps avec votre GPS et obtenir l'itinéraire vers la clinique la plus proche.",
            zh="点击右侧按钮打开 Google 地图自动定位您的位置并导航至最近的医疗机构。",
            ja="ボタンを押すとGoogleマップが開き、現在地から最寄りの医療機関へのルートを表示します。",
            ko="버튼을 누르면 Google 지도가 열려 현재 위치에서 가장 가까운 의료기관으로 길찾기를 안내합니다.",
            es="Haga clic en el botón para abrir Google Maps con su GPS y obtener indicaciones a la clínica más cercana.",
        ))
    with g2:
        st.link_button(
            "🗺️ " + tr(
                "Mở Google Maps gần nhất",
                "Open Nearest on Maps",
                fr="Ouvrir Google Maps",
                zh="打开附近地图",
                ja="Googleマップで開く",
                ko="가까운 병원 지도 열기",
                es="Abrir en Google Maps",
            ),
            url="https://www.google.com/maps/search/bệnh+viện+xét+nghiệm+tiểu+đường+nội+tiết+gần+đây",
            type="primary",
            use_container_width=True,
        )

st.write("")

FACILITIES = [
    {
        "region": "Bình Dương (Thủ Dầu Một & Thành phố Mới)",
        "name": "Bệnh viện Đa khoa Tỉnh Bình Dương (Khoa Nội tiết)",
        "type": tr("Bệnh viện Công lập Tuyến Tỉnh • BHYT", "Provincial Public Hospital • Health Insurance", fr="Hôpital Public Provincial", zh="省级公立综合医院", ja="省立総合病院", ko="성립 종합병원", es="Hospital Público Provincial"),
        "address": "Số 05 Phạm Ngọc Thạch, P. Hiệp Thành, TP. Thủ Dầu Một, Bình Dương",
        "specialty": tr("Chuyên khoa Nội tiết, xét nghiệm đường huyết lúc đói (FPG), HbA1c, tư vấn điều trị tiểu đường.", "Endocrinology Dept, Fasting Glucose (FPG), HbA1c, diabetes management.", fr="Service d'endocrinologie, glycémie à jeun, HbA1c.", zh="内分泌科、空腹血糖、糖化血红蛋白检测。", ja="内分泌科、空腹時血糖、HbA1c検査。", ko="내분비내과, 공복 혈당, 당화혈색소 검사.", es="Endocrinología, glucosa en ayunas, HbA1c."),
        "lat": 10.9961,
        "lon": 106.6558,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=Bệnh+viện+Đa+khoa+tỉnh+Bình+Dương",
    },
    {
        "region": "Bình Dương (Thủ Dầu Một & Thành phố Mới)",
        "name": "Bệnh viện Quốc tế Becamex (Khoa Nội Tổng hợp & Nội tiết)",
        "type": tr("Bệnh viện Đa khoa Quốc tế • BHYT", "International General Hospital • Insurance", fr="Hôpital Général International", zh="国际综合医院", ja="国際総合病院", ko="국제 종합병원", es="Hospital General Internacional"),
        "address": "Khu Gò Cát, P. Lái Thiêu, TP. Thuận An, Bình Dương",
        "specialty": tr("Tầm soát đái tháo đường, rối loạn chuyển hóa, xét nghiệm sinh hóa tự động chuẩn quốc tế.", "Diabetes & metabolic screening, automated clinical biochemistry lab.", fr="Dépistage du diabète et bilan métabolique complet.", zh="糖尿病与代谢综合征筛查、国际标准生化检验。", ja="糖尿病・代謝スクリーニング、国際基準生化学検査。", ko="당뇨병 및 대사 증후군 검진, 자동화 생화학 검사.", es="Detección de diabetes y laboratorio bioquímico."),
        "lat": 10.9095,
        "lon": 106.7024,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=Bệnh+viện+Quốc+tế+Becamex",
    },
    {
        "region": "Bình Dương (Thủ Dầu Một & Thành phố Mới)",
        "name": "Phòng khám Đa khoa Medic Bình Dương",
        "type": tr("Trung tâm Xét nghiệm & Chẩn đoán Y khoa", "Medical Diagnostics & Lab Center", fr="Centre de Diagnostic Médical", zh="医学检验与诊断中心", ja="医療診断・検査センター", ko="의료 진단 및 검사 센터", es="Centro de Diagnóstico Médico"),
        "address": "14A Nguyễn An Ninh, P. Phú Cường, TP. Thủ Dầu Một, Bình Dương",
        "specialty": tr("Xét nghiệm nhanh đường huyết, HbA1c, mỡ máu (Cholesterol), đo huyết áp và tư vấn nội khoa.", "Rapid glucose, HbA1c, lipid panel, blood pressure screening.", fr="Analyse rapide glycémie, HbA1c, bilan lipidique.", zh="快速血糖、HbA1c、血脂及血压检测。", ja="迅速血糖、HbA1c、脂質・血圧検査。", ko="신속 혈당, HbA1c, 고지혈증 및 혈압 검사.", es="Glucosa rápida, HbA1c, perfil lipídico."),
        "lat": 10.9804,
        "lon": 106.6519,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=Phòng+khám+Đa+khoa+Medic+Bình+Dương",
    },
    {
        "region": "TP. Hồ Chí Minh (Tuyến Chuyên sâu)",
        "name": "Bệnh viện Đại học Y Dược TP.HCM (Khoa Nội tiết)",
        "type": tr("Bệnh viện Tuyến Trung ương • Chuyên khoa sâu", "Tertiary University Hospital • Specialist", fr="Hôpital Universitaire Tertiaire", zh="大学附属专科医院", ja="大学附属専門病院", ko="대학병원 전문센터", es="Hospital Universitario Especializado"),
        "address": "215 Hồng Bàng, Phường 11, Quận 5, TP. Hồ Chí Minh",
        "specialty": tr("Trung tâm chuyên sâu hàng đầu phía Nam về Nội tiết – Đái tháo đường và biến chứng chuyển hóa.", "Leading Southern Vietnam center for Endocrinology, Diabetes & metabolic care.", fr="Centre de référence du Sud du Vietnam pour l'endocrinologie et le diabète.", zh="越南南部权威内分泌与糖尿病诊疗中心。", ja="ベトナム南部有数の内分泌・糖尿病専門センター。", ko="베트남 남부 최고 수준의 내분비·당뇨병 전문 센터.", es="Centro líder en endocrinología y diabetes."),
        "lat": 10.7553,
        "lon": 106.6645,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=Bệnh+viện+Đại+học+Y+Dược+TPHCM",
    },
    {
        "region": "TP. Hồ Chí Minh (Tuyến Chuyên sâu)",
        "name": "Bệnh viện Chợ Rẫy (Khoa Nội tiết)",
        "type": tr("Bệnh viện Đa khoa Trung ương Hạng Đặc biệt", "National Special-Grade Hospital", fr="Hôpital National Spécialisé", zh="国家级特等综合医院", ja="国立特級総合病院", ko="국립 특급 종합병원", es="Hospital Nacional Especializado"),
        "address": "201B Nguyễn Chí Thanh, Phường 12, Quận 5, TP. Hồ Chí Minh",
        "specialty": tr("Khám, tầm soát và điều trị chuyên sâu đái tháo đường tuýp 1, tuýp 2 và bệnh lý tim mạch – chuyển hóa.", "Comprehensive Type 1 & Type 2 diabetes and cardiometabolic care.", fr="Prise en charge complète du diabète de type 1 et 2.", zh="1型及2型糖尿病与心血管代谢疾病综合诊疗。", ja="1型・2型糖尿病および心血管代謝疾患の専門診療。", ko="제1형·제2형 당뇨병 및 심혈관 대사 질환 전문 진료.", es="Atención integral de diabetes tipo 1 y tipo 2."),
        "lat": 10.7578,
        "lon": 106.6595,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=Bệnh+viện+Chợ+Rẫy+Khoa+Nội+tiết",
    },
]

regions = [tr("Tất cả khu vực", "All regions", "Toutes les régions", "所有地区", "すべての地域", "전체 지역", "Todas las regiones")] + sorted(list({f["region"] for f in FACILITIES}))
sel_region = st.selectbox(
    tr("Chọn khu vực hiển thị:", "Filter by region:", "Filtrer par région :", "选择地区：", "地域を選択：", "지역 선택:", "Filtrar por región:"),
    options=regions,
)

filtered = FACILITIES if sel_region == regions[0] else [f for f in FACILITIES if f["region"] == sel_region]

col_list, col_map = st.columns([1.35, 1.0], gap="large")

with col_list:
    for item in filtered:
        html(f"""
        <div class="clinic-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;">
                <div style="font-size:1.05rem;font-weight:800;color:#0B3C6D;">🏥 {item['name']}</div>
                <span style="background:#E2F4F7;color:#006875;font-size:0.75rem;font-weight:700;padding:3px 10px;border-radius:999px;">{item['type']}</span>
            </div>
            <div style="font-size:0.86rem;color:#3D5B69;margin-top:6px;"><b>📍</b> {item['address']}</div>
            <div style="font-size:0.85rem;color:#5C7987;margin-top:4px;line-height:1.45;"><b>🩺</b> {item['specialty']}</div>
            <div style="margin-top:10px;">
                <a href="{item['maps_url']}" target="_blank" style="display:inline-block;background:#007B8A;color:#FFFFFF;text-decoration:none;font-size:0.82rem;font-weight:700;padding:6px 14px;border-radius:9px;">
                    🧭 {tr("Chỉ đường trên Google Maps", "Directions on Google Maps", "Itinéraire Google Maps", "Google 地图导航", "Googleマップでルート案内", "Google 지도 길찾기", "Cómo llegar en Google Maps")} →
                </a>
            </div>
        </div>
        """)

with col_map:
    st.markdown("**" + tr("Bản đồ phân bố cơ sở y tế", "Facility Locations Map", "Carte des établissements", "医疗机构分布图", "医療機関マップ", "의료기관 위치 지도", "Mapa de centros médicos") + "**")
    map_df = pd.DataFrame([{"lat": f["lat"], "lon": f["lon"], "name": f["name"]} for f in filtered])
    st.map(map_df, latitude="lat", longitude="lon", size=140, color="#D92B2B")
    st.caption(tr(
        "Điểm đánh dấu màu đỏ thể hiện vị trí các bệnh viện/trung tâm xét nghiệm chuyên khoa.",
        "Red markers indicate accredited hospitals and diabetes diagnostic centers.",
        fr="Les marqueurs rouges indiquent les hôpitaux et centres de dépistage accrédités.",
        zh="红色标记表示设有内分泌与糖尿病检测的医院及诊断中心。",
        ja="赤いマーカーは糖尿病検査に対応した病院・診断センターを示します。",
        ko="빨간색 마커는 당뇨병 검사가 가능한 전문 병원 및 진단 센터를 나타냅니다.",
        es="Los marcadores rojos indican hospitales y centros de diagnóstico acreditados.",
    ))

st.write("")
st.caption(DISCLAIMER)
