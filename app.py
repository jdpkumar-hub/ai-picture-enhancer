import streamlit as st
from PIL import Image
from auth import (
    signup,
    login,
    reset_password,
    google_login,
    get_user
)
from enhance import clean_product_image, enhance_photo

from storage import (
    upload_image,
    save_history,
    get_history,
    delete_history_item
)

import io

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Product Image Cleaner",
    layout="wide"
)

# =========================================================
# UI STYLE
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #00C9A7);
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
    font-size: 16px;
    font-weight: bold;
}

.stDownloadButton>button {
    background: linear-gradient(90deg, #4CAF50, #00C9A7);
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
    font-size: 16px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("🚀 AI Product Image Cleaner")

# =========================================================
# SESSION
# =========================================================

if "user" not in st.session_state:
    st.session_state.user = get_user()

# =========================================================
# AUTH SECTION
# =========================================================

if not st.session_state.user:

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Login",
            "Signup",
            "Reset Password"
        ]
    )

    # =====================================================
    # LOGIN
    # =====================================================

    if menu == "Login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if not email or not password:
                st.warning("Please enter email and password")

            else:

                try:

                    res = login(email, password)

                    if res and res.user:

                        st.session_state.user = res.user

                        st.success("Login successful!")

                        st.rerun()

                    else:
                        st.error("Invalid email or password")

                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
    # =====================================================
    # GOOGLE
    # =====================================================                    
                    
        st.markdown("---")

        google_url = google_login()

        if google_url:
            st.link_button(
                "🔵 Continue with Google",
                google_url
                )

    # =====================================================
    # SIGNUP
    # =====================================================

    elif menu == "Signup":

        st.subheader("Create Account")

        email = st.text_input("New Email")
        password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Signup"):

            if len(password) < 6:
                st.warning(
                    "Password must be at least 6 characters"
                )

            else:

                try:

                    signup(email, password)

                    st.success(
                        "Account created! Verify your email."
                    )

                except Exception as e:
                    st.error(f"Signup failed: {str(e)}")

    # =====================================================
    # RESET PASSWORD
    # =====================================================

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
                    st.warning(
                        "Too many reset requests. Please wait a few minutes."
                    )

                else:
                    st.error(f"Reset failed: {msg}")

# =========================================================
# MAIN APP
# =========================================================

if st.session_state.user:

    st.sidebar.success(
        f"Welcome {st.session_state.user.email}"
    )

    option = st.sidebar.radio(
        "Menu",
        [
            "Enhance Image",
            "History",
            "Logout"
        ]
    )

    # =====================================================
    # LOGOUT
    # =====================================================

    if option == "Logout":

        st.session_state.user = None
        st.rerun()

    # =====================================================
    # HISTORY
    # =====================================================

    elif option == "History":

        st.subheader("📜 Your History")

        history = get_history(
            st.session_state.user.email
        )

        if not history:
            st.info("No history found")

        for item in history:

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    item["original_url"],
                    caption="Original",
                    use_column_width=True
                )

            with col2:
                st.image(
                    item["enhanced_url"],
                    caption="Enhanced",
                    use_column_width=True
                )

            st.write(
                f"✨ Type: {item.get('enhancement_type', 'Unknown')}"
            )            

            if st.button(
                "🗑 Delete",
                key=item["id"]
            ):

                deleted = delete_history_item(
                    item["id"],
                    item["original_path"],
                    item["enhanced_path"]
                )

                if deleted:
                    st.success("Deleted successfully!")
                    st.rerun()

                else:
                    st.error("Delete failed")

    # =====================================================
    # ENHANCE IMAGE
    # =====================================================

    elif option == "Enhance Image":

        st.subheader(
            "Upload & Clean Your Product Image"
        )

        # =================================================
        # ENHANCEMENT TYPE
        # =================================================

        enhance_type = st.selectbox(
            "Enhancement Type",
            [
                "Product Clean",
                "Photo Enhance"
            ]
        )

        # =================================================
        # PHOTO MODE
        # =================================================

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

        # =================================================
        # FILE UPLOAD
        # =================================================

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

            # =============================================
            # PROCESS BUTTON
            # =============================================

            if st.button("✨ Clean Image"):

                with st.spinner(
                    "AI processing image..."
                ):

                    # =====================================
                    # PRODUCT CLEAN
                    # =====================================

                    if enhance_type == "Product Clean":

                        result = clean_product_image(img)

                    # =====================================
                    # PHOTO ENHANCE
                    # =====================================

                    else:

                        result = enhance_photo(
                            img,
                            photo_mode
                        )

                # =========================================
                # SHOW RESULT
                # =========================================

                with col2:

                    st.image(
                        result,
                        caption="After",
                        use_column_width=True
                    )

                # =========================================
                # SAVE TEMP OUTPUT
                # =========================================

                result.save("output.png")

                # =========================================
                # ORIGINAL BUFFER
                # =========================================

                original_buffer = io.BytesIO()

                img.save(
                    original_buffer,
                    format="PNG"
                )

                original_url, original_path = upload_image(
                    original_buffer.getvalue(),
                    "originals"
                )

                # =========================================
                # ENHANCED BUFFER
                # =========================================

                enhanced_buffer = io.BytesIO()

                result.save(
                    enhanced_buffer,
                    format="PNG"
                )

                enhanced_url, enhanced_path = upload_image(
                    enhanced_buffer.getvalue(),
                    "enhanced"
                )

                # =========================================
                # SAVE HISTORY
                # =========================================

                save_history(
                    st.session_state.user.email,
                    original_url,
                    enhanced_url,
                    enhance_type,
                    original_path,
                    enhanced_path
                )

                # =========================================
                # DOWNLOAD BUTTON
                # =========================================

                with open("output.png", "rb") as f:

                    st.download_button(
                        "📥 Download Clean Image",
                        f,
                        file_name="cleaned_image.png"
                    )