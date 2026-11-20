import base64
import wave
from pathlib import Path
import numpy as np
import streamlit as st
from utils.i18n import pick_language, t, lang as _lang

DISCLAIMER = t('disclaimer')


def tr(vi, en, fr=None, zh=None, ja=None, ko=None, es=None):
    cur = _lang()
    mapping = {'vi': vi, 'en': en, 'fr': fr, 'zh': zh, 'ja': ja, 'ko': ko, 'es': es}
    return mapping.get(cur) or en


def html(s):
    st.markdown('\n'.join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def render_eiu_header():
    """Hiển thị logo trường Đại học Quốc tế Miền Đông (EIU) + huy hiệu Y tế Việt Nam."""
    logo_path = Path(__file__).resolve().parents[1] / "assets"
    custom_png = next((p for p in [logo_path / "logo_truong.png", logo_path / "eiu_logo.png", logo_path / "logo.png"] if p.exists()), None)

    if custom_png:
        b64 = base64.b64encode(custom_png.read_bytes()).decode("ascii")
        img_tag = f'<img src="data:image/png;base64,{b64}" style="height:54px;width:auto;object-fit:contain;border-radius:6px;" alt="EIU Logo"/>'
    else:
        svg_file = logo_path / "eiu_logo.svg"
        if svg_file.exists():
            b64 = base64.b64encode(svg_file.read_bytes()).decode("ascii")
            img_tag = f'<img src="data:image/svg+xml;base64,{b64}" style="height:46px;width:auto;" alt="EIU Logo"/>'
        else:
            img_tag = '<strong style="color:#0B3C6D;font-size:1.1rem;">EIU • Eastern International University</strong>'

    badge_txt = tr(
        "Cổng Sàng Lọc Sức Khỏe Cộng Đồng • Chuẩn Màu Y Tế Việt Nam",
        "Community Health Screening Portal • Vietnam Medical Palette",
        fr="Portail de Dépistage Communautaire • Palette Médicale Vietnam",
        zh="社区健康筛查平台 • 越南医疗标准配色",
        ja="地域健康スクリーニング • ベトナム医療カラー",
        ko="지역사회 건강 스크리닝 • 베트남 의료 테마",
        es="Portal de Detección Comunitaria • Paleta Médica Vietnam",
    )

    html(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;background:#FFFFFF;border:1px solid #C5E2E8;border-radius:16px;padding:10px 18px;margin-bottom:14px;box-shadow:0 3px 12px rgba(0,123,138,0.06);">
        <div style="display:flex;align-items:center;gap:12px;">
            {img_tag}
        </div>
        <div style="display:flex;align-items:center;gap:8px;background:#E6F4F6;border:1px solid #B8DFE6;border-radius:999px;padding:6px 14px;font-size:0.8rem;font-weight:700;color:#006875;">
            <span style="display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:#D92B2B;color:#FFF;font-size:12px;font-weight:900;">+</span>
            <span>{badge_txt}</span>
        </div>
    </div>
    """)


def _ensure_healing_wav_file() -> str:
    """Tạo file nhạc thư giãn y khoa 432Hz vào assets/healing_432hz.wav."""
    assets_dir = Path(__file__).resolve().parents[1] / "assets"
    assets_dir.mkdir(exist_ok=True)
    wav_path = assets_dir / "healing_432hz.wav"
    if wav_path.exists() and wav_path.stat().st_size > 1000:
        return str(wav_path)

    sr = 22050
    dur = 16.0
    t_arr = np.linspace(0, dur, int(sr * dur), endpoint=False)
    audio = np.zeros_like(t_arr)

    for idx, f in enumerate([174.61, 216.0, 261.63, 323.63, 432.0]):
        lfo = 0.75 + 0.25 * np.sin(2 * np.pi * (0.125 * (idx + 1)) * t_arr)
        audio += (0.06 / (1 + 0.25 * idx)) * lfo * np.sin(2 * np.pi * f * t_arr)

    melody = [432.0, 513.74, 647.27, 576.65, 432.0, 384.87, 513.74, 432.0]
    for i, f in enumerate(melody):
        start = i * 2.0
        mask = t_arr >= start
        dt = t_arr[mask] - start
        env = np.exp(-1.4 * dt) * (1.0 - np.exp(-25.0 * dt))
        audio[mask] += 0.22 * env * (np.sin(2 * np.pi * f * dt) + 0.35 * np.sin(2 * np.pi * (f * 2) * dt))

    fade = int(0.15 * sr)
    audio[:fade] *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)

    pcm = np.clip(audio * 32767, -32767, 32767).astype(np.int16)
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    return str(wav_path)


def render_healing_audio():
    """Trình phát nhạc chữa lành 432Hz ở thanh bên với tự động kích hoạt khi chạm trang."""
    wav_file = _ensure_healing_wav_file()
    label_title = tr(
        "🎵 Nhạc thư giãn y khoa (432Hz)",
        "🎵 Medical Healing Music (432Hz)",
        fr="🎵 Musique thérapeutique (432Hz)",
        zh="🎵 医疗舒缓疗愈音乐 (432Hz)",
        ja="🎵 医療ヒーリング音楽 (432Hz)",
        ko="🎵 메디컬 힐링 사운드 (432Hz)",
        es="🎵 Música terapéutica (432Hz)",
    )
    with st.sidebar:
        st.caption(label_title)
        st.audio(wav_file, format="audio/wav", loop=True, autoplay=True)

    st.markdown(
        """
        <script>
        (function() {
            const unlockAudio = () => {
                const audios = window.parent.document.querySelectorAll('audio');
                audios.forEach(a => {
                    if (a.paused) {
                        a.play().catch(() => {});
                    }
                });
            };
            ['click', 'touchstart', 'keydown'].forEach(evt => {
                window.parent.document.addEventListener(evt, unlockAudio, { once: true });
            });
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def style():
    # Vietnam Ministry of Health (Bộ Y tế Việt Nam) color palette:
    # Primary Medical Teal/Cyan (#007B8A), Deep Navy Blue (#0B3C6D), Red Cross Accent (#D92B2B), Pure Clinical White (#FFFFFF)
    st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --g: #007B8A;
    --gd: #005B68;
    --navy: #0B3C6D;
    --g-soft: #E2F4F7;
    --med-bg: #F0F8FA;
    --card-bg: #FFFFFF;
    --ink: #0E2A36;
    --ink-sub: #3D5B69;
    --muted: #5C7987;
    --line: #C5E2E8;
    --amber: #D97706;
    --red: #D92B2B;
    --ok: #008A6E;
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: linear-gradient(145deg, #F7FCFD 0%, #EBF6F9 55%, #D6EEF3 100%) !important;
    background-attachment: fixed !important;
    color: var(--ink) !important;
    color-scheme: light !important;
}

.stApp, .stApp p, .stApp label, .stApp li, .stApp button, .stApp input,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1080px;
    padding-top: 1.2rem;
    padding-bottom: 2.8rem;
}

h1, h2, h3 {
    color: var(--navy) !important;
    letter-spacing: -0.4px;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #FFFFFF 0%, #EEF7F9 70%, #DCF0F4 100%) !important;
    border-right: 1px solid var(--line) !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: var(--ink) !important;
}

[data-testid="stSidebarNavLink"] {
    border-radius: 12px !important;
    font-weight: 500 !important;
    color: #274857 !important;
    padding: 0.55rem 0.9rem !important;
    margin-bottom: 4px;
    transition: all 0.15s ease;
}

[data-testid="stSidebarNavLink"]:hover {
    background: rgba(0, 123, 138, 0.09) !important;
}

[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: #D6EFF4 !important;
    color: var(--g) !important;
    font-weight: 700 !important;
    box-shadow: inset 3px 0 0 var(--g);
}

.sb-note {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    background: #FFFFFF;
    border: 1px solid #C5E2E8;
    border-left: 4px solid var(--red);
    border-radius: 12px;
    padding: 12px 14px;
    color: #2E4B59;
    font-size: 0.8rem;
    line-height: 1.45;
    margin-top: 0.4rem;
    box-shadow: 0 2px 8px rgba(0, 123, 138, 0.05);
}

div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #008294 0%, #0B3C6D 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    padding: 0 1.5rem !important;
    box-shadow: 0 4px 12px rgba(0, 123, 138, 0.24) !important;
    transition: transform 0.12s ease, box-shadow 0.15s ease !important;
}

div.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #006A78 0%, #082D52 100%) !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 123, 138, 0.30) !important;
}

div.stButton > button[kind="primary"] p,
div[data-testid="stFormSubmitButton"] > button p {
    color: #FFFFFF !important;
}

div.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    border: 1.5px solid #B7DCE4 !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    color: var(--navy) !important;
    font-weight: 600 !important;
    padding: 0 1.25rem !important;
}

