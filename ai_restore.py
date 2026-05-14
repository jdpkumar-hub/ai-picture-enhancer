import replicate
import streamlit as st
import tempfile

# Initialize Replicate client
client = replicate.Client(
    api_token=st.secrets["REPLICATE_API_TOKEN"]
)

# =========================================
# AI FACE RESTORATION
# =========================================
def restore_face(uploaded_file):

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:

        temp.write(uploaded_file.read())

        temp_path = temp.name

    # Run GFPGAN model
    output = client.run(
        "nightmareai/real-esrgan",
        input={
            "image": open(temp_path, "rb"),
            "face_enhance": True
        }
    )

    return output