import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import cv2
import numpy as np


def preprocess_image(image_path):
    """
    Improve OCR accuracy by preprocessing
    """

    img = cv2.imread(image_path)

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    gray = cv2.medianBlur(gray, 3)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def extract_text_from_image(image_path):

    processed = preprocess_image(image_path)

    if processed is None:
        return ""

    text = pytesseract.image_to_string(
        processed,
        lang="eng+hin",
        config="--oem 3 --psm 6"
    )

    return text


def extract_text_from_pdf(pdf_path):

    images = convert_from_path(pdf_path)

    full_text = ""

    for img in images:

        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(
            img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        text = pytesseract.image_to_string(
            thresh,
            lang="eng+hin",
            config="--oem 3 --psm 6"
        )

        full_text += text + "\n"

    return full_text