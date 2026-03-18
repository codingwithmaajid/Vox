# This is a Transcript.py File

import re 
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    if re.match(r"^[0-9A-Za-z_-]{11}$", url):
        return url



    if not re.search(r"(youtube\.com|youtu\.be)",url):
        raise ValueError("Not a YouTube Url :-" + url)



    patterns = [
        r"[?&]v=([0-9A-Za-z_-]{11})",
        r"youtu\.be/([0-9A-Za-z_-]{11})",
        r"/shorts/([0-9A-Za-z_-]{11})",
        r"/embed/([0-9A-Za-z_-]{11})",
    ]


    for values in patterns:
        match = re.search(values, url)
        if match:
            return match.group(1)

    raise ValueError("Could not find video ID in: " + url)

def fetch_transcript(url):
    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id)
        transcript_pieces = list(fetched)
        text = " ".join(piece.text for piece in transcript_pieces)
        return text, transcript_pieces

    except Exception as e:
        raise RuntimeError("Could not get transcript: " + str(e))





if __name__ == "__main__":
    text, pieces = fetch_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print("Words:", len(text.split()))
    print("First 100 chars:", text[:100])
