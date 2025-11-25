import base64
import pytesseract
from pdf2image import convert_from_bytes
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = FastAPI()

class OCRInput(BaseModel):
    pdf_base64: str

@app.post("/ocr")
async def ocr_endpoint(data: OCRInput):
    try:
        # obtener el base64 desde el modelo
        pdf_bytes = base64.b64decode(data.pdf_base64)

        # convertir PDF → imágenes
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
