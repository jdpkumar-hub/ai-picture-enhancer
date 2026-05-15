import streamlit as st
from supabase import create_client, Client

# =====================================================
# SUPABASE CONNECTION
# =====================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================================
# SEND EMAIL OTP
# =====================================================

def send_otp(email):

    try:

        supabase.auth.sign_in_with_otp({
            "email": email
        })

        return True

    except Exception as e:

        raise Exception(str(e))

# =====================================================
# VERIFY OTP
# =====================================================

def verify_otp(email, otp):

    try:

        response = supabase.auth.verify_otp({
            "email": email,
            "token": otp,
            "type": "email"
        })

        return response

    except Exception as e:

        raise Exception(str(e))

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

        raise Exception(str(e))

# =====================================================
# GET CURRENT USER
# =====================================================

def get_user():

    try:

        response = supabase.auth.get_user()

        if response and response.user:
            return response.user

        return None

    except:

        return None

# =====================================================
# LOGOUT
# =====================================================

def logout():

    try:

        supabase.auth.sign_out()

    except:

        pass