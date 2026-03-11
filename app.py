import streamlit as st
import sqlite3
import hashlib
import re
st.markdown("""
<style>
/* Remove default Streamlit padding */
.block-container {
    padding-top: 2rem;
}

/* Hero wrapper */
.hero-container {
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
    padding: 80px 20px 60px 20px;
}

/* Pill */
.hero-pill {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 999px;
    background: #f3e9ff;
    color: #6f4aa6;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 28px;
}

/* Title */
.hero-title {
    font-size: 56px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 28px;
}

.connect { color: #111827; }
.mentor { color: #6f4aa6; }
.grow { color: #f28c6b; }

/* Subtitle */
.hero-subtitle {
    font-size: 18px;
    color: #4b5563;
    max-width: 720px;
    margin: 0 auto 50px auto;
    line-height: 1.6;
}

/* Buttons */
.cta-wrapper {
    max-width: 420px;
    margin: 0 auto;
}

.primary-btn button,
.secondary-btn button {
    width: 100%;
    padding: 14px 24px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 12px;
}

/* Primary */
.primary-btn button {
    background-color: #6f4aa6;
    color: white;
    border: none;
}

/* Secondary */
.secondary-btn button {
    background-color: transparent;
    color: #f28c6b;
    border: 2px solid #f28c6b;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.home-hero {
    min-height: 75vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(
        circle at top,
        rgba(243, 232, 255, 0.6),
        rgba(255, 255, 255, 1) 60%
    );
}

.home-hero-inner {
    max-width: 900px;
    text-align: center;
    padding: 40px 20px;
}

.home-title {
    font-size: 64px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 20px;
}

.home-title .dark { color: #111827; }
.home-title .purple { color: #6B4C7A; }
.home-title .peach { color: #F09A7A; }

.home-subtitle {
    font-size: 18px;
    color: #6b7280;
    max-width: 720px;
    margin: 0 auto 40px auto;
    line-height: 1.6;
}

.home-actions {
    display: flex;
    justify-content: center;
    gap: 24px;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="AscendX", layout="wide")
# --------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------

def init_db():
    conn = sqlite3.connect("ascendx.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()
# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = None


# --------------------------------------------------
# URL PAGE HANDLING
# --------------------------------------------------
query_params = st.query_params

if "page" in query_params:
    st.session_state.page = query_params["page"][0]

# --------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------
st.markdown("""
<style>

/* ================================
   GLOBAL
================================ */
html, body {
    background-color: #f7f7fb;
    font-family: "Inter", sans-serif;
}

/* ================================
   HEADER BAR
================================ */
.header {
    position: sticky;
    top: 0;
    z-index: 999;
    background: white;
    padding: 12px 24px;
    border-bottom: 1px solid #e5e7eb;
}

/* ================================
   LOGO
================================ */
.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}

.logo-badge {
    background: #6B4C7A;
    color: white;
    padding: 6px 10px;
    border-radius: 10px;
    font-size: 14px;
}

/* ================================
   NAV BAR (MATCH HOME BUTTONS)
================================ */
.nav-bar {
    display: flex;
    gap: 14px;
    justify-content: center;
}

/* Same style as Home CTA */
.nav-html-btn {
    min-width: 160px;
    height: 48px;
    border-radius: 14px;

    background: white;
    border: 1px solid #d1d5db;

    font-size: 14px;
    font-weight: 600;
    color: #6B4C7A;

    cursor: pointer;
    transition: all 0.2s ease-in-out;
}

/* Hover */
.nav-html-btn:hover {
    background: #6B4C7A;
    color: white;
    border-color: #6B4C7A;
}

/* ================================
   USER INFO
================================ */
.user-info {
    text-align: right;
    font-size: 14px;
    color: #111827;
}

.user-info span {
    font-size: 12px;
    color: #6b7280;
}

/* ================================
   HERO
================================ */
.hero {
    padding: 80px 20px;
    text-align: center;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
}

.hero span {
    color: #6B4C7A;
}

.hero p {
    margin-top: 12px;
    font-size: 17px;
    color: #6b7280;
}

/* ================================
   CTA BUTTONS
================================ */
.cta-btn {
    min-width: 220px;
    height: 52px;
    border-radius: 16px;
    font-size: 15px;
    font-weight: 700;
    border: none;
    cursor: pointer;
}

.cta-primary {
    background: #6B4C7A;
    color: white;
}

.cta-outline {
    background: white;
    border: 1px solid #6B4C7A;
    color: #6B4C7A;
}

.cta-primary:hover {
    background: #5a3e66;
}

.cta-outline:hover {
    background: #6B4C7A;
    color: white;
}

/* ================================
   CARDS
================================ */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 35px rgba(0,0,0,0.08);
}
/* ================================
   HOME HERO (NEW)
================================ */
.home-hero {
    min-height: 75vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(
        circle at top,
        rgba(243, 232, 255, 0.6),
        rgba(255, 255, 255, 1) 60%
    );
}

.home-hero-inner {
    max-width: 900px;
    text-align: center;
    padding: 40px 20px;
}

.home-title {
    font-size: 64px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 20px;
}

.home-title .dark {
    color: #111827;
}

