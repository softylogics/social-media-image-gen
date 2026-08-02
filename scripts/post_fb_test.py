import json
import sys

import requests

BASE = "https://graph.facebook.com/v21.0"
IMAGE = r"D:\social-media-image-gen\test_image.png"
TOKEN_FILE = r"D:\social-media-image-gen\token.txt"
PAGE_ID = "451011084770089"


def load_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()


def get_page_access_token(system_token):
    r = requests.get(f"{BASE}/me/accounts", params={"access_token": system_token})
    print("me/accounts status:", r.status_code)
    r.raise_for_status()
    for page in r.json().get("data", []):
        if page["id"] == PAGE_ID:
            return page["access_token"]
    raise RuntimeError(f"Page {PAGE_ID} not found in system user's accounts")


def post_to_facebook(token, image_path, caption):
    url = f"{BASE}/{PAGE_ID}/photos"
    with open(image_path, "rb") as f:
        files = {"source": ("image.png", f, "image/png")}
        data = {"caption": caption, "access_token": token}
        r = requests.post(url, data=data, files=files)
    print("FB status:", r.status_code)
    print("FB body:", r.text)
    r.raise_for_status()
    return r.json()


def main():
    system_token = load_token()
    page_token = get_page_access_token(system_token)
    caption = "Test post from automation pipeline - Facebook"
    result = post_to_facebook(page_token, IMAGE, caption)
    print("Facebook post created:", result.get("id"))


if __name__ == "__main__":
    main()
