import urllib.request, json, ssl, os, time, base64

ctx = ssl.create_default_context()
API_KEY = "sk-m8Nlf73UMzo90eW2qZGWtjL2PpQw3NJseXQpKMODUowVTaPO"
OUTPUT_DIR = r"C:\Users\Administrator\Desktop\国内奇闻文章"

retry_images = [
    ("cover_02_一天四季小镇.png", "gpt-image-2", "A small Yunnan plateau village at 3000m altitude where four seasons happen in one day. Early morning mist with people in winter coats, midday sun with villagers in summer clothes, afternoon golden light, evening bonfire warmth. Black-necked cranes fly over rolling hills. Cinematic documentary style, China landscape photography."),
    ("cover_03_长寿村如皋.png", "gpt-image-2", "A serene Chinese village at the Yangtze River estuary in Jiangsu province. Elderly Chinese villagers enjoying peaceful life, green vegetable gardens, clean wells, morning mist over rice paddies. Sunlit cobblestone paths. A 100-year-old smiling grandmother tending to flowers. Photorealistic, warm tones, National Geographic style documentary photography."),
]

for i, (filename, model, prompt) in enumerate(retry_images):
    print(f"Generating {i+1}/2: {filename}")
    body = json.dumps({"model": model, "prompt": prompt, "n": 1, "size": "1024x1024"}).encode()
    req = urllib.request.Request(
        "https://api.302.ai/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180, context=ctx) as r:
            data = json.loads(r.read())
        
        img_data = data["data"][0]
        if "b64_json" in img_data:
            img_bytes = base64.b64decode(img_data["b64_json"])
        else:
            img_url = img_data["url"]
            img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=60, context=ctx) as r:
                img_bytes = r.read()
        
        out_path = os.path.join(OUTPUT_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"  Saved: {out_path} ({len(img_bytes)} bytes)")
    except Exception as e:
        print(f"  Error: {e}")
    time.sleep(5)

print("Done!")
