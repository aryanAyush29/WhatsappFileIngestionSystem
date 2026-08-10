import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

if not GRAPH_API_VERSION:
    print("WARNING: GRAPH_API_VERSION is not configured")

if not ACCESS_TOKEN:
    print("WARNING: WHATSAPP_ACCESS_TOKEN is not configured")

if not PHONE_NUMBER_ID:
    print("WARNING: WHATSAPP_PHONE_NUMBER_ID is not configured")


def get_media_url(media_id):
    """
    Get the temporary download URL for a WhatsApp media file.
    """

    if not GRAPH_API_VERSION or not ACCESS_TOKEN:
        raise ValueError(
            "Cannot fetch media URL: GRAPH_API_VERSION or WHATSAPP_ACCESS_TOKEN "
            "is not configured in .env"
        )

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{media_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "phone_number_id": PHONE_NUMBER_ID
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    return data["url"]


def download_media(media_url, output_path):
    """
    Download the actual WhatsApp media file.
    """

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(
        media_url,
        headers=headers,
        stream=True
    )

    response.raise_for_status()

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return output_path


if __name__ == "__main__":
    test_media_id = "MEDIA_ID_TEST_123"

    url = get_media_url(test_media_id)

    print("MEDIA URL:")
    print(url)