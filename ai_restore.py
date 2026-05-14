import replicate
import streamlit as st
import tempfile

replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

def restore_face(uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    output = replicate.run(
        "tencentarc/gfpgan:613a9fe11460e58c9c93c0d5fcf8d4a7d3e1c1cbf6f79d8f8b5f0e6e8c4c8f5d",
        input={
            "img": open(temp_path, "rb"),
            "version": "v1.4",
            "scale": 2
        }
    )

    return output