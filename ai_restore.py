import replicate
import streamlit as st
import tempfile

# =========================================
# REPLICATE CLIENT
# =========================================
client = replicate.Client(
    api_token=st.secrets["REPLICATE_API_TOKEN"]
)

# =========================================
# AI FACE RESTORE
# =========================================
def restore_face(uploaded_file):

    # Save uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:

        temp.write(uploaded_file.read())

        temp_path = temp.name

    # Run model
    output = client.run(
        "nightmareai/real-esrgan",
        input={
            "image": open(temp_path, "rb"),
            "scale": 2,
            "face_enhance": True
        }
    )

    return output