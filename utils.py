from PIL import Image
import pytesseract
import io
import tempfile
import whisper
from response_generator import generate_response

def ask_llm(prompt: str) -> str:
    return generate_response(prompt)

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

      
