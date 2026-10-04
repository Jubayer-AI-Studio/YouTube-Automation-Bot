import json
import sys
import random
import requests
from typing import Dict, Any

# Ensure proper Unicode printing on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, NICHE, CHANNEL_NAME

FALLBACK_TEMPLATES = [
    {
        "topic": "OpenAI Builds Real-Life JARVIS",
        "title": "OpenAI Just Built Iron Man's JARVIS In Real Life! ⚡🤖",
        "hook": "Tony Stark's JARVIS isn't science fiction anymore. OpenAI just brought it to life.",
        "script": (
            "Tony Stark's JARVIS isn't science fiction anymore. OpenAI just brought it to life. "
            "Imagine an autonomous AI that doesn't just chat, but controls your computer, hacks firewalls, "
            "writes software, and operates physical robots in real time. "
            "We are literally months away from having a personal superhero assistant running our digital world. "
            "Would you trust JARVIS with full access to your life?"
        ),
        "description": (
            "How real-world autonomous AI agents are turning Tony Stark's JARVIS into reality.\n\n"
            "📌 Chapters:\n0:00 - The Marvel Fantasy\n0:15 - Autonomous Agents Taking Over\n0:35 - Real-Life JARVIS\n\n"
            "#IronMan #JARVIS #AI #Robotics #MarvelTech #Shorts"
        ),
        "tags": ["Iron Man JARVIS", "Real Life JARVIS", "OpenAI", "Autonomous AI", "Future Tech", "Marvel AI", "Robotics 2026"],
        "b_roll_keywords": ["iron man jarvis hud", "futuristic robot combat", "sci fi hologram interface"]
    },
    {
        "topic": "Next-Gen Combat Humanoid Robots",
        "title": "New Combat Robots Move Like MARVEL Superheroes! 🦾⚡",
        "hook": "Forget slow clunky robots. What engineers just revealed looks straight out of Marvel.",
        "script": (
            "Forget slow clunky robots. What engineers just revealed looks straight out of Marvel. "
            "Next-gen humanoid robots can now perform backflips, combat parkour, and sprint at twenty miles per hour. "
            "Equipped with military-grade autonomous AI, they react faster than any human soldier on Earth. "
            "We are officially watching the birth of real-life Terminator tech. "
            "Are we creating our protectors... or our replacements?"
        ),
        "description": (
            "Humanoid combat robotics are advancing at terrifying speed.\n\n"
            "📌 Chapters:\n0:00 - Next-Gen Agility\n0:18 - Combat AI Reflexes\n0:35 - What Happens Next\n\n"
            "#Robotics #HumanoidRobot #FutureWarfare #SciFiTech #AI"
        ),
        "tags": ["Humanoid Robot", "Combat Robotics", "Boston Dynamics", "Military AI", "Terminator", "Future Robots", "Sci Fi Tech"],
        "b_roll_keywords": ["combat robot action", "sci fi soldier tunnel", "futuristic mechanical cyborg"]
    },
    {
        "topic": "The Quiet Rise of Neuromorphic AI Chips",
        "title": "Scientists Built an AI Chip That ACTUALLY Thinks Like a Brain! 🧠",
        "hook": "Forget Nvidia GPUs. What scientists just built in a Swiss lab is completely insane.",
        "script": (
            "Forget Nvidia GPUs. What scientists just built in a Swiss lab is completely insane. "
            "Instead of consuming enough electricity to power a small town, new neuromorphic chips run on less energy than a pocket watch, "
            "mimicking real biological synapses. If this scales, your smartphone could soon run a trillion-parameter AI model locally, "
            "with zero internet connection. And the craziest part? This is already working right now."
        ),
        "description": (
            "Explore the groundbreaking world of neuromorphic computing.\n\n"
            "📌 Chapters:\n0:00 - The GPU Problem\n0:15 - How Neuromorphic Synapses Work\n0:35 - Future of On-Device AI\n\n"
            "#AI #TechNews #ArtificialIntelligence #FutureTech #Shorts"
        ),
        "tags": ["Artificial Intelligence", "AI Chip", "Neuromorphic Computing", "Nvidia AI", "Future Tech", "Tech News", "AI 2026"],
        "b_roll_keywords": ["computer chip technology", "artificial intelligence brain", "futuristic server room", "microchip circuit"]
    },
    {
        "topic": "AI Cracks Quantum Chemistry",
        "title": "AI Just Solved a 100-Year-Old Physics Problem In SECONDS! ⚛️",
        "hook": "Einstein spent decades trying to calculate this. AI just solved it in under 4 seconds.",
        "script": (
            "Einstein spent decades trying to calculate this. AI just solved it in under 4 seconds. "
            "By combining deep neural networks with quantum physics equations, researchers have simulated the exact chemical reaction "
            "needed for room-temperature superconductors. If verified, this single discovery could revolutionize batteries, "
            "high-speed rail, and space exploration overnight. Are we entering the golden era of AI-driven science?"
        ),
        "description": (
            "How AI simulated complex quantum chemistry to unlock the secret of room-temperature superconductors.\n\n"
            "📌 Timestamps:\n0:00 - The 100-Year Mystery\n0:18 - AI Solves Quantum Physics\n0:35 - What This Changes\n\n"
            "#Science #QuantumComputing #AI #Superconductor #TechShorts"
        ),
        "tags": ["Quantum Physics", "AI Science", "Superconductors", "Quantum AI", "Scientific Discovery", "Physics News", "Artificial Intelligence"],
        "b_roll_keywords": ["quantum physics abstract", "laboratory experiment science", "superconductor technology", "digital particles futuristic"]
    },
    {
        "topic": "Recursive Self-Improving AI",
        "title": "The AI That Keeps Making ITSELF Smarter — Should We Be Worried? 🤖",
        "hook": "What if an AI could rewrite its own code to become 10x smarter overnight? That's already happening.",
        "script": (
            "What if an AI could rewrite its own code to become 10x smarter overnight? That's already happening. "
            "Recursive self-improvement — where AI optimizes its own architecture — has crossed from theory into real lab experiments. "
            "OpenAI, DeepMind and a dozen stealth startups are quietly racing to build it. "
            "Obama warned about it. Elon Musk lost sleep over it. "
            "Once triggered, there may be no stopping it. What would YOU do?"
        ),
        "description": (
            "Recursive Self-Improvement: The AI concept that could change everything overnight.\n\n"
            "📌 Timestamps:\n0:00 - What Is Recursive Self-Improvement\n0:20 - Real Lab Experiments\n0:38 - Why Leaders Are Scared\n\n"
            "#AGI #RecursiveAI #ArtificialIntelligence #FutureOfAI #AINews"
        ),
        "tags": ["Recursive AI", "AGI", "Self-Improving AI", "AI Safety", "OpenAI", "DeepMind", "AI News 2026", "Future AI"],
        "b_roll_keywords": ["artificial intelligence robot future", "data center servers glowing", "neural network visualization", "AI code programming"]
    }
]

