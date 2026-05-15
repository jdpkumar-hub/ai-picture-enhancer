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

        redirect_url = "https://ai-enhancer.streamlit.app"

        response = supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {
                    "redirect_to": redirect_url
                }
            }
        )

        return response.url

    except Exception as e:

        st.error(f"Google login error: {str(e)}")
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

        response = supabase.auth.get_user()

        if response and response.user:
            return response.user

        return None

    except:
        return None

# ======================================================
# LOGOUT
# ======================================================

def logout():

    try:
        supabase.auth.sign_out()

    except Exception:
        pass