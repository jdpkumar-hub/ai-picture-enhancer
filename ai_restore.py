import replicate
import streamlit as st
import tempfile
import os

# =====================================================
# AI FACE RESTORE  (via Replicate — real-esrgan)
# =====================================================

def restore_face(uploaded_file):

    # FIX: reset file pointer before reading in case it was
    #      already consumed upstream (e.g. by Image.open).
    uploaded_file.seek(0)

    # Save uploaded image to a temp file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    ) as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    try:
        # Run AI restoration
        output = replicate.run(
            "nightmareai/real-esrgan:42fed1c4",
            input={
                "image":        open(temp_path, "rb"),
                "scale":        4,
                "face_enhance": True
            }
        )
        return output

    except Exception as e:
        st.error(f"AI restoration failed: {str(e)}")
        return None

    finally:
        # Always clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