FREE_MODELS = [
    "qwen/qwen3.8-27b:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

def call_openrouter(prompt: str) -> str:
    """
    Calls OpenRouter API. Tries multiple free models with retry on rate limit.
    """
    import time
    last_error = None
    for model in FREE_MODELS:
        for attempt in range(2):
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://youtube.com/@jubayeraispecialist",
                        "X-Title": CHANNEL_NAME
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"}
                    },
                    timeout=45
                )
                r.raise_for_status()
                data = r.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                last_error = e
                if "429" in str(e):
                    print(f"[Rate limit on {model}] Waiting 8 seconds...")
                    time.sleep(8)
                else:
                    break
    raise Exception(f"All models failed. Last error: {last_error}")

def generate_script_and_seo(topic_prompt: str = "") -> Dict[str, Any]:
    """
    Generates a viral English script, SEO title, description, tags, and b-roll keywords.
    """
    if not OPENROUTER_API_KEY:
        print("[Notice] OPENROUTER_API_KEY not configured. Using pre-engineered blueprint...")
        return random.choice(FALLBACK_TEMPLATES)

    prompt = f"""
You are an elite YouTube Growth Strategist & Tech Scriptwriter (style: Fireship + ColdFusion + Matt Wolfe).
Channel: "{CHANNEL_NAME}" — focused on AI news, autonomous AI, mind-blowing tech facts, cybersecurity AI threats.

Create a 35-45 second high-retention YouTube Shorts script about: {topic_prompt or NICHE}.

Rules:
1. Hook (0-3s): Instantly shocking, no greetings, no intros. Grab attention NOW.
2. Body (3-35s): Witty, conversational, fast-paced. Dense information, easy to understand.
3. Ending (35-42s): Thought-provoking question or seamless loop back to the hook.
4. Language: Natural spoken English. No corporate speak.
5. Title: Curiosity gap + power words + emoji (max 80 chars).
6. Description: First 2 lines keyword-rich, then timestamps, then hashtags.
7. Tags: 12-15 high search volume tags.
8. b_roll_keywords: 4 short video search terms for stock footage.

Return ONLY valid JSON matching exactly this schema:
{{
    "topic": "...",
    "title": "...",
    "hook": "...",
    "script": "...",
    "description": "...",
    "tags": ["tag1", "tag2"],
    "b_roll_keywords": ["keyword1", "keyword2", "keyword3", "keyword4"]
}}
"""
    try:
        raw = call_openrouter(prompt)
        return json.loads(raw)
    except Exception as e:
        print(f"[Warning] OpenRouter call failed: {e}. Using fallback blueprint.")
        return random.choice(FALLBACK_TEMPLATES)


if __name__ == "__main__":
    print("Testing AI Script & SEO Generator with OpenRouter...\n")
    result = generate_script_and_seo()
    print("=" * 55)
    print(f"Title   : {result['title']}")
    print(f"Hook    : {result['hook']}")
    print(f"\nScript  :\n{result['script']}")
    print(f"\nTags    : {', '.join(result['tags'][:5])}...")
    print(f"B-Roll  : {result['b_roll_keywords']}")
    print("=" * 55)
