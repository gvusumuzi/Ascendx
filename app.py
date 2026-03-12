import streamlit as st

# --------------------------------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# --------------------------------------------------
st.set_page_config(page_title="AscendX", layout="wide")

# --------------------------------------------------
# SESSION STATE
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
st.markdown(
    """
<style>

html, body {
    background-color: #f7f7fb;
    font-family: "Inter", sans-serif;
}

/* HEADER */
.header {
    position: sticky;
    top: 0;
    z-index: 999;
    background: white;
    padding: 12px 24px;
    border-bottom: 1px solid #e5e7eb;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 700;
}

.logo-badge {
    background: #6B4C7A;
    color: white;
    padding: 6px 10px;
    border-radius: 10px;
}

/* NAV */
.nav-bar {
    display: flex;
    gap: 14px;
    justify-content: center;
}

.nav-html-btn {
    padding: 10px 16px;
    border-radius: 10px;
    background: white;
    border: 1px solid #d1d5db;
    font-weight: 600;
    color: #6B4C7A;
    text-decoration: none;
}

.nav-html-btn:hover {
    background: #6B4C7A;
    color: white;
}

/* HERO */
.hero-container {
    max-width: 900px;
    margin: auto;
    text-align: center;
    padding: 80px 20px;
}

.hero-title {
    font-size: 56px;
    font-weight: 800;
}

.connect { color:#111827; }
.mentor { color:#6f4aa6; }
.grow { color:#f28c6b; }

.hero-subtitle {
    font-size: 18px;
    color: #4b5563;
    max-width: 720px;
    margin: 20px auto;
}

.btn-link {
    display:block;
    text-decoration:none;
    padding:14px;
    border-radius:12px;
    margin-top:12px;
}

.btn-primary {
    background:#6f4aa6;
    color:white;
}

.btn-secondary {
    border:2px solid #f28c6b;
    color:#f28c6b;
}

</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("<div class='header'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 6, 3])

with col1:
    st.markdown(
        """
        <div class="logo">
        <div class="logo-badge">✨</div>
        AscendX
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
<div class="nav-bar">
<a class="nav-html-btn" href="?page=home">Home</a>
<a class="nav-html-btn" href="?page=mentors">Find Mentors</a>
<a class="nav-html-btn" href="?page=clients">Find Clients</a>
<a class="nav-html-btn" href="?page=login">Sign In</a>
<a class="nav-html-btn" href="?page=signup">Sign Up</a>
</div>
""",
        unsafe_allow_html=True,
    )

with col3:
    if st.session_state.user:
        st.write(f"👤 {st.session_state.user['name']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
if st.session_state.page == "home":

    st.markdown(
        """
<div class="hero-container">

<div class="hero-title">
<span class="connect">Connect.</span>
<span class="mentor"> Mentor.</span><br>
<span class="grow">Grow Together.</span>
</div>

<p class="hero-subtitle">
Find mentors who share your business interests, discover clients near you,
and build meaningful connections with fellow women entrepreneurs.
</p>

<a href="?page=mentors" class="btn-link btn-primary">
Find a Mentor
</a>

<a href="?page=clients" class="btn-link btn-secondary">
Find Clients
</a>

</div>
""",
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# MENTORS PAGE
# --------------------------------------------------
elif st.session_state.page == "mentors":

    st.title("👩‍🏫 Mentors")

    st.info("Mentor discovery feature coming soon.")

# --------------------------------------------------
# CLIENTS PAGE
# --------------------------------------------------
elif st.session_state.page == "clients":

    st.title("🧑‍💼 Clients")

    st.info("Client search feature coming soon.")

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------
elif st.session_state.page == "login":

    st.title("🔐 Sign In")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):

        if email and password:
            st.session_state.user = {
                "name": email.split("@")[0],
                "email": email,
                "role": "User",
            }

            st.success("Logged in successfully")
            st.session_state.page = "home"
            st.rerun()

        else:
            st.error("Enter email and password")

# --------------------------------------------------
# SIGNUP PAGE
# --------------------------------------------------
elif st.session_state.page == "signup":

    st.title("📝 Create an Account")

    with st.form("signup_form"):

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        role = st.selectbox("I am a:", ["Mentor", "Client"])
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Create Account")

        if submitted:

            if name and email and password:

                st.session_state.user = {
                    "name": name,
                    "email": email,
                    "role": role,
                }

                st.success("🎉 Account created successfully!")

                st.session_state.page = "home"
                st.rerun()

            else:
                st.error("Please fill in all fields.")
