import requests

API_KEY = "YOUR_PICSART_API_KEY"


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

        print("Status:", response.status_code)
        print("Response:", response.text)

        data = response.json()

        if "data" not in data:

            return None

        enhanced_url = data["data"]["url"]

        img_data = requests.get(enhanced_url).content

        with open(output_path, "wb") as f:
            f.write(img_data)

        return output_path

    except Exception as e:

        print("PicsArt Error:", e)

        return None