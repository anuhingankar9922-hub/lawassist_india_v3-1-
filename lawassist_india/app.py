"""LawAssist India - multilingual legal information assistant (Streamlit).

Run:  streamlit run app.py
"""
import html as _html
import io
import os
import re
from datetime import date, datetime

import streamlit as st

from src import constants as C
from src.analyzer import analyze
from src.chunking import build_chunks_for_document
from src.knowledge_base import COMPLIANCE, TOPICS, TOPIC_BY_ID
from src.lawyer_directory import filter_lawyers, get_unique, load_lawyers
from src.letters import LETTERS, render_letter
from src.pdf_utils import extract_pages_from_pdf
from src.retrieval import DocumentIndex, TopicIndex, best_sentences
from src.sos_data import EMERGENCY_NUMBERS, get_localized_numbers
from src.tools import DATE_LABELS, DEADLINE_KINDS, FEE_SLABS, FORUM_NAMES, consumer_fee, deadlines
from src.ui_text import ABOUT_FEATURES, ABOUT_HOW, EXAMPLES, QL, T

BASE = os.path.dirname(os.path.abspath(__file__))
esc = _html.escape

st.set_page_config(page_title="LawAssist India", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")


def H(s: str):
    """Render an HTML snippet (newlines collapsed so markdown never turns it into a code block)."""
    st.markdown(re.sub(r"\s*\n\s*", " ", s).strip(), unsafe_allow_html=True)


# --------------------------------------------------------------------------- state
ss = st.session_state
ss.setdefault("lang", "en")
ss.setdefault("fs", "A")
ss.setdefault("doc_index", DocumentIndex())
ss.setdefault("analyses", {})
ss.setdefault("chat", [])
ss.setdefault("uploader_ver", 0)
ss.setdefault("feedback", {})

# --------------------------------------------------------------------------- styling
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Noto+Sans:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Noto+Serif+Devanagari:wght@600;700&display=swap');
:root { --paper:@@PAPER@@; --surface:@@SURFACE@@; --ink:@@INK@@; --muted:@@MUTED@@; --rule:@@RULE@@; --maroon:@@MAROON@@; --maroon-d:@@MAROON_DARK@@; --brass:@@BRASS@@; --green:@@GREEN@@;
  --serif:'Source Serif 4','Noto Serif Devanagari',Georgia,serif; --sans:'Noto Sans','Noto Sans Devanagari','Segoe UI',system-ui,sans-serif; }
html { font-size: @@FS@@px !important; }
html, body, .stApp, .stMarkdown, p, li, label, input, textarea, button, [data-baseweb="select"], [data-baseweb="tab"] { font-family: var(--sans); }
[data-testid="stIconMaterial"], .material-icons, [class*="material-symbols"] { font-family: 'Material Symbols Rounded' !important; }
.stApp { background: var(--paper); color: var(--ink); }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stDecoration"], [data-testid="stHeader"], header { display:none !important; }
.block-container { max-width: 1120px; padding: 0.8rem 1.2rem 3rem; }
p, li { line-height: 1.6; }
a { color: var(--maroon); }

/* ---------- top bar ---------- */
.topbar { display:flex; align-items:center; gap:.7rem; padding:.2rem 0 .1rem; }
.mono { width:2.5rem; height:2.5rem; background:var(--maroon); color:#fff; border-radius:6px; display:flex; align-items:center; justify-content:center; font-family:var(--serif); font-weight:700; font-size:1.05rem; letter-spacing:.5px; flex:none; }
.brand { font-family:var(--serif); font-size:1.55rem; font-weight:700; color:var(--ink); line-height:1.05; }
.brand em { font-style:normal; color:var(--maroon); }
.ctl-label { font-size:.85rem; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; margin-bottom:.15rem; }

/* ---------- hero ---------- */
.hero { padding: 1.7rem 0 1.4rem; border-bottom: 2px solid var(--ink); margin-bottom: 0; }
.eyebrow { font-size:.88rem; font-weight:700; letter-spacing:.09em; text-transform:uppercase; color:var(--maroon); margin-bottom:.55rem; }
.hero h1 { font-family:var(--serif); font-size:2.7rem; line-height:1.1; font-weight:700; color:var(--ink); margin:0 0 .7rem; padding:0; letter-spacing:-.01em; }
.hero p { font-size:1.12rem; line-height:1.6; color:#363F4B; max-width:46rem; margin:0; }
.facts { display:flex; flex-wrap:wrap; gap:0; margin-top:1.2rem; }
.facts div { padding:0 1.3rem 0 0; margin-right:1.3rem; border-right:1px solid var(--rule); font-size:.95rem; color:var(--muted); }
.facts div:last-child { border-right:none; }
.facts b { font-family:var(--serif); font-size:1.6rem; color:var(--maroon); margin-right:.3rem; }
.notice { font-size:.98rem; line-height:1.55; color:#4A3B1B; background:#F3EAD3; border-left:4px solid var(--brass); padding:.65rem .95rem; margin:1rem 0 .4rem; border-radius:0 4px 4px 0; }
.notice b { color:#5B3F08; }

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap:.2rem; border-bottom:1px solid var(--rule); flex-wrap:wrap; }
.stTabs [data-baseweb="tab"] { height:auto; padding:.7rem .95rem; background:transparent; }
.stTabs [data-baseweb="tab"] p { font-size:1.1rem; font-weight:600; color:var(--muted); }
.stTabs [aria-selected="true"] p { color:var(--maroon); }
.stTabs [data-baseweb="tab-highlight"] { background-color:var(--maroon); height:3px; }
.stTabs [data-baseweb="tab-border"] { display:none; }

/* ---------- typography ---------- */
.sec-title { font-family:var(--serif); font-size:1.85rem; font-weight:700; color:var(--ink); margin:.9rem 0 .15rem; line-height:1.2; }
.sec-sub { font-size:1rem; color:var(--muted); margin-bottom:1rem; line-height:1.55; }
.label { font-size:.88rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--maroon); margin:1.1rem 0 .4rem; }

/* ---------- cards ---------- */
.card { background:var(--surface); border:1px solid var(--rule); border-radius:6px; padding:1.2rem 1.35rem; }
.card + .card { margin-top:.8rem; }
.ans-title { font-family:var(--serif); font-size:1.5rem; font-weight:700; color:var(--ink); line-height:1.25; margin:0 0 .2rem; }
.tag { display:inline-block; font-size:.92rem; font-weight:600; padding:.15rem .6rem; border-radius:3px; background:#F1ECE0; color:#4A4132; border:1px solid var(--rule); margin:.2rem .35rem .2rem 0; }
.plain { font-size:1.05rem; line-height:1.65; color:var(--ink); background:#FBF8F1; border-left:4px solid var(--brass); padding:.8rem 1rem; border-radius:0 4px 4px 0; }
ol.steps { list-style:none; counter-reset:s; margin:.2rem 0 0; padding:0; }
ol.steps li { counter-increment:s; position:relative; padding:.35rem 0 .55rem 2.4rem; font-size:1.02rem; line-height:1.6; }
ol.steps li:before { content:counter(s); position:absolute; left:0; top:.3rem; width:1.7rem; height:1.7rem; border-radius:4px; background:var(--maroon); color:#fff; font-family:var(--serif); font-weight:700; font-size:.95rem; display:flex; align-items:center; justify-content:center; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
@media (max-width:760px) { .two { grid-template-columns:1fr; } .hero h1 { font-size:2rem; } }
.box { background:#FBF8F1; border:1px solid var(--rule); border-radius:4px; padding:.7rem .95rem; font-size:1rem; line-height:1.55; }
.box ul { margin:0; padding-left:1.15rem; }
.help { margin-top:1rem; font-size:.95rem; font-weight:600; color:var(--green); border-top:1px dashed var(--rule); padding-top:.7rem; }

.hit { border:1px solid var(--rule); border-left:4px solid var(--maroon); background:#fff; border-radius:0 6px 6px 0; padding:.85rem 1.05rem; margin-top:.7rem; }
.hit-h { font-size:.92rem; font-weight:700; color:var(--maroon); margin-bottom:.35rem; }
.hit-b { font-size:1rem; line-height:1.65; }
.hit-b mark { background:#F6E3A8; padding:0 .15rem; }

.empty { color:var(--muted); font-size:1.05rem; line-height:1.6; padding:1rem 0; }

/* ---------- risk / flags ---------- */
.risk { border:1px solid; border-left-width:6px; border-radius:4px; padding:.8rem 1rem; font-weight:600; font-size:1.05rem; }
.risk small { display:block; font-weight:500; font-size:.88rem; opacity:.85; margin-top:.15rem; }
.risk.high { background:#FBEAE8; border-color:#E4B4AE; color:#8C1D14; border-left-color:#B3261E; }
.risk.medium { background:#FBF1DC; border-color:#E8CF9B; color:#704A06; border-left-color:#C98A12; }
.risk.low { background:#E6F1EA; border-color:#B5D3C1; color:#1E5238; border-left-color:var(--green); }
.stat { background:#fff; border:1px solid var(--rule); border-radius:4px; padding:.65rem .9rem; }
.stat b { display:block; font-family:var(--serif); font-size:1.9rem; color:var(--maroon); line-height:1.1; }
.stat span { font-size:.85rem; color:var(--muted); font-weight:700; letter-spacing:.05em; text-transform:uppercase; }
.flag { background:#fff; border:1px solid var(--rule); border-left-width:5px; border-radius:0 4px 4px 0; padding:.7rem .95rem; margin-bottom:.6rem; font-size:1rem; line-height:1.55; }
.flag.high { border-left-color:#B3261E; } .flag.medium { border-left-color:#C98A12; } .flag.low { border-left-color:#4F6D8F; }
.sev { font-size:.75rem; font-weight:800; letter-spacing:.07em; padding:.1rem .45rem; border-radius:3px; margin-right:.5rem; color:#fff; }
.sev.high { background:#B3261E; } .sev.medium { background:#C98A12; } .sev.low { background:#4F6D8F; }
.flag .q { font-size:.95rem; color:var(--muted); margin-top:.4rem; font-style:italic; }
.jg { display:grid; grid-template-columns: 11rem 1fr; gap:.45rem 1rem; font-size:.98rem; }
.jg .t { font-weight:700; color:var(--ink); }
@media (max-width:760px) { .jg { grid-template-columns:1fr; } }

/* ---------- letters / tools ---------- */
.paper { background:#fff; border:1px solid var(--rule); box-shadow:0 1px 0 var(--rule), 0 6px 0 -3px #fff, 0 7px 0 -3px var(--rule); padding:1.6rem 1.8rem; font-family:'Source Serif 4','Noto Serif Devanagari',Georgia,serif; font-size:1.02rem; line-height:1.7; color:#222; }
.dl { display:flex; align-items:center; gap:1rem; background:#fff; border:1px solid var(--rule); border-radius:4px; padding:.75rem 1rem; margin-bottom:.55rem; }
.dl .when { min-width:9.5rem; font-family:var(--serif); font-weight:700; font-size:1.2rem; color:var(--ink); }
.dl .what { flex:1; font-size:1rem; line-height:1.45; }
.dl .what small { display:block; color:var(--muted); font-size:.95rem; margin-top:.1rem; }
.dl .left { font-size:.85rem; font-weight:700; padding:.2rem .55rem; border-radius:3px; white-space:nowrap; }
.left.ok { background:#E6F1EA; color:#1E5238; } .left.soon { background:#FBF1DC; color:#704A06; } .left.past { background:#FBEAE8; color:#8C1D14; }
@media (max-width:760px) { .dl { flex-wrap:wrap; } .dl .when { min-width:100%; } }
.big-result { background:#fff; border:1px solid var(--rule); border-left:6px solid var(--maroon); border-radius:4px; padding:1rem 1.2rem; }
.big-result .k { font-size:.8rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--muted); }
.big-result .v { font-family:var(--serif); font-size:1.9rem; font-weight:700; color:var(--ink); line-height:1.2; }

/* ---------- lawyers ---------- */
.lawyer { display:flex; gap:1rem; }
.avatar { width:3.2rem; height:3.2rem; border-radius:6px; flex:none; background:#EFE6D2; color:var(--maroon); border:1px solid var(--rule); display:flex; align-items:center; justify-content:center; font-family:var(--serif); font-weight:700; font-size:1.15rem; }
.lname { font-family:var(--serif); font-size:1.2rem; font-weight:700; color:var(--ink); }
.lmeta { font-size:.98rem; color:var(--muted); margin:.1rem 0 .4rem; }
.callbtn { display:inline-block; text-decoration:none !important; background:var(--maroon); color:#fff !important; font-weight:600; font-size:.95rem; padding:.45rem .95rem; border-radius:4px; margin-top:.5rem; }
.callbtn:hover { background:var(--maroon-d); }
.callbtn.alt { background:#fff; color:var(--maroon) !important; border:1px solid var(--maroon); }

/* ---------- emergency ---------- */
.sosbanner { background:#B3261E; color:#fff; padding:1rem 1.3rem; border-radius:4px; font-family:var(--serif); font-size:1.5rem; font-weight:700; }
.sosgrid { display:grid; grid-template-columns:repeat(auto-fill,minmax(19rem,1fr)); gap:.8rem; margin-top:1rem; }
.sos { display:flex; align-items:center; gap:.9rem; background:#fff; border:1px solid var(--rule); border-radius:4px; padding:.75rem 1rem; text-decoration:none !important; color:var(--ink) !important; }
.sos:hover { border-color:#B3261E; background:#FFF8F7; }
.sos.prio { border:2px solid #B3261E; }
.sos .num { font-family:var(--serif); font-size:1.7rem; font-weight:700; color:#B3261E; min-width:4.6rem; }
.sos .nm { font-weight:700; font-size:1.02rem; line-height:1.25; }
.sos .ds { font-size:.95rem; color:var(--muted); margin-top:.1rem; line-height:1.35; }

/* ---------- streamlit widgets ---------- */
.stButton > button, .stDownloadButton > button { border-radius:4px; font-size:1rem; font-weight:600; min-height:2.6rem; }
[data-testid="stBaseButton-primary"] { background:var(--maroon) !important; color:#fff !important; border:1px solid var(--maroon) !important; }
[data-testid="stBaseButton-primary"]:hover { background:var(--maroon-d) !important; }
[data-testid="stBaseButton-secondary"] { background:#fff; color:var(--ink); border:1px solid #CFC6B3; }
[data-testid="stBaseButton-secondary"]:hover { border-color:var(--maroon); color:var(--maroon); background:#FFFBF5; }
.st-key-quick button, [class*="st-key-quick"] button { justify-content:flex-start !important; min-height:3.4rem; padding-left:1rem; border-left:4px solid var(--maroon); }
.st-key-quick button p, [class*="st-key-quick"] button p { text-align:left; font-family:var(--serif); font-size:1.1rem; font-weight:700; }
.st-key-quick button div, [class*="st-key-quick"] button div { justify-content:flex-start !important; }
[data-testid="stWidgetLabel"] p, label p { font-size:1.02rem !important; font-weight:600; color:var(--ink); }
input, textarea, [data-baseweb="select"] > div, [data-baseweb="select"] div { font-size:1.05rem !important; color:var(--ink) !important; }
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea, [data-testid="stDateInput"] input, [data-testid="stNumberInput"] input { font-size:1.05rem !important; padding-top:.55rem; padding-bottom:.55rem; }
.big-result { margin-bottom:.6rem; }
[data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-baseweb="textarea"], [data-baseweb="base-input"] { background:#fff !important; border-radius:4px !important; border:1px solid #CFC6B3 !important; }
[data-testid="stFileUploaderDropzone"] { background:#fff; border:2px dashed #CFC6B3; border-radius:6px; }
[data-testid="stFileUploaderDropzone"] button { background:#fff; color:var(--ink); border:1px solid #CFC6B3; }
[data-testid="stChatInput"] { border-radius:6px; border:1.5px solid #B9AE97; background:#fff; }
[data-testid="stChatInput"] textarea { font-size:1.05rem !important; }
[data-testid="stChatMessage"] { background:transparent; padding:.4rem 0; }
[data-testid="stChatMessage"] p { font-size:1.05rem; }
[data-testid="stExpander"] { background:#fff; border:1px solid var(--rule) !important; border-radius:6px !important; }
[data-testid="stExpander"] summary p { font-family:var(--serif); font-weight:700; font-size:1.12rem !important; color:var(--ink); }
[data-testid="stSegmentedControl"] button { font-size:.95rem; font-weight:600; }
[data-testid="stCaptionContainer"], .stCaption, [data-testid="stCaptionContainer"] p { font-size:.98rem !important; }
[data-testid="stAlert"] p { font-size:.98rem; }
</style>
"""
for k, v in {"PAPER": C.PAPER, "SURFACE": C.SURFACE, "INK": C.INK, "MUTED": C.MUTED, "RULE": C.RULE, "MAROON": C.MAROON,
             "MAROON_DARK": C.MAROON_DARK, "BRASS": C.BRASS, "GREEN": C.GREEN, "FS": str(C.TEXT_SIZES.get(ss.fs, 18))}.items():
    CSS = CSS.replace(f"@@{k}@@", v)
st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------- cached resources
@st.cache_resource(show_spinner=False)
def get_topic_index():
    return TopicIndex()


@st.cache_data(show_spinner=False)
def get_lawyers():
    return load_lawyers(os.path.join(BASE, "data", "lawyers.json"))


topic_index = get_topic_index()


def tx(d):
    """Pick the current-language value from a {en,hi,mr} dict."""
    return d.get(ss.lang) or d.get("en", "")


# --------------------------------------------------------------------------- top bar
c_brand, c_size, c_lang = st.columns([3.2, 1.3, 2.4], vertical_alignment="bottom")
with c_brand:
    H('<div class="topbar"><div class="mono">LA</div><div class="brand">Law<em>Assist</em> India</div></div>')
with c_size:
    st.markdown(f'<div class="ctl-label">{esc(T(ss.lang, "text_size"))}</div>', unsafe_allow_html=True)
    sz = st.segmented_control("size", list(C.TEXT_SIZES), default=ss.fs, selection_mode="single", key="size_pick", label_visibility="collapsed")
    if sz and sz != ss.fs:
        ss.fs = sz
        st.rerun()
with c_lang:
    st.markdown(f'<div class="ctl-label">{esc(T(ss.lang, "language"))} / भाषा</div>', unsafe_allow_html=True)
    picked = st.segmented_control("lang", list(C.LANGS), format_func=C.LANGS.get, default=ss.lang, selection_mode="single",
                                  key="lang_picker", label_visibility="collapsed")
    if picked and picked != ss.lang:    # clicking the active option returns None - keep the current language
        ss.lang = picked
        st.rerun()

lang = ss.lang

H(f"""<div class="hero"><div class="eyebrow">{esc(T(lang, 'hero_eyebrow'))}</div>
<h1>{esc(T(lang, 'hero_title'))}</h1><p>{esc(T(lang, 'hero_sub'))}</p>
<div class="facts"><div><b>{len(TOPICS)}</b>{esc(T(lang, 'metric_topics'))}</div><div><b>3</b>{esc(T(lang, 'metric_langs'))}</div>
<div><b>{len(EMERGENCY_NUMBERS)}</b>{esc(T(lang, 'metric_helplines'))}</div></div></div>""")
H(f"""<div class="notice"><b>{esc(T(lang, 'disclaimer_title'))}.</b> {esc(T(lang, 'disclaimer_text'))}</div>""")


# --------------------------------------------------------------------------- helpers: rendering
def topic_card_html(t, compact=False):
    acts = "".join(f'<span class="tag">{esc(a)}</span>' for a in t["acts"])
    steps = "".join(f"<li>{esc(s)}</li>" for s in tx(t["steps"]))
    docs = "".join(f"<li>{esc(d)}</li>" for d in tx(t["docs"]))
    head = "" if compact else f'<div class="ans-title">{esc(tx(t["title"]))}</div>'
    return f"""<div class="card">{head}
    <div class="label" style="margin-top:{'0' if compact else '.9rem'}">{esc(T(lang, 'ans_acts'))}</div><div>{acts}</div>
    <div class="label">{esc(T(lang, 'ans_simple'))}</div><div class="plain">{esc(tx(t['summary']))}</div>
    <div class="label">{esc(T(lang, 'ans_steps'))}</div><ol class="steps">{steps}</ol>
    <div class="two"><div><div class="label">{esc(T(lang, 'ans_where'))}</div><div class="box">{esc(tx(t['where']))}</div></div>
    <div><div class="label">{esc(T(lang, 'ans_docs'))}</div><div class="box"><ul>{docs}</ul></div></div></div>
    <div class="help">{esc(T(lang, 'ans_helpline'))}</div></div>"""


def compliance_card_html(c, compact=False):
    steps = "".join(f"<li>{esc(s)}</li>" for s in tx(c["steps"]))
    head = "" if compact else f'<div class="ans-title">{esc(tx(c["title"]))}</div>'
    return f"""<div class="card">{head}
    <div class="label" style="margin-top:{'0' if compact else '.9rem'}">{esc(T(lang, 'svc_who'))}</div><div class="plain">{esc(tx(c['who']))}</div>
    <div class="label">{esc(T(lang, 'svc_steps'))}</div><ol class="steps">{steps}</ol>
    <div class="box">{esc(tx(c['note']))}</div>
    <a class="callbtn" href="{esc(c['link'])}" target="_blank" rel="noopener">{esc(T(lang, 'svc_open'))} →</a></div>"""


def strength(score):
    labels = {"en": ("Strong match", "Good match", "Possible match"), "hi": ("मज़बूत मेल", "अच्छा मेल", "संभावित मेल"),
              "mr": ("मजबूत जुळणी", "चांगली जुळणी", "संभाव्य जुळणी")}[lang]
    return labels[0] if score >= 0.35 else labels[1] if score >= 0.2 else labels[2]


def doc_hit_html(hit):
    chunk, score, sents = hit["chunk"], hit["score"], hit["sents"]
    raw = re.sub(r"\s+", " ", chunk["raw_text"])
    pos = raw.find(sents[0]) if sents else -1
    if len(raw) > 620 and pos >= 0:          # show a window around the best sentence
        a = max(0, pos - 160)
        b = min(len(raw), a + 620)
        raw = ("…" if a else "") + raw[a:b] + ("…" if b < len(raw) else "")
    body = esc(raw)
    for s in sents:
        body = body.replace(esc(s), f"<mark>{esc(s)}</mark>", 1)
    return f"""<div class="hit"><div class="hit-h">{esc(chunk['doc_name'])} · {esc(T(lang, 'ans_page'))} {chunk['page_num']} · {esc(strength(score))}</div>
    <div class="hit-b">{body}</div></div>"""


def get_topic(tid, kind):
    return next(c for c in COMPLIANCE if c["id"] == tid) if kind == "compliance" else TOPIC_BY_ID[tid]


def run_query(q, scope):
    """Language-independent answer record (rendered later in the active language)."""
    rec = {"role": "assistant", "q": q, "topics": [], "doc_hits": []}
    if scope != "__kb__" and ss.doc_index.has_chunks():
        for chunk, score in ss.doc_index.search(q, None if scope == "__all__" else scope, k=2):
            rec["doc_hits"].append({"chunk": chunk, "score": score, "sents": best_sentences(chunk["raw_text"], q, 2)})
    if scope in ("__kb__", "__all__"):
        ranked = topic_index.rank(q, k=3)
        if ranked:
            top = ranked[0][1]
            rec["topics"] = [(t["id"], t.get("kind", "law"), s) for t, s in ranked if s >= 0.55 * top]
    return rec


def render_answer(rec, idx):
    if not rec["topics"] and not rec["doc_hits"]:
        H(f'<div class="card"><div class="plain">{esc(T(lang, "ans_none"))}</div></div>')
        return
    if rec["doc_hits"]:
        H(f'<div class="label" style="margin-top:.2rem">{esc(T(lang, "ans_doc_found"))}</div>')
        for hit in rec["doc_hits"]:
            H(doc_hit_html(hit))
    if rec["topics"]:
        tid, kind, _ = rec["topics"][0]
        t = get_topic(tid, kind)
        H(compliance_card_html(t) if kind == "compliance" else topic_card_html(t))
        if len(rec["topics"]) > 1:
            names = "".join(f'<span class="tag">{esc(tx(get_topic(i, k)["title"]))}</span>' for i, k, _ in rec["topics"][1:])
            H(f'<div class="label">{esc(T(lang, "ans_also"))}</div>{names}')
    c1, c2, c3, _sp = st.columns([1.5, 0.4, 0.4, 4])
    if ss.feedback.get(idx):
        c1.caption(T(lang, "feedback_thanks"))
    else:
        c1.caption(T(lang, "feedback_q"))
        if c2.button("👍", key=f"up_{idx}"):
            ss.feedback[idx] = "up"
            st.rerun()
        if c3.button("👎", key=f"dn_{idx}"):
            ss.feedback[idx] = "down"
            st.rerun()


def chat_transcript():
    lines = [f"{C.APP_TITLE} - chat export ({datetime.now():%d %b %Y %H:%M})", ""]
    for m in ss.chat:
        if m["role"] == "user":
            lines.append(f"Q: {m['content']}")
            continue
        for tid, kind, _ in m["topics"][:1]:
            t = get_topic(tid, kind)
            lines.append(f"A: {tx(t['title'])}")
            if kind != "compliance":
                lines.append("   Laws: " + "; ".join(t["acts"]))
                lines += [f"   {i}. {s}" for i, s in enumerate(tx(t["steps"]), 1)]
        for h in m["doc_hits"]:
            lines.append(f"   From {h['chunk']['doc_name']} p.{h['chunk']['page_num']}: " + " ".join(h["sents"]))
        if not m["topics"] and not m["doc_hits"]:
            lines.append("A: (no match found)")
        lines.append("")
    lines.append("Not legal advice. General information only.")
    return "\n".join(lines)


def add_document(name, pages):
    full = "\n\n".join(p["text"] for p in pages)
    ss.doc_index.add_document(name, full, build_chunks_for_document(name, pages))
    ss.analyses[name] = analyze(full)
    ss.active_doc = name


def pick_example(q):
    ss.pending_q = q


def pick_topic(tid):
    ss.pending_topic = tid


def make_docx(text: str) -> bytes:
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st_ = doc.styles["Normal"]
    st_.font.name = "Times New Roman"
    st_.font.size = Pt(12)
    for block in text.split("\n"):
        doc.add_paragraph(block)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def rel_days(d: date):
    n = (d - date.today()).days
    if n > 14:
        return f"{n} {T(lang, 'deadline_left')}", "ok"
    if n > 0:
        return f"{n} {T(lang, 'deadline_left')}", "soon"
    if n == 0:
        return T(lang, "deadline_today"), "soon"
    return f"{-n} {T(lang, 'deadline_over')}", "past"


# --------------------------------------------------------------------------- tabs
tabs = st.tabs([T(lang, k) for k in ("nav_chat", "nav_docs", "nav_tools", "nav_rights", "nav_services", "nav_lawyer", "nav_sos", "nav_about")])
tab_chat, tab_docs, tab_tools, tab_rights, tab_svc, tab_law, tab_sos, tab_about = tabs

# ============================== ASK ==============================
with tab_chat:
    scope = "__kb__"
    if ss.doc_index.has_chunks():
        opts = ["__all__", "__kb__"] + ss.doc_index.doc_names()
        labels = {"__all__": T(lang, "all_docs"), "__kb__": T(lang, "kb_only")}
        scope = st.selectbox(T(lang, "searching_in"), opts, format_func=lambda x: labels.get(x, x), key="scope")

    QUICK = ["rent", "consumer", "fir", "cyber", "labour", "cheque", "dv", "rera"]
    if not ss.chat:
        H(f'<div class="sec-title">{esc(T(lang, "quick_title"))}</div><div class="sec-sub">{esc(T(lang, "quick_sub"))}</div>')
        area = st.container(key="quick")
    else:
        area = st.expander(T(lang, "try_asking"))
    with area:
        cols = st.columns(4 if not ss.chat else 2)
        for i, tid in enumerate(QUICK):
            cols[i % len(cols)].button(QL(lang, tid), key=f"q_{tid}", on_click=pick_topic, args=(tid,), use_container_width=True)

    history = st.container()
    typed = st.chat_input(T(lang, "chat_placeholder"), key="chat_in")
    q = typed or ss.pop("pending_q", None)
    ptopic = ss.pop("pending_topic", None)
    if ptopic:
        ss.chat.append({"role": "user", "content": tx(TOPIC_BY_ID[ptopic]["title"])})
        ss.chat.append({"role": "assistant", "q": ptopic, "topics": [(ptopic, "law", 1.0)], "doc_hits": []})
    elif q and q.strip():
        ss.chat.append({"role": "user", "content": q.strip()})
        ss.chat.append(run_query(q.strip(), scope))

    with history:
        for i, m in enumerate(ss.chat):
            if m["role"] == "user":
                with st.chat_message("user", avatar="🙂"):
                    st.write(m["content"])
            else:
                with st.chat_message("assistant", avatar="⚖️"):
                    render_answer(m, i)

    if ss.chat:
        b1, b2, _ = st.columns([1.2, 1.3, 3])
        if b1.button(T(lang, "clear_chat"), key="clear_chat"):
            ss.chat = []
            ss.feedback = {}
            st.rerun()
        b2.download_button(T(lang, "download_chat"), chat_transcript(), file_name="lawassist_chat.txt", key="dl_chat")
    else:
        H(f'<div class="label">{esc(T(lang, "try_asking"))}</div>')
        for i, qx in enumerate(EXAMPLES[lang][:4]):
            st.button(qx, key=f"ex_{lang}_{i}", on_click=pick_example, args=(qx,))

# ============================== DOCUMENTS ==============================
with tab_docs:
    H(f'<div class="sec-title">{esc(T(lang, "docs_title"))}</div><div class="sec-sub">{esc(T(lang, "docs_sub"))}</div>')
    up_col, paste_col = st.columns(2, gap="large")
    with up_col:
        files = st.file_uploader(T(lang, "upload_label"), type=["pdf", "txt"], accept_multiple_files=True,
                                 key=f"uploader_{ss.uploader_ver}", help=f"Max {C.MAX_UPLOAD_MB} MB")
        st.caption(T(lang, "upload_hint"))
        for f in files or []:
            if ss.doc_index.has_doc(f.name):
                continue
            if f.name.lower().endswith(".txt"):
                text = f.getvalue().decode("utf-8", errors="ignore")
                pages = [{"page_num": 1, "text": text}] if text.strip() else []
            else:
                with st.spinner(f"{f.name} ..."):
                    pages = extract_pages_from_pdf(f)
            if pages:
                add_document(f.name, pages)
                st.toast(f"{f.name} - {T(lang, 'added_ok')}")
            else:
                st.warning(f"{f.name}: {T(lang, 'scan_warn')}")
    with paste_col:
        pasted = st.text_area(T(lang, "paste_label"), height=130, key="paste_text")
        pc1, pc2 = st.columns(2)
        if pc1.button(T(lang, "analyze_btn"), type="primary", key="analyze_paste", use_container_width=True):
            if pasted.strip():
                add_document(f"Pasted text {datetime.now():%H:%M:%S}", [{"page_num": 1, "text": pasted.strip()}])
                st.rerun()
        if pc2.button(T(lang, "sample_btn"), key="sample_btn", use_container_width=True):
            with open(os.path.join(BASE, "data", "sample_rent_agreement.txt"), encoding="utf-8") as fh:
                add_document("Sample rent agreement", [{"page_num": 1, "text": fh.read()}])
            st.rerun()

    names = ss.doc_index.doc_names()
    if not names:
        H(f'<div class="card"><div class="empty">{esc(T(lang, "no_docs"))}</div></div>')
    else:
        sel_col, rm_col = st.columns([4, 1], vertical_alignment="bottom")
        default = ss.get("active_doc") if ss.get("active_doc") in names else names[-1]
        doc = sel_col.selectbox(T(lang, "choose_doc"), names, index=names.index(default), key="doc_select")
        if rm_col.button(T(lang, "remove_doc"), key="rm_doc", use_container_width=True):
            ss.doc_index.remove(doc)
            ss.analyses.pop(doc, None)
            ss.uploader_ver += 1
            ss.pop("active_doc", None)
            st.rerun()
        a = ss.analyses.get(doc) or analyze(ss.doc_index.texts[doc])
        ss.analyses[doc] = a
        n_flags = len(a["flags"])
        r1, r2, r3, r4 = st.columns([2.4, 1, 1, 1])
        with r1:
            H(f"""<div class="risk {a['risk']}">{esc(T(lang, 'risk_level'))}: {esc(T(lang, 'risk_' + a['risk']))}
            <small>{n_flags} {esc(T(lang, 'sec_flags')).lower()}</small></div>""")
        for col, num, lab in ((r2, a["words"], T(lang, "doc_stats")), (r3, n_flags, T(lang, "sec_flags")), (r4, len(a["amounts"]), T(lang, "facts_amounts"))):
            with col:
                H(f'<div class="stat"><b>{num}</b><span>{esc(lab)}</span></div>')

        left, right = st.columns([1.35, 1], gap="large")
        with left:
            H(f'<div class="label">{esc(T(lang, "sec_summary"))}</div>')
            sm = "".join(f"<li>{esc(s)}</li>" for s in a["summary"]) or f"<li>{esc(T(lang, 'none_found'))}</li>"
            H(f'<div class="card"><div class="sec-sub" style="margin-bottom:.3rem">{esc(T(lang, "sec_summary_note"))}</div><ol class="steps">{sm}</ol></div>')
            H(f'<div class="label">{esc(T(lang, "sec_flags"))}</div>')
            if not a["flags"]:
                H(f'<div class="risk low">{esc(T(lang, "no_flags"))}</div>')
            for fl in a["flags"]:
                H(f"""<div class="flag {fl['severity']}"><span class="sev {fl['severity']}">{esc(T(lang, 'sev_' + fl['severity']))}</span>
                {esc(tx(fl['explain']))}<div class="q">{esc(fl['quote'])}</div></div>""")
        with right:
            def facts(label, items):
                body = "".join(f"<li>{esc(i)}</li>" for i in items) or f"<li style='color:{C.MUTED}'>{esc(T(lang, 'none_found'))}</li>"
                return f'<div class="label">{esc(label)}</div><div class="box"><ul>{body}</ul></div>'
            notices = [(n if len(n) <= 150 else n[:150].rsplit(" ", 1)[0] + "…") for n in a["notice"]]
            H('<div class="card">' + f'<div class="ans-title" style="font-size:1.2rem">{esc(T(lang, "sec_facts"))}</div>'
              + facts(T(lang, "facts_amounts"), a["amounts"]) + facts(T(lang, "facts_durations"), a["durations"])
              + facts(T(lang, "facts_dates"), a["dates"]) + facts(T(lang, "facts_notice"), notices) + '</div>')
            if a["jargon"]:
                H(f'<div class="label">{esc(T(lang, "sec_jargon"))}</div>')
                rows = "".join(f'<div class="t">{esc(j["term"])}</div><div>{esc(tx(j["meaning"]))}</div>' for j in a["jargon"])
                H(f'<div class="card"><div class="jg">{rows}</div></div>')
        if a["obligations"]:
            with st.expander(T(lang, "sec_oblig")):
                for o in a["obligations"]:
                    st.markdown(f"- {o}")
        st.info(T(lang, "ask_doc_hint"))
        rep = [f"{C.APP_TITLE} - Document report: {doc}", f"Risk: {a['risk'].upper()}  |  Words: {a['words']}", "", "SUMMARY"]
        rep += [f"- {s}" for s in a["summary"]] + ["", "CLAUSES TO CHECK"]
        rep += [f"- [{f['severity'].upper()}] {f['explain']['en']}  ({f['quote']})" for f in a["flags"]] or ["- none detected"]
        rep += ["", "KEY FACTS", "Amounts: " + ", ".join(a["amounts"]), "Periods: " + ", ".join(a["durations"]), "Dates: " + ", ".join(a["dates"]),
                "", "Not legal advice. Please consult a licensed advocate."]
        st.download_button(T(lang, "download_report"), "\n".join(rep), file_name="lawassist_report.txt", key="dl_report")

# ============================== LETTERS & TOOLS ==============================
with tab_tools:
    H(f'<div class="sec-title">{esc(T(lang, "tools_title"))}</div><div class="sec-sub">{esc(T(lang, "tools_sub"))}</div>')
    tool_opts = ["letter", "deadline", "fee"]
    tool_lbl = {"letter": T(lang, "tool_letter"), "deadline": T(lang, "tool_deadline"), "fee": T(lang, "tool_fee")}
    tool = st.segmented_control("tool", tool_opts, format_func=tool_lbl.get, default="letter", selection_mode="single",
                                key="tool_pick", label_visibility="collapsed") or "letter"

    if tool == "letter":
        lid = st.selectbox(T(lang, "letter_pick"), list(LETTERS), format_func=lambda k: tx(LETTERS[k]["title"]), key="letter_id")
        L = LETTERS[lid]
        st.caption(tx(L["about"]))
        avail = L["langs"]
        if len(avail) > 1:
            out_lang = st.radio(T(lang, "letter_lang"), avail, index=avail.index(lang) if lang in avail else 0,
                                format_func=C.LANGS.get, horizontal=True, key=f"lang_{lid}")
        else:
            out_lang = "en"
            st.caption(T(lang, "letter_only_en"))
        fcol, pcol = st.columns([1, 1.15], gap="large")
        vals = {}
        with fcol:
            H(f'<div class="label" style="margin-top:0">{esc(T(lang, "letter_fill"))}</div>')
            for key, label, kind in L["fields"]:
                wk = f"f_{lid}_{key}"
                if kind == "area":
                    vals[key] = st.text_area(tx(label), key=wk, height=95)
                elif kind == "num":
                    n = st.number_input(tx(label), min_value=0, step=500, key=wk)
                    vals[key] = f"{int(n):,}" if n else ""
                elif kind == "date":
                    d = st.date_input(tx(label), value=date.today(), format="DD/MM/YYYY", key=wk)
                    vals[key] = d.strftime("%d %B %Y")
                else:
                    vals[key] = st.text_input(tx(label), key=wk)
        text = render_letter(lid, out_lang, vals)
        with pcol:
            H(f'<div class="label" style="margin-top:0">{esc(T(lang, "letter_preview"))}</div>')
            H(f'<div class="paper">{esc(text).replace(chr(10), "<br>")}</div>')
            d1, d2 = st.columns(2)
            d1.download_button(T(lang, "letter_dl_docx"), make_docx(text), file_name=f"lawassist_{lid}.docx", key=f"dlw_{lid}",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", type="primary", use_container_width=True)
            d2.download_button(T(lang, "letter_dl_txt"), text, file_name=f"lawassist_{lid}.txt", key=f"dlt_{lid}", use_container_width=True)
            st.caption(T(lang, "letter_note"))

    elif tool == "deadline":
        kind = st.selectbox(T(lang, "deadline_pick"), list(DEADLINE_KINDS), format_func=lambda k: tx(DEADLINE_KINDS[k]), key="dl_kind")
        d0 = st.date_input(tx(DATE_LABELS[kind]), value=date.today(), format="DD/MM/YYYY", key=f"dl_date_{kind}")
        sent = None
        if kind == "cheque":
            if st.checkbox(T(lang, "deadline_notice"), key="dl_sent_chk"):
                sent = st.date_input(" ", value=d0, min_value=d0, format="DD/MM/YYYY", key="dl_sent", label_visibility="collapsed")
        for row in deadlines(kind, d0, sent):
            when, cls = rel_days(row["date"])
            H(f"""<div class="dl"><div class="when">{row['date'].strftime('%d %b %Y')}</div>
            <div class="what">{esc(tx(row['label']))}<small>{esc(tx(row['note']))}</small></div><div class="left {cls}">{esc(when)}</div></div>""")
        st.warning(T(lang, "deadline_warn"))

    else:  # consumer fee
        val = st.number_input(T(lang, "fee_value"), min_value=0, value=300000, step=10000, key="fee_val")
        st.caption(T(lang, "fee_hint"))
        fee, forum = consumer_fee(int(val))
        f1, f2 = st.columns(2)
        with f1:
            H(f'<div class="big-result"><div class="k">{esc(T(lang, "fee_forum"))}</div><div class="v">{esc(tx(FORUM_NAMES[forum]))}</div></div>')
        with f2:
            fee_txt = T(lang, "fee_none") if fee == 0 else f"₹{fee:,}"
            H(f'<div class="big-result"><div class="k">{esc(T(lang, "fee_amount"))}</div><div class="v">{esc(fee_txt)}</div></div>')
        st.caption(T(lang, "fee_note"))
        with st.expander(T(lang, "fee_table")):
            lo = 0
            rows = []
            for limit, f in FEE_SLABS:
                rows.append({"From (₹)": f"{lo:,}", "Up to (₹)": f"{limit:,}", "Fee (₹)": f if f else "0"})
                lo = limit
            rows.append({"From (₹)": f"{lo:,}", "Up to (₹)": "—", "Fee (₹)": 7500})
            st.dataframe(rows, hide_index=True, use_container_width=True)

# ============================== RIGHTS ==============================
with tab_rights:
    H(f'<div class="sec-title">{esc(T(lang, "rights_title"))}</div><div class="sec-sub">{esc(T(lang, "rights_sub"))}</div>')
    term = st.text_input(T(lang, "rights_search"), key="rights_q", placeholder=T(lang, "rights_search")).strip().lower()
    shown = 0
    for t in TOPICS:
        hay = (" ".join(t["title"].values()) + " " + t["keywords"]).lower()
        if term and term not in hay:
            continue
        shown += 1
        with st.expander(tx(t["title"]), expanded=bool(term) and shown == 1):
            H(topic_card_html(t, compact=True))
    if not shown:
        H(f'<div class="card"><div class="empty">{esc(T(lang, "ans_none"))}</div></div>')

# ============================== SERVICES ==============================
with tab_svc:
    H(f'<div class="sec-title">{esc(T(lang, "svc_title"))}</div><div class="sec-sub">{esc(T(lang, "svc_sub"))}</div>')
    for i, c in enumerate(COMPLIANCE):
        with st.expander(tx(c["title"]), expanded=(i == 0)):
            H(compliance_card_html(c, compact=True))

# ============================== LAWYERS ==============================
with tab_law:
    H(f'<div class="sec-title">{esc(T(lang, "law_title"))}</div>')
    st.info(T(lang, "law_demo"))
    lawyers = get_lawyers()
    all_l = T(lang, "f_all")
    f1, f2, f3, f4 = st.columns(4)
    city = f1.selectbox(T(lang, "f_city"), [all_l] + get_unique(lawyers, "city"), key="f_city")
    spec = f2.selectbox(T(lang, "f_spec"), [all_l] + get_unique(lawyers, "specialization"), key="f_spec")
    lg = f3.selectbox(T(lang, "f_lang"), [all_l] + list(C.LANGS), format_func=lambda x: all_l if x == all_l else C.LANGS[x], key="f_lang")
    max_fee = f4.slider(T(lang, "f_fee"), 500, 3000, 3000, step=100, key="f_fee")
    res = filter_lawyers(lawyers, None if city == all_l else city, None if spec == all_l else spec, None if lg == all_l else lg, max_fee)
    st.caption(f"**{len(res)}** {T(lang, 'law_count')}")
    if not res:
        H(f'<div class="card"><div class="empty">{esc(T(lang, "law_none"))}</div></div>')
    cols = st.columns(2)
    for i, l in enumerate(res):
        ini = "".join(w[0] for w in l["name"].replace("Adv. ", "").split()[:2]).upper()
        tags = "".join(f'<span class="tag">{esc(s)}</span>' for s in l["specialization"])
        lgs = " · ".join(C.LANGS[x] for x in l["languages"])
        with cols[i % 2]:
            H(f"""<div class="card" style="margin-bottom:.8rem"><div class="lawyer"><div class="avatar">{esc(ini)}</div><div>
            <div class="lname">{esc(l['name'])}</div>
            <div class="lmeta">{esc(l['city'])}, {esc(l['state'])} · {l['experience']} {esc(T(lang, 'law_exp'))}</div>
            <div>{tags}</div>
            <div class="lmeta" style="margin-top:.4rem">{esc(lgs)} · {esc(T(lang, 'law_fee'))}: <b>₹{l['fees']}</b></div>
            <a class="callbtn" href="tel:{esc(l['phone'])}">{esc(T(lang, 'law_call'))} {esc(l['phone'])}</a></div></div></div>""")

# ============================== EMERGENCY ==============================
with tab_sos:
    H(f'<div class="sec-title">{esc(T(lang, "sos_title"))}</div>')
    H(f'<div class="sosbanner">{esc(T(lang, "sos_alert"))}</div>')
    st.caption(T(lang, "sos_tip"))
    cards = ""
    for it in get_localized_numbers(lang):
        cards += f"""<a class="sos {'prio' if it['prio'] else ''}" href="tel:{it['number']}"><div class="num">{it['number']}</div>
        <div><div class="nm">{esc(it['name'])}</div><div class="ds">{esc(it['desc'])}</div></div></a>"""
    H(f'<div class="sosgrid">{cards}</div>')

# ============================== ABOUT ==============================
with tab_about:
    H(f'<div class="sec-title">{esc(T(lang, "about_title"))}</div>')
    m1, m2, m3, m4 = st.columns(4)
    for col, num, lab in ((m1, len(TOPICS) + len(COMPLIANCE), T(lang, "metric_topics")), (m2, 3, T(lang, "metric_langs")),
                          (m3, len(EMERGENCY_NUMBERS), T(lang, "metric_helplines")), (m4, ss.doc_index.num_docs(), T(lang, "metric_docs"))):
        with col:
            H(f'<div class="stat"><b>{num}</b><span>{esc(lab)}</span></div>')
    H(f'<div class="card" style="margin-top:1rem"><div class="plain">{esc(T(lang, "about_body"))}</div>'
      f'<div class="label">{esc(T(lang, "about_features"))}</div><div class="box"><ul>' + "".join(f"<li>{esc(x)}</li>" for x in ABOUT_FEATURES[lang]) + '</ul></div>'
      f'<div class="label">{esc(T(lang, "about_how"))}</div><div class="box"><ul>' + "".join(f"<li>{esc(x)}</li>" for x in ABOUT_HOW[lang]) + '</ul></div>'
      f'<div class="label">{esc(T(lang, "about_limits"))}</div><div class="box">{esc(T(lang, "about_limits_body"))}</div></div>')

H(f'<div style="margin-top:2.2rem;padding-top:.9rem;border-top:1px solid {C.RULE};font-size:.88rem;color:{C.MUTED}">{esc(C.APP_TITLE)} · {esc(T(lang, "disclaimer_title"))}</div>')
