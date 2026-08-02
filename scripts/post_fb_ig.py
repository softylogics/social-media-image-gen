import json
import os
import time

import requests

BASE = "https://graph.facebook.com/v21.0"
GITHUB_RAW = "https://raw.githubusercontent.com/softylogics/social-media-image-gen/master"
PAGE_ID = "451011084770089"
IG_USER_ID = "17841472192347466"


def get_page_token(system_token):
    r = requests.get(f"{BASE}/me/accounts", params={"access_token": system_token})
    r.raise_for_status()
    for page in r.json().get("data", []):
        if page["id"] == PAGE_ID:
            return page["access_token"]
    raise RuntimeError(f"Page {PAGE_ID} not found")


def post_to_facebook(page_token, image_path, caption):
    url = f"{BASE}/{PAGE_ID}/photos"
    with open(image_path, "rb") as f:
        files = {"source": (os.path.basename(image_path), f, "image/png")}
        data = {"caption": caption, "access_token": page_token}
        r = requests.post(url, data=data, files=files)
    print("FB:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()


def create_ig_container(system_token, image_url, caption):
    url = f"{BASE}/{IG_USER_ID}/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": system_token,
    }
    r = requests.post(url, data=data)
    print("IG container:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()["id"]


def publish_ig_container(system_token, creation_id):
    url = f"{BASE}/{IG_USER_ID}/media_publish"
    data = {"creation_id": creation_id, "access_token": system_token}
    r = requests.post(url, data=data)
    print("IG publish:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()


def main():
    system_token = os.environ["FB_SYSTEM_USER_TOKEN"]
    page_token = get_page_token(system_token)

    with open("state/pending_post.json") as f:
        pending = json.load(f)
    image_name = pending["image_name"]
    caption = pending["caption"]
    image_path = os.path.join("images", image_name)

    fb = post_to_facebook(page_token, image_path, caption)
    print("Facebook post id:", fb.get("id"))

    image_url = f"{GITHUB_RAW}/images/{image_name}"
    creation_id = create_ig_container(system_token, image_url, caption)
    time.sleep(5)
    ig = publish_ig_container(system_token, creation_id)
    print("Instagram post id:", ig.get("id"))

    with open("state/last_post.json", "w") as f:
        json.dump(
            {"image_name": image_name, "image_url": image_url,
             "fb_id": fb.get("id"), "ig_id": ig.get("id"),
             "caption": caption, "timestamp": int(time.time())},
            f, indent=2)
    print("DONE")


if __name__ == "__main__":
    main()
