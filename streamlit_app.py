import streamlit as st
import json
import os
import uuid
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Чек-лист Конструктор",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "checklists.json"

# ─────────────────────────────────────────
#  THEMES
# ─────────────────────────────────────────
THEMES = {
    "☀️ Светлая": {
        "stripe1": "#f0f0f0",
        "stripe2": "#ffffff",
        "card_bg": "#ffffff",
        "card_border": "#e0e0e0",
        "text": "#1a1a2e",
        "subtext": "#666666",
        "input_bg": "#f8f8f8",
        "input_border": "#d0d0d0",
        "sidebar_bg": "#f5f5f5",
        "hover": "#f0f0ff",
        "shadow": "rgba(0,0,0,0.08)",
    },
    "🌙 Тёмная": {
        "stripe1": "#2a2a2a",
        "stripe2": "#1a1a1a",
        "card_bg": "#2d2d2d",
        "card_border": "#444444",
        "text": "#f0f0f0",
        "subtext": "#aaaaaa",
        "input_bg": "#3a3a3a",
        "input_border": "#555555",
        "sidebar_bg": "#242424",
        "hover": "#3a3a4a",
        "shadow": "rgba(0,0,0,0.3)",
    },
    "💙 Синяя": {
        "stripe1": "#e8f0ff",
        "stripe2": "#f5f8ff",
        "card_bg": "#ffffff",
        "card_border": "#b8d0ff",
        "text": "#1a2a5e",
        "subtext": "#4a6aa0",
        "input_bg": "#f0f5ff",
        "input_border": "#99bbff",
        "sidebar_bg": "#e0ecff",
        "hover": "#ddeeff",
        "shadow": "rgba(100,130,255,0.12)",
    },
    "💚 Зелёная": {
        "stripe1": "#e8f5e9",
        "stripe2": "#f5fbf5",
        "card_bg": "#ffffff",
        "card_border": "#b8ddb8",
        "text": "#1a3a1a",
        "subtext": "#4a7a4a",
        "input_bg": "#f0faf0",
        "input_border": "#99cc99",
        "sidebar_bg": "#e0f0e0",
        "hover": "#ddf0dd",
        "shadow": "rgba(50,160,50,0.10)",
    },
}

# ─────────────────────────────────────────
#  DATA HELPERS
# ─────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def new_id():
    return str(uuid.uuid4())[:8]

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if "checklists" not in st.session_state:
    st.session_state.checklists = load_data()
if "active_id" not in st.session_state:
    st.session_state.active_id = None
if "theme" not in st.session_state:
    st.session_state.theme = "☀️ Светлая"
if "copy_done" not in st.session_state:
    st.session_state.copy_done = {}

def persist():
    save_data(st.session_state.checklists)