.home-title .purple {
    color: #6B4C7A;
}

.home-title .peach {
    color: #F09A7A;
}

.home-subtitle {
    font-size: 18px;
    color: #6b7280;
    max-width: 720px;
    margin: 0 auto 40px auto;
    line-height: 1.6;
}

.home-actions {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER NAVIGATION
# --------------------------------------------------
st.markdown("<div class='header'>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([3, 6, 3])

    # LOGO
    with col1:
        st.markdown("""
        <div class="logo">
            <div class="logo-badge">✨</div>
            AscendX
        </div>
        """, unsafe_allow_html=True)

    # NAV BUTTONS (WORKING)
    with col2:
        st.markdown("""
        <div class="nav-bar">
      <a class="nav-html-btn" href="?page=home">Home</a>
    <a class="nav-html-btn" href="?page=mentors">Find Mentors</a>
    <a class="nav-html-btn" href="?page=clients">Find Clients</a>
    <a class="nav-html-btn" href="?page=login">Sign In</a>
    <a class="nav-html-btn" href="?page=signup">Sign Up</a>
        </div>
        """, unsafe_allow_html=True)

    # USER INFO
    with col3:
        if st.session_state.user:
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.page = "home"
        st.rerun()

    st.markdown(
        f"""
        <div class="user-info">
            👤 <strong>{st.session_state.user['name']}</strong><br>
            <span>{st.session_state.user['role']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
            st.markdown(
                f"""
                <div class="user-info">
                    👤 <strong>{st.session_state.user['name']}</strong><br>
                    <span>{st.session_state.user['role']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)
st.write("")

# --------------------------------------------------
# PAGE: MENTORS
# --------------------------------------------------
if st.session_state.page == "mentors":
    st.markdown("## 👩‍🏫 Mentors")
    st.info("Mentors page coming next.")

# --------------------------------------------------
# PAGE: CLIENTS
# --------------------------------------------------
if st.session_state.page == "clients":
    st.markdown("## 🧑‍💼 Clients")
    st.info("Clients page coming next.")

# --------------------------------------------------
# PAGE: LOGIN
# --------------------------------------------------
# --------------------------------------------------
# PAGE: LOGIN
# --------------------------------------------------
if st.session_state.page == "login":

    st.markdown("""
    <div class="card" style="max-width:500px;margin:auto;">
        <h2 style="text-align:center;">🔐 Sign In</h2>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Sign In")

        if submitted:
            conn = sqlite3.connect("ascendx.db")
            c = conn.cursor()

            c.execute(
                "SELECT name, role, password FROM users WHERE email = ?",
                (email,)
            )
            user = c.fetchone()
            conn.close()

            if user and user[2] == hash_password(password):
                st.session_state.user = {
                    "name": user[0],
                    "role": user[1],
                    "email": email
                }

                st.success("Welcome back!")
                st.session_state.page = "home"
                st.rerun()

            else:
                st.error("Invalid email or password.")

# --------------------------------------------------
# PAGE: HOME
# --------------------------------------------------
if st.session_state.page == "home":

    st.html("""
    <style>
    .btn-link {
        display: block;
        width: 100%;
        text-align: center;
        text-decoration: none;
        padding: 14px 24px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
    }
    {
# PAGE: SIGN UP
# --------------------------------------------------
if st.session_state.page == "signup":

    st.markdown("""
    <div class="card" style="max-width:500px;margin:auto;">
        <h2 style="text-align:center;">📝 Create Account</h2>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        role = st.selectbox("I am a:", ["Mentor", "Client"])
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Create Account")

        if submitted:

            if not name or not email or not password:
                st.error("All fields are required.")
            
            elif not valid_email(email):
                st.error("Please enter a valid email address.")
            
            else:
                conn = sqlite3.connect("ascendx.db")
                c = conn.cursor()

                try:
                    c.execute(
                        "INSERT INTO users (name, email, role, password) VALUES (?, ?, ?, ?)",
                        (name, email, role, hash_password(password))
                    )
                    conn.commit()

                    st.success("🎉 Account created successfully!")
                    st.session_state.page = "login"
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Email already exists. Please sign in.")

                conn.close()
    .btn-primary {
        background-color: #6f4aa6;
        color: white;
        border: none;
    }

    .btn-secondary {
        background-color: transparent;
        color: #f28c6b;
        border: 2px solid #f28c6b;
    }
    </style>

    <div class="hero-container">

        <div class="hero-pill">
            ✨ Empowering Women in Business
        </div>

        <div class="hero-title">
            <span class="connect">Connect.</span>
            <span class="mentor"> Mentor.</span><br>
            <span class="grow">Grow Together.</span>
        </div>

        <p class="hero-subtitle">
            Find mentors who share your business interests, discover clients near you,
            and build meaningful connections with fellow women entrepreneurs.
        </p>

        <div class="cta-wrapper">

            <a href="?page=mentors" class="btn-link btn-primary">
                Find a Mentor
            </a>

            <div style="height:14px;"></div>

            <a href="?page=clients" class="btn-link btn-secondary">
                Find Clients
            </a>

        </div>

    </div>
    """)