div.stButton > button[kind="secondary"]:hover {
    border-color: var(--g) !important;
    color: var(--g) !important;
    background: #EFF8FA !important;
}

div[data-baseweb="input"], div[data-baseweb="select"] > div {
    background: #F7FCFD !important;
    border: 1.5px solid #C5E2E8 !important;
    border-radius: 11px !important;
    min-height: 44px !important;
    color: var(--ink) !important;
}

div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
    border-color: var(--g) !important;
    box-shadow: 0 0 0 3px rgba(0, 123, 138, 0.14) !important;
    background: #FFFFFF !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] span {
    color: var(--ink) !important;
    font-size: 16px !important;
}

button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    display: none !important;
}

div[data-testid="stRadio"] > div {
    gap: 0.65rem;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] label {
    background: #F3FAFC;
    border: 1px solid #CBE5EB;
    border-radius: 10px;
    padding: 8px 14px !important;
    font-size: 0.93rem;
    color: var(--ink) !important;
    min-height: 42px;
    display: inline-flex;
    align-items: center;
    transition: all 0.15s ease;
}

div[data-testid="stRadio"] label:hover {
    border-color: var(--g);
    background: #E2F4F7;
}

input[type="radio"] {
    accent-color: var(--g) !important;
}

.st-key-hero {
    background: linear-gradient(125deg, #FFFFFF 0%, #EDF8FA 58%, #CBEAF0 100%) !important;
    border: 1px solid var(--line);
    border-radius: 26px;
    padding: 2.2rem 2.4rem;
    box-shadow: 0 10px 30px rgba(0, 123, 138, 0.07);
}

.st-key-assess_sheet {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 1.8rem 2rem;
    box-shadow: 0 8px 26px rgba(0, 123, 138, 0.06);
}

.st-key-result_sheet {
    background: linear-gradient(130deg, #FFFFFF 0%, #ECF7F9 58%, #CBEAF0 100%) !important;
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 1.8rem 2rem;
    box-shadow: 0 8px 26px rgba(0, 123, 138, 0.07);
}

[class*="st-key-qcard_"] {
    background: #F8FCFD;
    border: 1px solid #D1E9EE;
    border-radius: 16px;
    padding: 15px 18px 14px 18px;
    box-shadow: 0 2px 6px rgba(0, 123, 138, 0.03);
    min-height: 118px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

[class*="st-key-qcard_"]:hover {
    border-color: #77C2CE;
    box-shadow: 0 4px 14px rgba(0, 123, 138, 0.08);
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

.brand-h1 {
    font-size: 3.2rem;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: -1.5px;
    line-height: 1.05;
    margin: 0;
}

.hero-sub {
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.28;
    color: var(--g);
    margin: 0.85rem 0 0.7rem;
}

.hero-p {
    color: var(--ink-sub);
    font-size: 1rem;
    line-height: 1.65;
    max-width: 31rem;
    margin-bottom: 1.3rem;
}

.feat {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid var(--line);
    border-radius: 18px;
    text-align: center;
    padding: 1.1rem 0.6rem;
    box-shadow: 0 4px 14px rgba(0, 123, 138, 0.04);
}

.feat .ic {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: var(--g-soft);
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.feat .tt {
    font-weight: 700;
    color: var(--navy);
    font-size: 0.93rem;
    margin-top: 0.6rem;
    line-height: 1.35;
}

.ph {
    display: flex;
    gap: 14px;
    align-items: center;
}

.ph .ico {
    width: 46px;
    height: 46px;
    border-radius: 13px;
    background: var(--g-soft);
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 46px;
}

.ph .tt {
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: -0.5px;
    line-height: 1.15;
}

.ph .ss {
    font-size: 0.9rem;
    color: var(--ink-sub);
    margin-top: 3px;
}

.stp {
    display: flex;
    align-items: flex-start;
    justify-content: flex-end;
}

.stp .st {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    font-size: 0.75rem;
    color: var(--muted);
    width: 88px;
    text-align: center;
}

.stp .n {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #DCEEF2;
    color: #5C7987;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.82rem;
}

.stp .on .n, .stp .done .n {
    background: var(--g);
    color: #FFFFFF;
}

.stp .on {
    color: var(--navy);
    font-weight: 700;
}

.stp .ln {
    flex: 0 0 24px;
    height: 2px;
    background: #C5E2E8;
    margin-top: 13px;
}

.stp .ln.done {
    background: var(--g);
}

.fl {
    font-weight: 700;
    color: var(--navy);
    font-size: 0.95rem;
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 0.35rem;
}

.ring-card {
    background: #FFFFFF;
    border: 1px solid #CBE5EB;
    border-radius: 50%;
    width: 192px;
    height: 192px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(0, 123, 138, 0.10);
}

.cat {
    background: #FFFFFF;
    border: 1px solid #C5E2E8;
    border-radius: 16px;
    padding: 18px 20px;
    position: relative;
}

.cat .k {
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.cat .v {
    font-size: 1.75rem;
    font-weight: 800;
    margin: 0.25rem 0 0.45rem;
    line-height: 1.15;
}

.cat .d {
    font-size: 0.88rem;
    color: var(--ink-sub);
    line-height: 1.48;
}

.bar-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0.75rem 0;
}

.bar-name {
    flex: 0 0 195px;
    font-size: 0.91rem;
    color: var(--navy);
    font-weight: 600;
}

.bar-track {
    flex: 1;
    height: 16px;
    background: #E4F2F5;
    border-radius: 8px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 8px;
}

.bar-val {
    flex: 0 0 105px;
    text-align: right;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--ink-sub);
}

.clinic-card {
    background: #FFFFFF;
    border: 1px solid #C5E2E8;
    border-left: 5px solid #007B8A;
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(0, 123, 138, 0.05);
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-top: 0.8rem !important;
    }
    .st-key-hero, .st-key-assess_sheet, .st-key-result_sheet {
        padding: 1.25rem 1.1rem !important;
        border-radius: 18px !important;
    }
    .brand-h1 { font-size: 2.25rem !important; }
    .hero-sub { font-size: 1.25rem !important; }
    .ph .tt { font-size: 1.3rem !important; }
    .stp { justify-content: flex-start; margin-top: 0.6rem; }
    .stp .st { width: 72px; font-size: 0.7rem; }
    .bar-name { flex-basis: 115px; font-size: 0.83rem; }
    .bar-val { flex-basis: 82px; font-size: 0.78rem; }
}
</style>''', unsafe_allow_html=True)


def page_header(icon, title, sub=''):
    sub_html = f'<div class="ss">{sub}</div>' if sub else ''
    html(f'<div class="ph"><div class="ico">{icon}</div><div><div class="tt">{title}</div>{sub_html}</div></div>')


def stepper(current, labels):
    parts = []
    for k, label in enumerate(labels):
        cls = 'done' if k < current else 'on' if k == current else ''
        mark = '✓' if k < current else k + 1
        parts.append(f'<div class="st {cls}"><div class="n">{mark}</div>{label}</div>')
        if k < len(labels) - 1:
            parts.append(f'<div class="ln {"done" if k < current else ""}"></div>')
    html('<div class="stp">' + ''.join(parts) + '</div>')


def field(icon, label):
    html(f'<div class="fl"><span>{icon}</span><span>{label}</span></div>')


def ring(frac, text, color, sub):
    r = 68
    c = 6.28318 * r
    d = c * max(0.05, min(1.0, frac))
    return (
        f'<div class="ring-card">'
        f'<svg viewBox="0 0 180 180" width="176" height="176">'
        f'<circle cx="90" cy="90" r="{r}" fill="none" stroke="#D6EEF3" stroke-width="14"/>'
        f'<circle cx="90" cy="90" r="{r}" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round" '
        f'stroke-dasharray="{d:.1f} {c:.1f}" transform="rotate(-90 90 90)"/>'
        f'<text x="90" y="92" text-anchor="middle" font-size="30" font-weight="800" fill="#0B3C6D" font-family="Plus Jakarta Sans,sans-serif">{text}</text>'
        f'<text x="90" y="114" text-anchor="middle" font-size="11.5" fill="#5C7987" font-family="Plus Jakarta Sans,sans-serif">{sub}</text>'
        f'</svg></div>'
    )


GLUCOMETER_SVG = '''<svg viewBox="0 0 330 290" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:320px">
<path d="M210 78c-24-44-90-32-90 20 0 44 58 76 90 108 32-32 90-64 90-108 0-52-66-64-90-20z" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linejoin="round"/>
<ellipse cx="262" cy="196" rx="30" ry="14" fill="#4DB6AC" transform="rotate(-35 262 196)"/>
<ellipse cx="288" cy="214" rx="24" ry="11" fill="#00897B" transform="rotate(20 288 214)"/>
<rect x="60" y="262" width="240" height="16" rx="8" fill="#B2DFDB"/>
<g transform="rotate(-8 170 160)">
<rect x="116" y="70" width="122" height="190" rx="24" fill="#0B3C6D"/>
<rect x="128" y="84" width="98" height="66" rx="10" fill="#E6F4F6"/>
<text x="188" y="132" text-anchor="middle" font-size="38" font-weight="800" fill="#0B3C6D" font-family="Arial,sans-serif">98</text>
<circle cx="142" cy="102" r="5" fill="#D92B2B"/>
<text x="188" y="145" text-anchor="middle" font-size="9" fill="#007B8A" font-family="Arial,sans-serif">mg/dL</text>
<circle cx="177" cy="196" r="15" fill="#E8EEF5"/>
<circle cx="145" cy="196" r="8" fill="#4A77A8"/><circle cx="209" cy="196" r="8" fill="#4A77A8"/>
<rect x="157" y="258" width="40" height="40" rx="3" fill="#fff" stroke="#C5E2E8"/>
</g></svg>'''


def disclaimer():
    st.info(t('disclaimer'))


def simulator(m, key='sim'):
    import numpy as np
    import plotly.express as px
    from utils.data_loader import ROOT
    from utils.threshold import threshold_table, choose_threshold
    st.subheader('Explore the decision threshold')
    st.write('The threshold is the point where the app changes its testing suggestion. Lowering it usually catches more positive survey labels but also flags more negative ones. Your score stays the same.')
    st.caption('Illustrative relative penalty units only — these are not actual medical costs. Defaults: false alarm 1, missed positive label 5.')
    a, b = st.columns(2)
    cfp = a.number_input('Penalty for a false alarm (FP)', min_value=0., max_value=1000., value=1., step=1., key=key + 'fp')
    cfn = b.number_input('Penalty for a missed positive label (FN)', min_value=0., max_value=1000., value=5., step=1., key=key + 'fn')
    if cfp + cfn == 0:
        st.warning('Give at least one error a positive penalty.')
        return
    with np.load(ROOT / 'models/validation_predictions.npz') as saved:
        best, table = choose_threshold(threshold_table(saved['y'], saved['p']), cfp, cfn)
    label = 'No alerts' if best.threshold > 1 else f'{best.threshold:.1%}'
    a, b, c = st.columns(3)
    a.metric('Cost-selected threshold', label)
    b.metric('Validation penalty / person', f'{best.cost_per_person:.3f}')
    c.metric('Total validation penalty', f'{best.total_cost:,.0f}')
    chosen = st.slider('Try a threshold yourself', 0., 1., min(float(best.threshold), 1.), .01, key=key + 'threshold')
    with np.load(ROOT / 'models/validation_predictions.npz') as saved:
        y, p = saved['y'], saved['p']
        pred = p >= chosen
        tp = int(((y == 1) & pred).sum())
        fp = int(((y == 0) & pred).sum())
        fn = int(((y == 1) & ~pred).sum())
        tn = int(((y == 0) & ~pred).sum())
    precision = tp / (tp + fp) if tp + fp else 0.
    recall = tp / (tp + fn)
    f1 = 2 * tp / (2 * tp + fp + fn)
    st.dataframe([dict(Threshold=chosen, FP=fp, FN=fn, Precision=precision, Recall=recall, F1=f1, FPR=fp / (fp + tn), FDR=fp / (tp + fp) if tp + fp else None, Penalty=cfp * fp + cfn * fn)], hide_index=True)
    plot = table[table.threshold <= 1].sort_values('threshold')
    plot = plot.iloc[::max(1, len(plot) // 600)]
    fig = px.line(plot, x='threshold', y=['recall', 'precision', 'FPR'], labels={'value': 'Rate', 'variable': 'Measure'}, color_discrete_sequence=['#007B8A', '#0B3C6D', '#D92B2B'])
    fig.add_vline(x=chosen, line_dash='dot')
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(plot, x='threshold', y='cost_per_person', labels={'cost_per_person': 'Validation penalty per person'}, color_discrete_sequence=['#007B8A'])
    fig.add_vline(x=min(float(best.threshold), 1.), line_dash='dot')
    st.plotly_chart(fig, use_container_width=True)
    if 'probability' in st.session_state:
        p = st.session_state.probability
        st.info(f'Your score stays {p:.1%}. At your trial threshold {chosen:.1%}: ' + ('the model flags your answers for a testing discussion.' if p >= chosen else 'the model does not flag your answers; this does not rule out diabetes.'))
    if st.button('Use cost-selected threshold for my results', key=key + 'apply'):
        st.session_state.active_threshold = float(best.threshold)
        st.session_state.active_costs = {'FP': cfp, 'FN': cfn}
        st.success('Saved for this session. Return to My Results to see the updated decision.')
