import requests
import streamlit as st


API_KEY = "YOUR_REAL_PICSART_API_KEY"


def picsart_face_enhance(input_path, output_path):

    url = "https://api.picsart.io/tools/1.0/enhance/face"

    headers = {
        "X-Picsart-API-Key": API_KEY
    }

    try:

        with open(input_path, "rb") as image_file:

            files = {
                "image": image_file
            }

            response = requests.post(
                url,
                headers=headers,
                files=files
            )

        # =========================================
        # DEBUG OUTPUT
        # =========================================

        print("STATUS CODE:", response.status_code)

        print("RAW RESPONSE:")
        print(response.text)

        # =========================================
        # CHECK STATUS
        # =========================================

        if response.status_code != 200:

            st.error(f"API Error: {response.status_code}")

            return None

        data = response.json()

        print("JSON:", data)

        # =========================================
        # VALIDATE RESPONSE
        # =========================================

        if "data" not in data:

            st.error("No 'data' field returned")

            return None

        if "url" not in data["data"]:

            st.error("No image URL returned")

            return None

        enhanced_url = data["data"]["url"]

        print("Enhanced URL:", enhanced_url)

        # =========================================
        # DOWNLOAD RESULT
        # =========================================

        img_data = requests.get(enhanced_url).content

        with open(output_path, "wb") as f:
            f.write(img_data)

        return output_path

    except Exception as e:

        st.error(f"PicsArt Exception: {str(e)}")

        print("EXCEPTION:", e)

        return None