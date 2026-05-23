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
if "mode" not in st.session_state:
    st.session_state.mode = "home"

def persist():
    save_data(st.session_state.checklists)

# ─────────────────────────────────────────
#  CSS  (тёмная тема, фиксированная)
# ─────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap');

    html, body, * { font-family: 'Nunito', sans-serif !important; }

    /* Страница */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main {
        background: #111111 !important;
    }

    /* Скрыть сайдбар */
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"] { display: none !important; }

    /* Центральный блок */
    .block-container {
        max-width: 680px !important;
        padding: 2rem 1rem 3rem !important;
    }

    /* ═══ ГЛАВНАЯ КАРТОЧКА ═══ */
    .main-card {
        background-color: #2a2a2a;
        background-image: repeating-linear-gradient(
            45deg,
            #303030 0px, #303030 14px,
            #2a2a2a 14px, #2a2a2a 28px
        );
        border-radius: 32px;
        padding: 36px 36px 40px;
        box-shadow: 0 12px 60px rgba(0,0,0,0.5);
    }

    /* Шапка */
    .card-logo {
        display: flex; align-items: center; gap: 10px;
        font-size: 1rem; font-weight: 900; color: #f0f0f0;
        margin-bottom: 0;
    }
    .logo-circle {
        width: 36px; height: 36px; border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex; align-items: center; justify-content: center;
        font-size: 17px; flex-shrink: 0;
    }

    /* Hero */
    .big-avatar {
        width: 84px; height: 84px; border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex; align-items: center; justify-content: center;
        font-size: 38px; margin: 0 auto 16px;
        box-shadow: 0 6px 28px rgba(102,126,234,0.45);
    }
    .hero-title {
        color: #f0f0f0;
        font-size: 2.2rem; font-weight: 900;
        letter-spacing: -0.5px; margin-bottom: 6px;
        text-align: center;
    }
    .hero-sub {
        color: #aaaaaa;
        font-size: 0.95rem; text-align: center;
    }

    /* Section label */
    .sec-label {
        color: #888888;
        font-size: 0.7rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: 1.8px;
        margin: 18px 0 8px;
    }

    /* Типографика */
    .cl-name { color: #f0f0f0; font-size: 1.45rem; font-weight: 900; margin-bottom: 4px; }
    .cl-meta {
        color: #aaaaaa; font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace !important;
        margin-bottom: 14px;
    }

    /* Прогресс */
    .progress-label {
        color: #aaaaaa; font-size: 0.8rem; font-weight: 700;
        text-align: right; margin-bottom: 4px;
    }
    .progress-wrap {
        background: #3a3a3a; border-radius: 20px;
        height: 14px; overflow: hidden;
    }
    .progress-fill {
        height: 100%; border-radius: 20px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.4s cubic-bezier(.4,0,.2,1);
    }

    /* Пункты */
    .item-row {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 14px; border-radius: 12px; margin-bottom: 6px;
        background: #383838; border: 1px solid #4a4a4a;
    }
    .item-text { color: #f0f0f0; font-size: 0.96rem; font-weight: 600; }

    /* Разделитель */
    .divider {
        border: none; border-top: 1.5px solid #3a3a3a; margin: 18px 0;
    }

    /* Кнопки */
    div.stButton > button {
        border-radius: 30px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.2s !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        filter: brightness(1.1) !important;
    }

    /* Инпуты */
    [data-testid="stTextInput"] input {
        border-radius: 12px !important;
        background: #383838 !important;
        border: 1.5px solid #4a4a4a !important;
        color: #f0f0f0 !important;
        font-weight: 600 !important;
    }
    [data-testid="stTextInput"] input::placeholder { color: #888888 !important; }

    /* Radio / Checkbox */
    [data-testid="stRadio"] label span,
    [data-testid="stCheckbox"] label span { color: #f0f0f0 !important; font-weight: 600; }

    /* Code */
    [data-testid="stCode"] { border-radius: 12px !important; }

    /* Все тексты */
    p, span, label, div { color: #f0f0f0; }
    .stAlert p { color: #f0f0f0 !important; }

    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def card_open():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

def sec(label):
    st.markdown(f'<div class="sec-label">{label}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────
def render_home():
    card_open()

    st.markdown('<div class="card-logo"><div class="logo-circle">📝</div> Чек-лист Конструктор</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:32px 0 24px;">
        <div class="big-avatar">📝</div>
        <div class="hero-title">Чек-лист Конструктор</div>
        <div class="hero-sub">Создавайте списки, отслеживайте прогресс</div>
    </div>
    """, unsafe_allow_html=True)

    divider()
    sec("➕ Новый чек-лист")

    new_name = st.text_input("", placeholder="Название, например: Покупки 🛒",
                             label_visibility="collapsed", key="home_new_name")
    if st.button("✨ Создать чек-лист", use_container_width=True, type="primary"):
        if new_name.strip():
            cid = new_id()
            st.session_state.checklists[cid] = {
                "name": new_name.strip(),
                "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "items": []
            }
            st.session_state.active_id = cid
            st.session_state.mode = "editor"
            persist()
            st.rerun()
        else:
            st.warning("Введите название!")

    cl = st.session_state.checklists
    if cl:
        divider()
        sec("📋 Мои чек-листы")
        for cid, data in cl.items():
            total = len(data["items"])
            done = sum(1 for i in data["items"] if i.get("done"))
            pct = int(done / total * 100) if total else 0

            ci, cb1, cb2 = st.columns([4, 1.4, 1.4])
            with ci:
                st.markdown(f"""
                <div style="padding:4px 0;">
                  <div style="font-size:1rem;font-weight:800;color:#f0f0f0;">{data['name']}</div>
                  <div style="font-size:0.76rem;color:#aaaaaa;">{done}/{total} выполнено · {pct}%</div>
                </div>""", unsafe_allow_html=True)
            with cb1:
                if st.button("👁 Открыть", key=f"view_{cid}", use_container_width=True):
                    st.session_state.active_id = cid
                    st.session_state.mode = "view"
                    st.rerun()
            with cb2:
                if st.button("✏️ Редакт.", key=f"edit_{cid}", use_container_width=True):
                    st.session_state.active_id = cid
                    st.session_state.mode = "editor"
                    st.rerun()

            st.markdown(f"""
            <div style="margin:-4px 0 14px;">
              <div class="progress-wrap">
                <div class="progress-fill" style="width:{pct}%;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    card_close()

# ─────────────────────────────────────────
#  EDITOR
# ─────────────────────────────────────────
def render_editor():
    cl = st.session_state.checklists
    cid = st.session_state.active_id
    if not cid or cid not in cl:
        st.session_state.mode = "home"
        st.rerun()
        return
    data = cl[cid]

    card_open()

    st.markdown('<div class="card-logo"><div class="logo-circle">📝</div> Редактор</div>',
                unsafe_allow_html=True)

    if st.button("← Назад", key="editor_back"):
        st.session_state.mode = "home"
        st.rerun()

    divider()
    sec("📝 Название чек-листа")
    new_title = st.text_input("", value=data["name"],
                              label_visibility="collapsed", key="editor_title")
    if new_title.strip() and new_title.strip() != data["name"]:
        data["name"] = new_title.strip()
        persist()

    divider()
    sec("➕ Добавить пункт")

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        new_item_text = st.text_input("", placeholder="Что нужно сделать?",
                                     label_visibility="collapsed", key="editor_new_item")
    with col_btn:
        if st.button("＋", key="editor_add_btn", use_container_width=True):
            if new_item_text.strip():
                data["items"].append({"id": new_id(), "text": new_item_text.strip(), "done": False})
                persist()
                st.rerun()

    items = data["items"]
    if items:
        divider()
        sec(f"📋 Пункты ({len(items)})")
        for idx, item in enumerate(items):
            c1, c2 = st.columns([6, 0.7])
            with c1:
                edited = st.text_input("", value=item["text"],
                                       label_visibility="collapsed",
                                       key=f"edit_item_{item['id']}")
                if edited.strip() and edited.strip() != item["text"]:
                    item["text"] = edited.strip()
                    persist()
            with c2:
                st.write("")
                if st.button("✕", key=f"editor_del_{item['id']}"):
                    items.pop(idx)
                    persist()
                    st.rerun()
    else:
        st.markdown('<div style="color:#888;text-align:center;padding:16px 0;">Добавьте первый пункт ☝️</div>',
                    unsafe_allow_html=True)

    divider()
    col_save, col_del = st.columns([3, 1])
    with col_save:
        if st.button("💾 Сохранить и открыть", use_container_width=True, type="primary"):
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

    card_close()

# ─────────────────────────────────────────
#  VIEW
# ─────────────────────────────────────────
def render_view():
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

    card_open()

    st.markdown('<div class="card-logo"><div class="logo-circle">📝</div> Чек-лист</div>',
                unsafe_allow_html=True)

    if st.button("← Назад", key="view_back"):
        st.session_state.mode = "home"
        st.rerun()

    divider()

    st.markdown(f'<div class="cl-name">{data["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cl-meta">📅 {data["created"]} &nbsp;|&nbsp; 📦 {total} пунктов</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="progress-label">{done_count} из {total} выполнено · {pct}%</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="progress-wrap" style="margin-bottom:16px;">
        <div class="progress-fill" style="width:{pct}%;"></div>
    </div>""", unsafe_allow_html=True)

    divider()
    sec("📋 Пункты")

    filter_mode = st.radio("", ["Все", "Активные", "Выполненные"],
                           horizontal=True, label_visibility="collapsed", key="view_filter")

    if not items:
        st.markdown('<div style="color:#888;text-align:center;padding:20px 0;">Список пуст</div>',
                    unsafe_allow_html=True)
    else:
        for item in items:
            if filter_mode == "Активные" and item.get("done"):
                continue
            if filter_mode == "Выполненные" and not item.get("done"):
                continue
            c1, c2 = st.columns([0.5, 6])
            with c1:
                checked = st.checkbox("", value=item.get("done", False),
                                      key=f"view_chk_{item['id']}")
                if checked != item.get("done"):
                    item["done"] = checked
                    persist()
                    st.rerun()
            with c2:
                strike = "line-through;opacity:0.4" if item.get("done") else "none"
                st.markdown(
                    f'<div class="item-row"><span class="item-text" '
                    f'style="text-decoration:{strike};">{item["text"]}</span></div>',
                    unsafe_allow_html=True)

    divider()
    if st.button("🔄 Сбросить все отметки", use_container_width=False):
        for item in items:
            item["done"] = False
        persist()
        st.rerun()

    if items:
        divider()
        sec("📤 Экспорт текстом")
        text_export = f"✅ {data['name']}\n" + "\n".join(
            f"{'[x]' if i.get('done') else '[ ]'} {i['text']}" for i in items
        )
        st.code(text_export, language=None)

    divider()
    if st.button("✏️ Редактировать чек-лист", use_container_width=True):
        st.session_state.mode = "editor"
        st.rerun()

    card_close()

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    inject_css()
    mode = st.session_state.mode
    if mode == "home":
        render_home()
    elif mode == "editor":
        render_editor()
    elif mode == "view":
        render_view()

if __name__ == "__main__":
    main()
