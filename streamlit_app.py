import streamlit as st
import json
import os
import uuid
from datetime import datetime

st.set_page_config(
    page_title="Чек-лист Конструктор",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = "checklists.json"

# ─────────────────────────────────────────
#  THEMES
# ─────────────────────────────────────────
THEMES = {
    "☀️ Светлая": {
        "stripe1": "#f0f0f0", "stripe2": "#ffffff",
        "card_bg": "#ffffff", "card_border": "#e0e0e0",
        "text": "#1a1a2e", "subtext": "#666666",
        "input_bg": "#f8f8f8", "input_border": "#d0d0d0",
        "nav_bg": "#ffffff", "nav_border": "#e8e8e8",
        "shadow": "rgba(0,0,0,0.08)", "hover": "#f0f0ff",
        "dark": False,
    },
    "🌙 Тёмная": {
        "stripe1": "#2a2a2a", "stripe2": "#1a1a1a",
        "card_bg": "#2d2d2d", "card_border": "#444444",
        "text": "#f0f0f0", "subtext": "#aaaaaa",
        "input_bg": "#3a3a3a", "input_border": "#555555",
        "nav_bg": "#242424", "nav_border": "#3a3a3a",
        "shadow": "rgba(0,0,0,0.3)", "hover": "#3a3a4a",
        "dark": True,
    },
    "💙 Синяя": {
        "stripe1": "#e8f0ff", "stripe2": "#f5f8ff",
        "card_bg": "#ffffff", "card_border": "#b8d0ff",
        "text": "#1a2a5e", "subtext": "#4a6aa0",
        "input_bg": "#f0f5ff", "input_border": "#99bbff",
        "nav_bg": "#ffffff", "nav_border": "#ccdeff",
        "shadow": "rgba(100,130,255,0.12)", "hover": "#ddeeff",
        "dark": False,
    },
    "💚 Зелёная": {
        "stripe1": "#e8f5e9", "stripe2": "#f5fbf5",
        "card_bg": "#ffffff", "card_border": "#b8ddb8",
        "text": "#1a3a1a", "subtext": "#4a7a4a",
        "input_bg": "#f0faf0", "input_border": "#99cc99",
        "nav_bg": "#ffffff", "nav_border": "#c8e8c8",
        "shadow": "rgba(50,160,50,0.10)", "hover": "#ddf0dd",
        "dark": False,
    },
}

# ─────────────────────────────────────────
#  DATA
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
# mode: "home" | "editor" | "view"
if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "draft_items" not in st.session_state:
    st.session_state.draft_items = []

def persist():
    save_data(st.session_state.checklists)

# ─────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────
def inject_css(t):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Nunito', sans-serif !important;
    }}

    /* Hide sidebar toggle and collapse button */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    /* Striped background */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {t['stripe1']};
        background-image: repeating-linear-gradient(
            45deg,
            {t['stripe2']} 0px, {t['stripe2']} 12px,
            {t['stripe1']} 12px, {t['stripe1']} 24px
        );
        min-height: 100vh;
    }}

    /* Center content max-width */
    .block-container {{
        max-width: 720px !important;
        padding: 2rem 1.5rem !important;
    }}

    /* Top nav bar */
    .top-nav {{
        background: {t['nav_bg']};
        border: 1.5px solid {t['nav_border']};
        border-radius: 20px;
        padding: 14px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 28px;
        box-shadow: 0 2px 16px {t['shadow']};
    }}
    .nav-logo {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.1rem;
        font-weight: 900;
        color: {t['text']};
    }}
    .nav-avatar {{
        width: 38px; height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
    }}

    /* Cards */
    .cl-card {{
        background: {t['card_bg']};
        border: 1.5px solid {t['card_border']};
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow: 0 4px 24px {t['shadow']};
    }}

    /* Hero */
    .hero {{
        text-align: center;
        padding: 48px 20px 32px;
    }}
    .big-avatar {{
        width: 90px; height: 90px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 40px;
        margin: 0 auto 20px;
        box-shadow: 0 6px 28px rgba(102,126,234,0.4);
    }}
    .hero-title {{
        color: {t['text']};
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
    }}
    .hero-sub {{
        color: {t['subtext']};
        font-size: 1rem;
        margin-bottom: 32px;
    }}

    /* Section label */
    .sec-label {{
        color: {t['subtext']};
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 20px 0 10px;
    }}

    /* Typography */
    .cl-name {{
        color: {t['text']};
        font-size: 1.5rem;
        font-weight: 900;
        margin-bottom: 4px;
    }}
    .cl-meta {{
        color: {t['subtext']};
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 16px;
    }}

    /* Progress */
    .progress-label {{
        color: {t['subtext']};
        font-size: 0.82rem;
        font-weight: 700;
        text-align: right;
        margin-bottom: 4px;
    }}
    .progress-wrap {{
        background: {t['input_bg']};
        border-radius: 20px;
        height: 16px;
        overflow: hidden;
        border: 1px solid {t['card_border']};
        margin-bottom: 20px;
    }}
    .progress-fill {{
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.4s cubic-bezier(.4,0,.2,1);
    }}

    /* Item rows */
    .item-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 11px 16px;
        border-radius: 14px;
        margin-bottom: 7px;
        background: {t['input_bg']};
        border: 1px solid {t['input_border']};
    }}
    .item-text {{
        color: {t['text']};
        font-size: 0.97rem;
        font-weight: 600;
        flex: 1;
    }}
    .item-text.done {{
        text-decoration: line-through;
        opacity: 0.45;
    }}

    /* Checklist list card on home */
    .cl-list-item {{
        background: {t['card_bg']};
        border: 1.5px solid {t['card_border']};
        border-radius: 16px;
        padding: 14px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px {t['shadow']};
        transition: transform 0.15s;
    }}

    /* Buttons */
    div.stButton > button {{
        border-radius: 30px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.2s !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-1px) !important;
        filter: brightness(1.07) !important;
    }}

    /* Inputs */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {{
        border-radius: 14px !important;
        background: {t['input_bg']} !important;
        border: 1.5px solid {t['input_border']} !important;
        color: {t['text']} !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 600 !important;
    }}

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {{
        border-radius: 14px !important;
        background: {t['input_bg']} !important;
        border: 1.5px solid {t['input_border']} !important;
        color: {t['text']} !important;
    }}

    /* Radio */
    [data-testid="stRadio"] label span {{
        color: {t['text']} !important;
        font-weight: 600;
    }}

    /* Checkbox */
    [data-testid="stCheckbox"] label span {{
        color: {t['text']} !important;
        font-weight: 600;
    }}

    hr {{
        border: none;
        border-top: 1.5px solid {t['card_border']};
        margin: 18px 0;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  NAV BAR
# ─────────────────────────────────────────
def render_nav(t):
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:0;">
            <div style="width:38px;height:38px;border-radius:50%;
                background:linear-gradient(135deg,#667eea,#764ba2);
                display:flex;align-items:center;justify-content:center;font-size:18px;">📝</div>
            <span style="font-size:1.05rem;font-weight:900;color:{t['text']};">Чек-лист Конструктор</span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        theme_choice = st.selectbox(
            "Тема", list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.theme),
            label_visibility="collapsed",
            key="theme_select"
        )
        if theme_choice != st.session_state.theme:
            st.session_state.theme = theme_choice
            st.rerun()

# ─────────────────────────────────────────
#  HOME PAGE
# ─────────────────────────────────────────
def render_home(t):
    # Hero
    st.markdown(f"""
    <div class="hero">
        <div class="big-avatar">📝</div>
        <div class="hero-title">Чек-лист Конструктор</div>
        <div class="hero-sub">Создавайте списки, отслеживайте прогресс</div>
    </div>
    """, unsafe_allow_html=True)

    # Create new
    st.markdown(f'<div class="sec-label">➕ Новый чек-лист</div>', unsafe_allow_html=True)
    with st.container():
        new_name = st.text_input("", placeholder="Название списка, например: Покупки 🛒", label_visibility="collapsed", key="home_new_name")
        if st.button("✨ Создать чек-лист", use_container_width=True, type="primary"):
            if new_name.strip():
                cid = new_id()
                st.session_state.checklists[cid] = {
                    "name": new_name.strip(),
                    "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "items": []
                }
                st.session_state.active_id = cid
                st.session_state.draft_items = []
                st.session_state.mode = "editor"
                persist()
                st.rerun()
            else:
                st.warning("Введите название списка!")

    # Existing checklists
    cl = st.session_state.checklists
    if cl:
        st.markdown(f'<div class="sec-label" style="margin-top:28px;">📋 Мои чек-листы</div>', unsafe_allow_html=True)
        for cid, data in cl.items():
            total = len(data["items"])
            done = sum(1 for i in data["items"] if i.get("done"))
            pct = int(done / total * 100) if total else 0

            col_info, col_btn1, col_btn2 = st.columns([4, 1.3, 1.3])
            with col_info:
                st.markdown(f"""
                <div style="padding:4px 0;">
                    <div style="font-size:1rem;font-weight:800;color:{t['text']};">{data['name']}</div>
                    <div style="font-size:0.78rem;color:{t['subtext']};">{done}/{total} выполнено · {pct}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn1:
                if st.button("👁 Открыть", key=f"view_{cid}", use_container_width=True):
                    st.session_state.active_id = cid
                    st.session_state.mode = "view"
                    st.rerun()
            with col_btn2:
                if st.button("✏️ Редакт.", key=f"edit_{cid}", use_container_width=True):
                    st.session_state.active_id = cid
                    st.session_state.draft_items = [dict(i) for i in data["items"]]
                    st.session_state.mode = "editor"
                    st.rerun()
            st.markdown(f"""
            <div style="margin:-8px 0 12px 0;">
                <div style="background:{t['input_bg']};border-radius:20px;height:6px;overflow:hidden;border:1px solid {t['card_border']};">
                    <div style="width:{pct}%;height:100%;border-radius:20px;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  EDITOR PAGE
# ─────────────────────────────────────────
def render_editor(t):
    cl = st.session_state.checklists
    cid = st.session_state.active_id

    if not cid or cid not in cl:
        st.session_state.mode = "home"
        st.rerun()
        return

    data = cl[cid]

    # Back button
    if st.button("← Назад к списку", key="editor_back"):
        st.session_state.mode = "home"
        st.rerun()

    st.markdown(f'<div class="cl-card">', unsafe_allow_html=True)

    # Title editing
    st.markdown(f'<div class="sec-label">📝 Название чек-листа</div>', unsafe_allow_html=True)
    new_title = st.text_input("", value=data["name"], label_visibility="collapsed", key="editor_title")
    if new_title.strip() and new_title.strip() != data["name"]:
        data["name"] = new_title.strip()
        persist()

    st.markdown("---")

    # Add items
    st.markdown(f'<div class="sec-label">➕ Добавить пункт</div>', unsafe_allow_html=True)
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        new_item_text = st.text_input("", placeholder="Что нужно сделать?", label_visibility="collapsed", key="editor_new_item")
    with col_btn:
        if st.button("＋ Добавить", key="editor_add_btn", use_container_width=True):
            if new_item_text.strip():
                data["items"].append({"id": new_id(), "text": new_item_text.strip(), "done": False})
                persist()
                st.rerun()
            else:
                st.warning("Введите текст!")

    # Current items
    items = data["items"]
    if items:
        st.markdown(f'<div class="sec-label" style="margin-top:16px;">📋 Пункты ({len(items)})</div>', unsafe_allow_html=True)
        for idx, item in enumerate(items):
            c1, c2, c3 = st.columns([5, 1, 0.6])
            with c1:
                edited = st.text_input(
                    "", value=item["text"],
                    label_visibility="collapsed",
                    key=f"edit_item_{item['id']}"
                )
                if edited.strip() and edited.strip() != item["text"]:
                    item["text"] = edited.strip()
                    persist()
            with c2:
                st.write("")
            with c3:
                if st.button("✕", key=f"editor_del_{item['id']}"):
                    items.pop(idx)
                    persist()
                    st.rerun()
    else:
        st.markdown(f'<div style="color:{t["subtext"]};text-align:center;padding:20px 0;font-size:0.95rem;">Пусто — добавьте первый пункт ☝️</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Save button
    col_save, col_del = st.columns([3, 1])
    with col_save:
        if st.button("💾 Сохранить и открыть чек-лист", use_container_width=True, type="primary"):
            persist()
            st.session_state.mode = "view"
            st.rerun()
    with col_del:
        if st.button("🗑️ Удалить", use_container_width=True):
            del cl[cid]
            st.session_state.active_id = None
            persist()
            st.session_state.mode = "home"
            st.rerun()

# ─────────────────────────────────────────
#  VIEW PAGE
# ─────────────────────────────────────────
def render_view(t):
    cl = st.session_state.checklists
    cid = st.session_state.active_id

    if not cid or cid not in cl:
        st.session_state.mode = "home"
        st.rerun()
        return

    data = cl[cid]
    items = data["items"]
    total = len(items)
    done_count = sum(1 for i in items if i.get("done"))
    pct = int(done_count / total * 100) if total else 0

    # Back
    if st.button("← Назад к списку", key="view_back"):
        st.session_state.mode = "home"
        st.rerun()

    # Header card
    st.markdown(f"""
    <div class="cl-card">
        <div class="cl-name">{data['name']}</div>
        <div class="cl-meta">📅 {data['created']} &nbsp;|&nbsp; 📦 {total} пунктов</div>
        <div class="progress-label">{done_count} из {total} выполнено &nbsp;·&nbsp; {pct}%</div>
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter
    st.markdown(f'<div class="sec-label">📋 Пункты</div>', unsafe_allow_html=True)
    filter_mode = st.radio(
        "", ["Все", "Активные", "Выполненные"],
        horizontal=True, label_visibility="collapsed", key="view_filter"
    )

    if not items:
        st.markdown(f'<div style="color:{t["subtext"]};text-align:center;padding:24px;">Список пуст</div>', unsafe_allow_html=True)
    else:
        for item in items:
            if filter_mode == "Активные" and item.get("done"):
                continue
            if filter_mode == "Выполненные" and not item.get("done"):
                continue

            c1, c2 = st.columns([0.6, 6])
            with c1:
                checked = st.checkbox("", value=item.get("done", False), key=f"view_chk_{item['id']}")
                if checked != item.get("done"):
                    item["done"] = checked
                    persist()
                    st.rerun()
            with c2:
                strike = "line-through;opacity:0.45" if item.get("done") else "none"
                st.markdown(
                    f'<div class="item-row"><span class="item-text" style="text-decoration:{strike};">{item["text"]}</span></div>',
                    unsafe_allow_html=True
                )

    # Reset
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Сбросить все отметки", use_container_width=True):
            for item in items:
                item["done"] = False
            persist()
            st.rerun()

    # Export
    if items:
        st.markdown("---")
        st.markdown(f'<div class="sec-label">📤 Экспорт текстом</div>', unsafe_allow_html=True)
        text_export = f"✅ {data['name']}\n" + "\n".join(
            f"{'[x]' if i.get('done') else '[ ]'} {i['text']}" for i in items
        )
        st.code(text_export, language=None)

    st.markdown("<br>", unsafe_allow_html=True)

    # Edit button at the bottom
    st.markdown("---")
    if st.button("✏️ Редактировать чек-лист", use_container_width=True):
        st.session_state.mode = "editor"
        st.rerun()

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    t = THEMES[st.session_state.theme]
    inject_css(t)
    render_nav(t)

    mode = st.session_state.mode
    if mode == "home":
        render_home(t)
    elif mode == "editor":
        render_editor(t)
    elif mode == "view":
        render_view(t)

if __name__ == "__main__":
    main()
