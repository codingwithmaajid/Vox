# vox 🎙️

An all-in-one AI tool that turns any YouTube video into study material.
Built to make AI features accessible to everyone — no subscriptions, no complicated setup.

## What it does

- `summarize` — get a clear summary in seconds
- `notes` — structured study notes with headings and bullets  
- `quiz` — 5 multiple choice questions to test yourself
- `keypoints` — 8 key points from the video
- `ask` — ask anything about the video

## Setup

**1. Get a free API key**

Go to https://console.groq.com, sign up free, copy your key.

**2. Set your key**
```bash
export VOX_GROQ_API_KEY=your-key-here
```

**3. Install vox**
```bash
curl -sSL https://raw.githubusercontent.com/codingwithmaajid/Vox/main/install.sh | bash
```

## Usage
```bash
# Direct commands
vox summarize https://youtube.com/watch?v=...
vox notes     https://youtube.com/watch?v=...
vox quiz      https://youtube.com/watch?v=...
vox ask       https://youtube.com/watch?v=... "your question"

# Interactive mode
vox
```

## Built with

- Python
- Groq API (free)
- Textual
- Click
- youtube-transcript-api