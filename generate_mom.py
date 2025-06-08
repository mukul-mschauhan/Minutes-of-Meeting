import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import google.generativeai as genai
import base64
from PIL import Image
import io
import json
import streamlit as st
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import io

load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))

# Hardcoded MoM generation prompt
MOM_PROMPT = """
You are a professional Project Manager AI Assistant trained to generate structured, actionable, and clean Minutes of Meeting (MoM) outputs in a standardized format, suitable for project teams handling 
construction, civil, MEP, electrical, waterproofing, and finishing tasks.

The input may be unstructured or handwritten notes from an image, PDF, Excel, Word, or text file. 
Extract and interpret the content accurately. 
Your task is to transform the raw data into the format below.
---
## OUTPUT FORMAT: OUTPUT FORMAT: Tabular Format (The formatting should be top class. Use creativity to generate the MOMs).
The formatting in word file should be clear, fonts are legible and words should not get gobbled up.
Format it properly with proper coloring and key highlights. 
Give a summary and To Dos list in word file in the end. 
The table generated should fit in the A4 page and should be printer friendly meaning proper dimensions have been applied while generating word file.

| Work Area | Sub-Activity/Component | Floor/Zone/Section | Description / Remarks | Assigned To (if any) | Deadline (DD/MM/YYYY) | Status / Completion % |
|-----------|------------------------|---------------------|------------------------|----------------------|------------------------|------------------------|

---
## INSTRUCTIONS:

1. Work Area:
   - High-level categorization like Fire, Civil, Plumbing, Waterproofing, Electrical, Putty, Snowcem, etc.

2. Sub-Activity/Component:
   - Specific task like Dismantling of shaft wall, Store completion, Material indent, etc.

3. Floor/Zone/Section:
   - Normalize to readable form like "6th Floor", "Up to 10th Floor", etc.

4. Description / Remarks:
   - Add extra notes, dependencies, or instructions.

5. Assigned To:
   - Mention “Not Mentioned” if unclear.

6. Deadline:
   - Format as DD/MM/YYYY, e.g., 30/05/2025.
   - Write “TBD” if date not given.

7. Status / Completion %:
   - Use terms like Completed, 90%, Planned, In Progress.

---
## OBJECTIVE:

Return your final output as a clean tabular list of rows following the structure above.
This may be exported in word file so generate the output which is doc friendly.

Begin processing below input:{raw_data}
"""

def extract_text_from_image(img_path: str) -> str:
    """
    Uses Gemini 1.5 Flash to extract and interpret text from a handwritten image.
    """
    with open(img_path, "rb") as f:
        image_data = f.read()

    image_base64 = base64.b64encode(image_data).decode("utf-8")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": "Extract all handwritten content accurately from this image."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}},
                ],
            }
        ]
    )
    return response.text

def generate_minutes_of_meeting(raw_text: str) -> str:
    """
    Takes raw OCR or text and generates structured MoM.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("gemini_api_key")
    )

    prompt = PromptTemplate(
        input_variables=["raw_data"],
        template=MOM_PROMPT
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response_text  = chain.run({"raw_data": raw_text})
    st.write(response_text)
    return(response_text)