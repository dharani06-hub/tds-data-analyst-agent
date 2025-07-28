import openai
import pytesseract
from PIL import Image
import io
import tempfile
import whisper

openai.api_key = "your-openai-api-key"

def ask_llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def image_to_text(image_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img)

def audio_to_text(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        model = whisper.load_model("base")
        result = model.transcribe(tmp.name)
        return result["text"]

