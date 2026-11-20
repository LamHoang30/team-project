import streamlit as st

from utils.i18n import t, age_labels, health_labels
from utils.prediction import predict
from utils.ui import html, render_eiu_header, page_header, stepper, field

render_eiu_header()
S = st.session_state
F = S.setdefault("form", {})


def note(text):
    html(f'<div style="font-size:.9rem;color:#3D5B69;font-weight:500;line-height:1.45;margin:.1rem 0 .55rem 0;">{text}</div>')


IC_CLIPBOARD = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M9 12h6M9 16h4"/></svg>'
IC_USER = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-6 8-6s8 2 8 6"/></svg>'
IC_CALENDAR = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
IC_RULER = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 6v4M11 6v3M15 6v4M19 6v3"/></svg>'
IC_BP = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#D92B2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 7-4-14-3 7H2"/></svg>'
IC_CHOL = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.7l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>'
IC_HEALTH = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#007B8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M12 8v6M9 11h6"/></svg>'

YES_NO_MAP = {"yes": t("yes"), "no": t("no")}
UNKNOWN_MAP = {"yes": t("yes"), "no": t("no"), "unknown": t("unknown")}

age_list = age_labels()
age_values = [str(i + 1) for i in range(len(age_list))]
age_map = {str(i + 1): lbl for i, lbl in enumerate(age_list)}

health_list = health_labels()
health_values = [str(i + 1) for i in range(len(health_list))]
health_map = {str(i + 1): lbl for i, lbl in enumerate(health_list)}


def idx_of(options, val):
    return options.index(val) if val in options else None


unk_opts = ["yes", "no", "unknown"]

with st.container(key="assess_sheet"):
    h_col1, h_col2 = st.columns([1.8, 1.0], vertical_alignment="center")
    with h_col1:
        page_header(IC_CLIPBOARD, t("assess_title"), t("assess_sub"))
    with h_col2:
        stepper(0, [t("step_q"), t("step_r")])

    st.write("")

    with st.form("assess_form", border=False):
        c1, c2 = st.columns(2, gap="medium")

        with c1:
            with st.container(key="qcard_1"):
                field(IC_USER, t("about_you"))
                note(t("about_you_note"))
                adult = st.radio(
                    "Adult",
                    options=["yes", "no"],
                    index=idx_of(["yes", "no"], F.get("adult")),
                    format_func=lambda v: YES_NO_MAP[v],
                    horizontal=True,
                    label_visibility="collapsed",
                )

        with c2:
            with st.container(key="qcard_2"):
                field(IC_CALENDAR, t("age"))
                note(t("age_note"))
                age = st.selectbox(
                    "Age",
                    options=age_values,
                    index=idx_of(age_values, F.get("age")),
                    format_func=lambda v: age_map[v],
                    placeholder=t("age_ph"),
                    label_visibility="collapsed",
                )

        with st.container(key="qcard_3"):
            field(IC_RULER, t("hw_title"))
            note(t("hw_note"))
            ch, cw = st.columns(2, gap="medium")
            with ch:
                height = st.number_input(t("height"), min_value=100.0, max_value=230.0, value=float(F.get("height", 160.0)), step=0.5)
            with cw:
                weight = st.number_input(t("weight"), min_value=20.0, max_value=350.0, value=float(F.get("weight", 55.0)), step=0.5)

        c5, c6 = st.columns(2, gap="medium")

        with c5:
            with st.container(key="qcard_4"):
                field(IC_BP, t("bp_q"))
                note(t("bp_note"))
                bp = st.radio("BP", options=unk_opts, index=idx_of(unk_opts, F.get("bp")), format_func=lambda v: UNKNOWN_MAP[v], horizontal=True, label_visibility="collapsed")

        with c6:
            with st.container(key="qcard_5"):
                field(IC_CHOL, t("chol_q"))
                note(t("chol_note"))
                chol = st.radio("Chol", options=unk_opts, index=idx_of(unk_opts, F.get("chol")), format_func=lambda v: UNKNOWN_MAP[v], horizontal=True, label_visibility="collapsed")

        with st.container(key="qcard_6"):
            field(IC_HEALTH, t("health_q"))
            health = st.radio("GenHlth", options=health_values, index=idx_of(health_values, F.get("health")), format_func=lambda v: health_map[v], horizontal=True, label_visibility="collapsed")

        st.write("")
        _, b_right = st.columns([5.2, 2.6])
        with b_right:
            submitted = st.form_submit_button(t("submit") + "  →", type="primary", use_container_width=True)

    if st.button("←  " + t("back")):
        if "_home_page" in S:
            st.switch_page(S["_home_page"])

if submitted:
    F.update(adult=adult, age=age, bp=bp, chol=chol, health=health, height=float(height), weight=float(weight))
    bmi_val = float(weight) / (float(height) / 100.0) ** 2

    if adult == "no":
        st.error(t("err_adult"))
    elif None in (adult, age, bp, chol, health):
        st.error(t("err_missing"))
    elif bp == "unknown" or chol == "unknown":
        st.warning(t("warn_unknown"))
    else:
        answers = {"Age": int(age), "BMI": float(bmi_val), "HighBP": int(bp == "yes"), "HighChol": int(chol == "yes"), "GenHlth": int(health)}
        try:
            with st.spinner(t("wz_calc")):
                p = predict(answers)
            S["answers"] = answers
            S["probability"] = p
            S.pop("active_threshold", None)
            S.pop("active_costs", None)
            st.switch_page("pages/2_My_Results.py")
        except ValueError:
            st.error(t("err_range"))
