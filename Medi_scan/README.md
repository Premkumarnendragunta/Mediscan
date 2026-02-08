# MediFind – Prescription Reader & Medicine Locator (Django)

MediFind is a Django web app that reads a **handwritten/printed prescription image** using OCR,
extracts **medicine names**, shows **details** (uses/side-effects), and helps locate **nearby pharmacies**.

## Features
- Upload prescription image (JPG/PNG/PDF*).
- OCR with preprocessing (OpenCV + Tesseract).
- Fuzzy matching against a medicine database (CSV -> DB).
- Medicine details page.
- Google Maps Places integration to search pharmacies near you.

> *PDF support requires converting the first page to image (use `pdf2image` if needed).

---

## Quick Start

### 1) Requirements
- Python 3.10+
- **Tesseract OCR binary** installed on your machine
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: `brew install tesseract`
  - Linux (Debian/Ubuntu): `sudo apt-get install tesseract-ocr`
- A Google Maps API key (for Places) – optional for basic run

### 2) Create & activate virtualenv
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Environment variables
Copy `.env.example` to `.env` and fill values.
```bash
cp .env.example .env
```

### 4) Django setup
```bash
python manage.py migrate
python manage.py load_medicines  # loads sample CSV into DB
python manage.py runserver
```

Open http://127.0.0.1:8000 and upload a sample image.

### 5) Tesseract path (Windows)
If Tesseract isn’t on PATH, set it in `.env`:
```
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## Project Structure
```
medifind/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ medifind_project/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ core/
   ├─ models.py
   ├─ views.py
   ├─ urls.py
   ├─ forms.py
   ├─ ocr.py
   ├─ medicine_matcher.py
   ├─ management/commands/load_medicines.py
   ├─ templates/
   │  ├─ base.html
   │  ├─ index.html
   │  └─ result.html
   ├─ static/
   │  ├─ css/styles.css
   │  └─ js/map.js
   └─ data/medicines_sample.csv
```

---

## Notes
- This is a **starter**. You can replace the sample CSV with a larger dataset.
- For better handwriting OCR, consider Google Cloud Vision. You can integrate it in `ocr.py`.
- If you add PDF support, install `pdf2image` and `poppler` and convert to images before OCR.
