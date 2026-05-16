import replicate
import streamlit as st
import tempfile

# =====================================================
# AI FACE RESTORE
# =====================================================

def restore_face(uploaded_file):

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    ) as temp:

        temp.write(uploaded_file.read())

        temp_path = temp.name

    # Run AI restoration
    output = replicate.run(

        "nightmareai/real-esrgan",

        input={

            "image": open(temp_path, "rb"),

            "scale": 4,

            "face_enhance": True
        }
    )

    return output