import streamlit as st

from auth import logout


def render_sidebar():

    with st.sidebar:

        # ==========================================
        # LOGO
        # ==========================================

        st.image(
            "assets/logo.png",
            width=240
        )

        st.caption(
            "🚀 Smart AI Image Platform"
        )

        st.markdown(
            "<div class='sidebar-divider'></div>",
            unsafe_allow_html=True
        )

        # ==========================================
        # MENU
        # ==========================================

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):
            st.switch_page("app.py")

        if st.button(
            "✨ Enhance",
            use_container_width=True
        ):
            st.switch_page("pages/1_Enhance.py")

        if st.button(
            "🪄 Remove Background",
            use_container_width=True
        ):
            st.switch_page(
                "pages/4_Background_Remove.py"
            )

        if st.button(
            "🧓 Restore Photo",
            use_container_width=True
        ):
            st.switch_page(
                "pages/5_Old_Photo_Restore.py"
            )

        if st.button(
            "🧼 Remove Objects",
            use_container_width=True
        ):
            st.switch_page(
                "pages/6_Object_Removal.py"
            )

        if st.button(
            "🛍 Product AI",
            use_container_width=True
        ):
            st.switch_page(
                "pages/7_Product_Photo_AI.py"
            )

        if st.button(
            "🤖 Prompt Edit",
            use_container_width=True
        ):
            st.switch_page(
                "pages/8_AI_Prompt_Edit.py"
            )

        if st.button(
            "📦 Batch Enhance",
            use_container_width=True
        ):
            st.switch_page(
                "pages/9_Batch_Enhancer.py"
            )

        if st.button(
            "🎨 Anime Studio",
            use_container_width=True
        ):
            st.switch_page(
                "pages/10_Anime_Studio.py"
            )

        if st.button(
            "📜 History",
            use_container_width=True
        ):
            st.switch_page(
                "pages/2_History.py"
            )

        if st.button(
            "👤 Profile",
            use_container_width=True
        ):
            st.switch_page(
                "pages/3_Profile.py"
            )

        st.markdown(
            "<div class='sidebar-divider'></div>",
            unsafe_allow_html=True
        )

        # ==========================================
        # LOGOUT
        # ==========================================

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()

            st.session_state.user = None

            st.switch_page("app.py")

            st.stop()

        # ==========================================
        # USER
        # ==========================================

        if (
            "user" in st.session_state
            and st.session_state.user
        ):

            st.success(
                f"Welcome {st.session_state.user.email}"
            )

        st.caption(
            "Built by JDP Kumar 🚀"
        )