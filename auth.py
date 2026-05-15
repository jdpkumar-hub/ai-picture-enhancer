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
# SEND OTP LOGIN
# =====================================================

def send_otp_login(email):

    return supabase.auth.sign_in_with_otp({

        "email": email
    })


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