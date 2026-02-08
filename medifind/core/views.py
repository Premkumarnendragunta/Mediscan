import os
from django.shortcuts import render
from django.conf import settings
from .forms import UploadForm
from .ocr import extract_text

# LLM imports
import google.generativeai as genai
from dotenv import load_dotenv

# Translation
from deep_translator import GoogleTranslator

load_dotenv()
genai.configure(api_key="AIzaSyCF7kBttdz9OX4eXQNQwwcwA5NfmR0jdkQ")

# Map form language codes to TTS codes
TTS_LANGUAGE_CODES = {
    "en": "en-US",
    "hi": "hi-IN",
    "kn": "kn-IN",
    "te": "te-IN",
    "ta": "ta-IN",
}

def index(request):
    context = {"api_key": settings.GOOGLE_MAPS_API_KEY}

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded file
            img = form.cleaned_data["prescription"]
            uploads_dir = settings.BASE_DIR / "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            file_path = uploads_dir / img.name
            with open(file_path, "wb+") as dest:
                for chunk in img.chunks():
                    dest.write(chunk)

            # Step 1: Extract text using OCR
            raw_text = extract_text(str(file_path))

            # Step 2: Get user-selected language
            selected_language = form.cleaned_data["language"]
            tts_lang_code = TTS_LANGUAGE_CODES.get(selected_language, "en-US")
            selected_language_name = dict(form.fields['language'].choices)[selected_language]

            # Step 3: Build prompt → Always English
            prompt = f"""
            You are a medical assistant.
            This is an image of a doctor's prescription 

            

            Your task:
            - Identify all medicines in the prescription
            - Give full medicine name
            - Purpose
            - Dosage
            - Common side effects
            - Where it can be commonly purchased

            IMPORTANT:
            - Respond ONLY in English.
            - Do NOT include any other language.
            """

            try:
                model = genai.GenerativeModel("gemini-2.5-pro")  # supports multimodal
                with open(file_path, "rb") as img_file:
                    image_data = img_file.read()

                response = model.generate_content([
                    prompt,
                    {"mime_type": "image/png", "data": image_data}
                ])

                matches_en = response.text

                # Step 4: Translate to user-selected language if not English
                if selected_language != "en":
                    matches = GoogleTranslator(
                        source='en',
                        target=selected_language
                    ).translate(matches_en)
                else:
                    matches = matches_en

            except Exception as e:
                matches = f"Error calling LLM: {e}"

            # Step 5: Update context and render results
            context.update({
                "form": form,
                "raw_text": raw_text,
                "matches": matches,   # already translated to user’s language
                "selected_language": selected_language_name,
                "selected_language_code": tts_lang_code,
                "uploaded_image": img.name
            })
            return render(request, "result.html", context)
        else:
            context["form"] = form
    else:
        context["form"] = UploadForm()

    return render(request, "index.html", context)
