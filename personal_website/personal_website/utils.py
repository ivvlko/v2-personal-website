from urllib.parse import urlparse, parse_qs


def process_youtube_link(url):
    if not url:
        return url

    parsed_url = urlparse(url)

    if "youtube.com" in parsed_url.netloc and "watch" in parsed_url.path:
        video_id = parse_qs(parsed_url.query).get("v", [""])[0]
        return f"https://www.youtube.com/embed/{video_id}"

    if "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path.lstrip("/")
        return f"https://www.youtube.com/embed/{video_id}"

    return url
