import asyncio
from pathlib import Path
import edge_tts
from config import AUDIO_DIR, VOICE_EN_MALE

async def generate_speech_async(text: str, output_path: Path, voice: str = VOICE_EN_MALE) -> Path:
    """
    Generates realistic neural voiceover using Edge-TTS asynchronously.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))
    return output_path

def generate_voice(text: str, filename: str = "voiceover.mp3", voice: str = VOICE_EN_MALE) -> Path:
    """
    Synchronous wrapper to generate neural voiceover.
    """
    output_path = AUDIO_DIR / filename
    asyncio.run(generate_speech_async(text, output_path, voice))
    return output_path

if __name__ == "__main__":
    sample_text = (
        "Did you know artificial intelligence just cracked one of the biggest mysteries in biology? "
        "Scientists didn't expect this breakthrough for another twenty years. Subscribe to stay ahead!"
    )
    print("Generating sample voiceover...")
    path = generate_voice(sample_text, "sample_test.mp3")
    print(f"Sample voice generated successfully at: {path}")
