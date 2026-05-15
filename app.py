import streamlit as st
from PIL import Image
from auth import login, signup, reset_password
from enhance import clean_product_image, enhance_photo
from ai_restore import restore_face
from storage import upload_image, save_history, get_history
import io

st.set_page_config(page_title="AI Image Cleaner", layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1 {
    text-align: center;
}
.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #00C9A7);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Product Image Cleaner")

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None

# =========================================================
# 🔐 AUTH SECTION
# =========================================================
if not st.session_state.user:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Signup", "Reset Password"]
    )

    # ---------- LOGIN ----------
    if menu == "Login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if not email or not password:
                st.warning("Enter email and password")

            else:
                try:
                    res = login(email, password)

                    if res.user:
                        st.session_state.user = res.user
                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Invalid email or password")

                except Exception as e:
                    st.error(f"Login failed: {str(e)}")

    # ---------- SIGNUP ----------
    elif menu == "Signup":

        st.subheader("Create Account")

        email = st.text_input("New Email")
        password = st.text_input("New Password", type="password")

        if st.button("Signup"):

            if len(password) < 6:
                st.warning("Password must be at least 6 characters")

            else:
                try:
                    signup(email, password)
                    st.success("Account created! Verify your email.")

                except Exception as e:
                    st.error(f"Signup failed: {str(e)}")

    # ---------- RESET PASSWORD ----------
    elif menu == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Enter your email")

        if st.button("Send Reset Link"):

            try:
                reset_password(email)
                st.success("Password reset email sent!")

            except Exception as e:

                msg = str(e)

                if "rate limit" in msg.lower():
                    st.warning("Too many reset requests. Please wait a few minutes.")

                else:
                    st.error(f"Reset failed: {msg}")

# =========================================================
# 🚀 MAIN APP
# =========================================================
if st.session_state.user:

    st.sidebar.success(f"Welcome {st.session_state.user.email}")
    option = st.sidebar.radio(
        "Menu",
        [
            "Enhance Image",
            "History",
            "Logout"
        ]
    )
 
    # ---------- LOGOUT ----------
    if option == "Logout":
        st.session_state.user = None
        st.rerun()
        
    # ---------- HISTORY ---------------
    if option == "History":

        st.subheader("📜 Your History")

        history = get_history(
            st.session_state.user.email
        )

        for item in history:

            col1, col2 = st.columns(2)

            with col1:
                st.image(item["original_url"], caption="Original")

            with col2:
                st.image(item["enhanced_url"], caption="Enhanced")
                
    # ---------- ENHANCE ----------
    if option == "Enhance Image":

        st.subheader("Upload & Clean Your Product Image")

        # 🔥 Enhancement Type
        
        enhance_type = st.selectbox(
            "Enhancement Type",
            [
                "Product Clean",
                "Photo Enhance",
                "AI Face Restore"
            ]
        )        
        
        photo_mode = "Natural"

        if enhance_type == "Photo Enhance":

            photo_mode = st.selectbox(
                "Photo Style",
                [
                    "Natural",
                    "Sharp",
                    "Bright",
                    "Social Media"
                ]
            )
            
        uploaded = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded:

            img = Image.open(uploaded)

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    img,
                    caption="Before",
                    use_column_width=True
                )

            # 🔥 PROCESS BUTTON
            if st.button("✨ Clean Image"):

                with st.spinner("AI processing image..."):

                    # PRODUCT CLEAN
                    # PRODUCT CLEAN
                    if enhance_type == "Product Clean":
                        result = clean_product_image(img)

                    # PHOTO ENHANCE
                    elif enhance_type == "Photo Enhance":
                        result = enhance_photo(img, photo_mode)

                    # AI FACE RESTORE
                    else:
                        restored_url = restore_face(uploaded)

                        st.image(restored_url, caption="AI Restored")
                        st.stop()                    
                    

                with col2:
                    st.image(
                        result,
                        caption="After",
                        use_column_width=True
                    )

                # SAVE OUTPUT
                result.save("output.png")

                # DOWNLOAD BUTTON
                with open("output.png", "rb") as f:

                    st.download_button(
                        "📥 Download Clean Image",
                        f,
                        file_name="cleaned_image.png"
                    )
                    
# SAVE ORIGINAL
original_buffer = io.BytesIO()
img.save(original_buffer, format="PNG")

original_url = upload_image(
    original_buffer.getvalue(),
    "original.png"
)

# SAVE ENHANCED
enhanced_buffer = io.BytesIO()
result.save(enhanced_buffer, format="PNG")

enhanced_url = upload_image(
    enhanced_buffer.getvalue(),
    "enhanced.png"
)
# SAVE HISTORY
save_history(
    st.session_state.user.email,
    original_url,
    enhanced_url
)