import cv2
import pytesseract
from django.conf import settings

# Configure Tesseract path if provided (Windows)
if getattr(settings, "TESSERACT_CMD", ""):
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def preprocess_image(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # denoise
    gray = cv2.fastNlMeansDenoising(gray, h=30)
    # threshold
    th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return th

def extract_text(image_path: str) -> str:
    processed = preprocess_image(image_path)
    # Use LSTM recognition engine. PSM 6: Assume a single uniform block of text.
    config = "--oem 1 --psm 6"
    text = pytesseract.image_to_string(processed, config=config)
    return text
