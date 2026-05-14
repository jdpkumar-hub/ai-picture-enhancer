from supabase import create_client
import streamlit as st

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ---------- LOGIN ----------
def login(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

# ---------- SIGNUP ----------
def signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

# ---------- RESET PASSWORD ----------
def reset_password(email):
    return supabase.auth.reset_password_email(
        email,
        {
            "redirect_to": "https://wequqsbvhydvugifevhm.supabase.co/auth/v1/verify"
        }
    )