# ─────────────────────────────────────────
#  CSS INJECTION
# ─────────────────────────────────────────
def inject_css(t):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Global Reset ── */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Nunito', sans-serif !important;
    }}

    /* ── Striped background ── */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {t['stripe1']};
        background-image: repeating-linear-gradient(
            45deg,
            {t['stripe2']} 0px,
            {t['stripe2']} 12px,
            {t['stripe1']} 12px,
            {t['stripe1']} 24px
        );
        min-height: 100vh;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {t['sidebar_bg']} !important;
        border-right: 2px solid {t['card_border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {t['text']} !important;
    }}

    /* ── Cards ── */
    .cl-card {{
        background: {t['card_bg']};
        border: 1.5px solid {t['card_border']};
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow: 0 4px 24px {t['shadow']};
        transition: box-shadow 0.2s ease, transform 0.15s ease;
    }}
    .cl-card:hover {{
        box-shadow: 0 8px 32px {t['shadow']};
        transform: translateY(-2px);
    }}

    /* ── Avatar ── */
    .avatar {{
        width: 80px; height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 36px;
        margin: 0 auto 16px auto;
        box-shadow: 0 4px 20px rgba(102,126,234,0.4);
    }}

    /* ── Typography ── */
    .cl-title {{
        color: {t['text']};
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }}
    .cl-subtitle {{
        color: {t['subtext']};
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 28px;
    }}
    .cl-name {{
        color: {t['text']};
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 4px;
    }}
    .cl-meta {{
        color: {t['subtext']};
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 16px;
    }}

    /* ── Progress bar ── */
    .progress-wrap {{
        background: {t['input_bg']};
        border-radius: 20px;
        height: 14px;
        overflow: hidden;
        margin: 10px 0 18px 0;
        border: 1px solid {t['card_border']};
    }}
    .progress-fill {{
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.4s cubic-bezier(.4,0,.2,1);
    }}
    .progress-label {{
        color: {t['subtext']};
        font-size: 0.82rem;
        font-weight: 700;
        text-align: right;
        margin-bottom: 2px;
    }}

    /* ── Checklist item ── */
    .item-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 14px;
        margin-bottom: 6px;
        background: {t['input_bg']};
        border: 1px solid {t['input_border']};
        transition: background 0.15s;
    }}
    .item-row:hover {{
        background: {t['hover']};
    }}
    .item-text {{
        color: {t['text']};
        font-size: 0.97rem;
        font-weight: 600;
        flex: 1;
    }}
    .item-text.done {{
        text-decoration: line-through;
        opacity: 0.5;
    }}

    /* ── Buttons ── */
    div.stButton > button {{
        border-radius: 30px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer;
    }}
    div.stButton > button:hover {{
        transform: translateY(-1px) !important;
        filter: brightness(1.08) !important;
    }}
    div.stButton > button:active {{
        transform: translateY(0px) !important;
    }}

    /* ── Sidebar list item ── */
    .sidebar-item {{
        padding: 10px 14px;
        border-radius: 14px;
        margin-bottom: 6px;
        cursor: pointer;
        border: 1.5px solid transparent;
        transition: all 0.15s;
        background: {t['card_bg']};
        border-color: {t['card_border']};
        color: {t['text']};
        font-weight: 700;
        font-size: 0.92rem;
    }}
    .sidebar-item.active {{
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border-color: #667eea;
        color: #667eea;
    }}

    /* ── Inputs ── */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {{
        border-radius: 14px !important;
        background: {t['input_bg']} !important;
        border: 1.5px solid {t['input_border']} !important;
        color: {t['text']} !important;
        font-family: 'Nunito', sans-serif !important;
    }}

    /* ── Checkbox ── */
    [data-testid="stCheckbox"] {{
        accent-color: #667eea;
    }}
    [data-testid="stCheckbox"] label span {{
        color: {t['text']} !important;
        font-weight: 600;
    }}

    /* ── Section header ── */
    .section-header {{
        color: {t['subtext']};
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 20px 0 10px 0;
        padding-left: 4px;
    }}

    /* ── Badge ── */
    .badge {{
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 2px 10px;
        border-radius: 20px;
        margin-left: 8px;
    }}

    /* ── Copy success ── */
    .copy-success {{
        color: #28a745;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 6px 12px;
        background: #e8f5e9;
        border-radius: 10px;
        display: inline-block;
    }}

    /* ── Divider ── */
    hr {{
        border: none;
        border-top: 1.5px solid {t['card_border']};
        margin: 20px 0;
    }}

    /* ── Hide Streamlit branding ── */
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{padding-top: 2rem;}}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Avatar + title
        st.markdown('<div class="avatar">📝</div>', unsafe_allow_html=True)
        st.markdown('<div class="cl-title" style="font-size:1.4rem;margin-bottom:2px;">Конструктор</div>', unsafe_allow_html=True)
        st.markdown('<div class="cl-subtitle" style="font-size:0.8rem;margin-bottom:16px;">чек-листов</div>', unsafe_allow_html=True)

        # Theme selector
        st.markdown('<div class="section-header">🎨 Тема</div>', unsafe_allow_html=True)
        theme_choice = st.selectbox(
            "Тема", list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.theme),
            label_visibility="collapsed"
        )
        if theme_choice != st.session_state.theme:
            st.session_state.theme = theme_choice
            st.rerun()

        st.markdown("---")

        # New checklist
        st.markdown('<div class="section-header">➕ Новый чек-лист</div>', unsafe_allow_html=True)
        new_name = st.text_input("Название", placeholder="Например: Покупки 🛒", label_visibility="collapsed")
        if st.button("✨ Создать чек-лист", use_container_width=True):
            if new_name.strip():
                cid = new_id()
                st.session_state.checklists[cid] = {
                    "name": new_name.strip(),
                    "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "items": []
                }
                st.session_state.active_id = cid
                persist()
                st.rerun()
            else:
                st.warning("Введите название!")

        st.markdown("---")

        # List of checklists
        cl = st.session_state.checklists
        if cl:
            st.markdown('<div class="section-header">📋 Мои списки</div>', unsafe_allow_html=True)
            for cid, data in cl.items():
                total = len(data["items"])
                done = sum(1 for i in data["items"] if i.get("done"))
                label = f"{data['name']}"
                badge = f"  {done}/{total}" if total else ""
                active = cid == st.session_state.active_id
                btn_style = "primary" if active else "secondary"
                if st.button(f"{label}{badge}", key=f"sel_{cid}", use_container_width=True, type=btn_style):
                    st.session_state.active_id = cid
                    st.rerun()
        else:
            st.markdown(f'<div style="color:#999;font-size:0.85rem;padding:10px 0;">Нет чек-листов. Создайте первый!</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────
def render_main():
    t = THEMES[st.session_state.theme]
    cl = st.session_state.checklists
    active_id = st.session_state.active_id

    # Hero if nothing selected
    if not active_id or active_id not in cl:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:60vh;">
            <div class="avatar" style="width:100px;height:100px;font-size:48px;margin-bottom:24px;">📝</div>
            <div class="cl-title">Чек-лист Конструктор</div>
            <div class="cl-subtitle">Создайте первый список в боковой панели →</div>
        </div>
        """, unsafe_allow_html=True)
        return

    data = cl[active_id]
    items = data["items"]
    total = len(items)
    done_count = sum(1 for i in items if i.get("done"))
    pct = int(done_count / total * 100) if total else 0

    # ── Header card ──
    st.markdown(f"""
    <div class="cl-card">
        <div class="cl-name">{data['name']}</div>
        <div class="cl-meta">📅 Создан: {data['created']} &nbsp;|&nbsp; 📦 Пунктов: {total}</div>
        <div class="progress-label">{done_count} из {total} выполнено &nbsp; {pct}%</div>
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Action buttons ──
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        # Rename
        new_title = st.text_input("Переименовать", value=data["name"], label_visibility="collapsed")
        if new_title.strip() and new_title.strip() != data["name"]:
            data["name"] = new_title.strip()
            persist()
            st.rerun()
    with col2:
        if st.button("🔄 Сбросить все отметки", use_container_width=True):
            for item in items:
                item["done"] = False
            persist()
            st.rerun()
    with col3:
        if st.button("🗑️ Удалить чек-лист", use_container_width=True):
            del cl[active_id]
            st.session_state.active_id = None
            persist()
            st.rerun()

    st.markdown("---")

    # ── Add item ──
    st.markdown('<div class="section-header">➕ Добавить пункт</div>', unsafe_allow_html=True)
    a1, a2 = st.columns([4, 1])
    with a1:
        new_item = st.text_input("Новый пункт", placeholder="Что нужно сделать?", label_visibility="collapsed", key="new_item_input")
    with a2:
        if st.button("＋ Добавить", use_container_width=True):
            if new_item.strip():
                items.append({"id": new_id(), "text": new_item.strip(), "done": False})
                persist()
                st.rerun()
            else:
                st.warning("Введите текст!")

    st.markdown("---")

    # ── Items ──
    if not items:
        st.markdown(f'<div style="color:{t["subtext"]};text-align:center;padding:30px 0;font-size:1rem;">Список пуст. Добавьте первый пункт ☝️</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-header">📋 Пункты списка</div>', unsafe_allow_html=True)

        # Filter tabs
        filter_mode = st.radio(
            "Фильтр", ["Все", "Активные", "Выполненные"],
            horizontal=True, label_visibility="collapsed"
        )

        filtered = items
        if filter_mode == "Активные":
            filtered = [i for i in items if not i.get("done")]
        elif filter_mode == "Выполненные":
            filtered = [i for i in items if i.get("done")]

        if not filtered:
            st.markdown(f'<div style="color:{t["subtext"]};text-align:center;padding:20px 0;">Пусто в этой категории</div>', unsafe_allow_html=True)

        for idx, item in enumerate(items):
            if filter_mode == "Активные" and item.get("done"):
                continue
            if filter_mode == "Выполненные" and not item.get("done"):
                continue

            c1, c2, c3 = st.columns([0.7, 5, 1])
            with c1:
                checked = st.checkbox(
                    "", value=item.get("done", False),
                    key=f"chk_{item['id']}"
                )
                if checked != item.get("done"):
                    item["done"] = checked
                    persist()
                    st.rerun()
            with c2:
                strike = "line-through; opacity:0.5" if item.get("done") else "none"
                st.markdown(
                    f'<div class="item-row" style="margin-bottom:0;">'
                    f'<span class="item-text" style="text-decoration:{strike};">{item["text"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with c3:
                if st.button("✕", key=f"del_{item['id']}", help="Удалить пункт"):
                    items.remove(item)
                    persist()
                    st.rerun()

    # ── Copy as text ──
    if items:
        st.markdown("---")
        st.markdown('<div class="section-header">📤 Экспорт</div>', unsafe_allow_html=True)
        text_export = f"✅ {data['name']}\n" + "\n".join(
            f"{'[x]' if i.get('done') else '[ ]'} {i['text']}" for i in items
        )
        st.code(text_export, language=None)
        st.caption("Скопируйте текст выше — это ваш чек-лист в текстовом формате")

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    t = THEMES[st.session_state.theme]
    inject_css(t)
    render_sidebar()
    render_main()

if __name__ == "__main__":
    main()
