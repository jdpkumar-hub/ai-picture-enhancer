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
            "🪄 Background Remove",
            use_container_width=True
        ):
            st.switch_page(
                "pages/4_Background_Remove.py"
            )

        if st.button(
            "🧓 Old Photo Restore",
            use_container_width=True
        ):
            st.switch_page(
                "pages/5_Old_Photo_Restore.py"
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
        # USER INFO
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