from fastapi import FastAPI, UploadFile, File
import os
import pytesseract

from services.ocr_service import extract_text_from_image, extract_text_from_pdf
from services.extraction_service import extract_fields
from utils.file_utils import save_temp_file
from models.schemas import ExtractionResult


from fastapi import FastAPI, UploadFile, File
from typing import List
import os
import pytesseract

from services.ocr_service import extract_text_from_image, extract_text_from_pdf
from services.extraction_service import extract_fields
from utils.file_utils import save_temp_file
from models.schemas import ExtractionResult


app = FastAPI(title="Document AI Extraction Service")

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\shourabha.gupta\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


@app.get("/")
def home():
    return {"message": "Document AI Extraction Service Running"}


@app.post("/extract", response_model=ExtractionResult)
async def extract_document(files: List[UploadFile] = File(...)):

    full_text = ""

    for file in files:

        file_path = save_temp_file(file)

        ext = os.path.splitext(file_path)[1].lower()

        if ext in [".jpg", ".jpeg", ".png"]:
            text = extract_text_from_image(file_path)

        elif ext == ".pdf":
            text = extract_text_from_pdf(file_path)

        else:
            continue

        full_text += "\n" + text

        os.remove(file_path)

    extracted = extract_fields(full_text)

    extracted["RawText"] = full_text

    return extracted