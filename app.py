from pathlib import Path
import streamlit as st

from utils.i18n import t, pick_language
from utils.ui import style, html, render_eiu_header, render_healing_audio, GLUCOMETER_SVG

st.set_page_config(
    page_title="GlucoGuide • EIU Health Screening",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto",
)

_logo_file = next((p for p in ["assets/logo_truong.png", "assets/eiu_logo.png", "assets/eiu_logo.svg"] if Path(p).exists()), None)
if _logo_file:
    st.logo(_logo_file, size="large")

style()
pick_language()
render_healing_audio()

st.sidebar.markdown(
    f"""
    <div class="sb-note">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#D92B2B" stroke-width="2" style="flex:0 0 16px;margin-top:2px">
            <circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>
        </svg>
        <span>{t("disclaimer")}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

IC_SHIELD = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'
IC_CHART = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><rect x="7" y="10" width="3" height="7" rx="1"/><rect x="12" y="6" width="3" height="11" rx="1"/><rect x="17" y="13" width="3" height="4" rx="1"/></svg>'
IC_PIN = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#D92B2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'


def home():
    render_eiu_header()
    with st.container(key="hero"):
        left, right = st.columns([6, 5], vertical_alignment="center", gap="large")

        with left:
            html(f"""
            <div class="brand-h1">GlucoGuide</div>
            <div class="hero-sub">{t("hero_sub")}</div>
            <div class="hero-p">{t("hero_p")}</div>
            """)
            b1, b2 = st.columns([1.15, 1.15], gap="small")
            with b1:
                if st.button(t("start_btn") + "  →", type="primary", use_container_width=True):
                    st.switch_page("pages/1_Risk_Assessment.py")
            with b2:
                if st.button("📍 " + t("clinics_btn"), type="secondary", use_container_width=True):
                    st.switch_page("pages/5_Nearby_Clinics.py")

        with right:
            html(f'<div style="text-align:center">{GLUCOMETER_SVG}</div>')

    st.write("")
    feats = [
        (IC_SHIELD, t("feat_1")),
        (IC_CHART, t("feat_2")),
        (IC_PIN, t("feat_3")),
    ]
    for col, (icon, label) in zip(st.columns(3), feats):
        with col:
            html(f'<div class="feat"><div class="ic">{icon}</div><div class="tt">{label}</div></div>')

    st.write("")
    with st.container(border=True):
        st.markdown("**" + t("privacy_title") + "**")
        st.caption(t("home_privacy"))

    st.warning(t("home_diag"))


home_page = st.Page(home, title=t("nav_home"), icon=":material/home:", default=True)
st.session_state["_home_page"] = home_page

pages = [
    home_page,
    st.Page("pages/1_Risk_Assessment.py", title=t("nav_assess"), icon=":material/assignment:"),
    st.Page("pages/2_My_Results.py", title=t("nav_results"), icon=":material/assessment:"),
    st.Page("pages/5_Nearby_Clinics.py", title=t("nav_clinics"), icon=":material/local_hospital:"),
    st.Page("pages/4_Understanding.py", title=t("nav_understand"), icon=":material/lightbulb:"),
    st.Page("pages/3_About_Model.py", title=t("nav_about"), icon=":material/info:"),
]

nav = st.navigation(pages)
nav.run()
