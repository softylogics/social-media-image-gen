import json
import os
import time
import urllib.request

EXAMPLE_IMAGE_URLS = [
    "https://picsum.photos/1024/1024",
]


def download_image(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(dest, "wb") as f:
        f.write(data)


def main():
    image_name = os.environ.get("IMAGE_NAME", f"post_{int(time.time())}.png")
    local_path = os.path.join("images", image_name)
    os.makedirs("images", exist_ok=True)
    src = os.environ.get("IMAGE_URL", EXAMPLE_IMAGE_URLS[0])
    download_image(src, local_path)
    with open("state/pending_post.json", "w") as f:
        json.dump(
            {"image_name": image_name, "image_url": src,
             "caption": os.environ.get(
                 "CAPTION", "Test post from GitHub Actions automation pipeline"),
             "timestamp": int(time.time())},
            f, indent=2)
    print(f"Downloaded {src} -> {local_path}")


if __name__ == "__main__":
    main()
