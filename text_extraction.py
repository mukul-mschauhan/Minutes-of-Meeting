import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import docx2txt
import pandas as pd
import io

# Set the tesseract path manually
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.type
    if file_type in ["image/jpeg", "image/png"]:
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)

    elif file_type == "application/pdf":
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)

    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    elif file_type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        df = pd.read_excel(uploaded_file)
        return df.to_string(index=False)

    else:
        return "Unsupported file type"