import streamlit as st
from supabase import create_client

# ======================================================
# SUPABASE
# ======================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ======================================================
# IMPORTANT
# ======================================================

REDIRECT_URL = "https://ai-enhancer.streamlit.app"

# ======================================================
# LOGIN
# ======================================================

def login(email, password):

    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

# ======================================================
# SIGNUP
# ======================================================

def signup(email, password):

    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

# ======================================================
# GOOGLE LOGIN
# ======================================================

def google_login():

    try:

        oauth = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": REDIRECT_URL
            }
        })

        return oauth.url

    except Exception:
        return None

# ======================================================
# RESET PASSWORD
# ======================================================

def reset_password(email):

    return supabase.auth.reset_password_email(
        email,
        {
            "redirect_to": REDIRECT_URL
        }
    )

# ======================================================
# GET USER
# ======================================================

def get_user():

    try:

        session = supabase.auth.get_session()

        if session and session.user:
            return session.user

        return None

    except Exception:
        return None

# ======================================================
# LOGOUT
# ======================================================

def logout():

    try:
        supabase.auth.sign_out()

    except Exception:
        pass