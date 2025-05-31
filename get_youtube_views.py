import os, json, requests
from notion_client import Client
from urllib.parse import urlparse, parse_qs

NOTION_TOKEN = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

URL_PROP = config["url_property_name"]
VIEWS_PROP = config["view_count_property_name"]

notion = Client(auth=NOTION_TOKEN)

def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    qs = parse_qs(parsed.query)
    return qs.get('v', [None])[0]

def get_view_count(video_id):
    api = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    r = requests.get(api).json()
    print("🔐 YouTube API Key Loaded:", YOUTUBE_API_KEY[:6], "...")
    return int(r["items"][0]["statistics"]["viewCount"]) if "items" in r and r["items"] else None

results = notion.databases.query(database_id=DATABASE_ID)
for page in results["results"]:
    props = page["properties"]
    if URL_PROP not in props or not props[URL_PROP].get("url"):
        continue
    video_id = extract_video_id(props[URL_PROP]["url"])
    if not video_id:
        continue
    views = get_view_count(video_id)
    if views is not None:
        notion.pages.update(page_id=page["id"], properties={
            VIEWS_PROP: {"number": views}
        })
    print(f"🎵 {props.get('曲名', {}).get('title', [{}])[0].get('plain_text', 'Untitled')}")
    print(f"🔗 URL: {props[URL_PROP]['url']}")
    print(f"📺 Video ID: {video_id}")
    print(f"👀 Views: {views}")
