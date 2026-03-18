import os
import ollama

DEFAULT_MODEL = os.getenv("VOX_MODEL", "llama-3.1-8b-instant")
GROQ_API_KEY = os.getenv("VOX_GROQ_API_KEY")

PROMPTS = {
     "summary":   """You are a helpful study assistant.
Read this YouTube video transcript and write a clear summary in 3-5 paragraphs.
Cover the main topic, key ideas, and conclusion.

TRANSCRIPT:
{transcript}""",

"notes":    """You are an expert note-taker.
Convert this transcript into structured study notes using:
- headings for major sections
- bullet points for key facts
- bold for important terms

TRANSCRIPT:
{transcript}""",

"quiz":     """You are a quiz creator.
From this transcript, make 5 multiple-choice questions.
For each: write the question, give 4 options (A B C D), mark the correct answer.

TRANSCRIPT:
{transcript}""",

"keypoints":    """Extract the 8 most important points from this transcript.
Number them. Each one should be one clear sentence.

TRANSCRIPT:
{transcript}""",

"ask":     """You are answering questions about a YouTube video.
Use ONLY the transcript below. If the answer is not there, say so.

TRANSCRIPT:
{transcript}

QUESTION: {question}""",
}


def build_prompt(action, transcript, question=""):
    if action not in PROMPTS:
        raise ValueError("Unknown action: " + action)

    template = PROMPTS[action]

    words = transcript.split()
    if len(words) > 4000:
        transcript = " ".join(words[:4000]) + "\n[Transcript trimmed]"    
    if action == "ask":
        return template.format(transcript=transcript, question=question)
    else:
        return template.format(transcript=transcript)    




def ask_groq(prompt):
    if not GROQ_API_KEY:
        raise RuntimeError(
            "No API key found.\n"
            "Get a free key at https://console.groq.com\n"
            "Then run: export VOX_GROQ_API_KEY=your-key"
        )
    
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content


def run_action(action, transcript, question=""):
    prompt = build_prompt(action, transcript, question=question)
    result = ask_groq(prompt)
    return result



if __name__ == "__main__":
    test_transcript = "Machine learning is a subset of AI. Neural networks are inspired by the brain. Training involves adjusting weights using backpropagation."
    
    print("Testing build_prompt...")
    prompt = build_prompt("summary", test_transcript)
    print("Prompt built successfully")
    print("Testing Ollama connection...")
    result = run_action("summary", test_transcript)
    print(result)    