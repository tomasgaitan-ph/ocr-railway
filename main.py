import base64
import pytesseract
from pdf2image import convert_from_bytes
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Tesseract path (Debian slim uses this)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = FastAPI()

@app.post("/ocr")
async def ocr_endpoint(pdf_base64: str):
    try:
        # 1) Decode Base64 PDF
        pdf_bytes = base64.b64decode(pdf_base64)

        # 2) Convert to images
        images = convert_from_bytes(pdf_bytes, dpi=300)

        full_text = ""

        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img, lang="spa+eng")
            full_text += f"\n\n--- Página {i+1} ---\n{text}"

        return {
            "error": False,
            "pages": len(images),
            "text": full_text
        }

    except Exception as e:
        return {"error": True, "message": str(e)}
