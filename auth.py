import streamlit as st
from supabase import create_client, Client

# =====================================================
# SUPABASE
# =====================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================================
# LOGIN
# =====================================================

def login(email, password):

    return supabase.auth.sign_in_with_password({

        "email": email,
        "password": password

    })

# =====================================================
# SIGNUP
# =====================================================

def signup(email, password):

    return supabase.auth.sign_up({

        "email": email,
        "password": password

    })

# =====================================================
# RESET PASSWORD
# =====================================================

def reset_password(email):

    return supabase.auth.reset_password_email(
        email,
        {
            "redirect_to":
            "https://ai-enhancer.streamlit.app/?type=recovery"
        }
    )

# =====================================================
# GOOGLE LOGIN
# =====================================================

def google_login():

    try:

        redirect_url = "https://ai-enhancer.streamlit.app"

        response = supabase.auth.sign_in_with_oauth({

            "provider": "google",

            "options": {
                "redirect_to": redirect_url
            }

        })

        return response.url

    except Exception as e:

        st.error(str(e))

        return None

# =====================================================
# GET USER
# =====================================================

def get_user():

    try:

        user = supabase.auth.get_user()

        if user:
            return user.user

        return None

    except:
        return None

# =====================================================
# LOGOUT
# =====================================================

def logout():

    supabase.auth.sign_out()