import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import pytesseract
from PIL import Image
import mammoth
import PyPDF2
import io
import json
from typing import Dict, Any

# Set the tesseract path manually
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class MoMGenerator:
    def __init__(self, gemini_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=gemini_api_key,
        )

    def extract_text_from_file(self, uploaded_file) -> str:
        file_type = uploaded_file.type
        try:
            if file_type.startswith('image/'):
                return self._extract_from_image(uploaded_file)
            elif file_type == 'application/pdf':
                return self._extract_from_pdf(uploaded_file)
            elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return self._extract_from_docx(uploaded_file)
            elif file_type == 'text/plain':
                return str(uploaded_file.read(), "utf-8")
            else:
                st.error(f"Unsupported file type: {file_type}")
                return ""
        except Exception as e:
            st.error(f"Error extracting text from file: {str(e)}")
            return ""

    def _extract_from_image(self, uploaded_file) -> str:
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)

    def _extract_from_pdf(self, uploaded_file) -> str:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, uploaded_file) -> str:
        result = mammoth.extract_raw_text(uploaded_file)
        return result.value

    def generate_mom_prompt(self) -> str:
        return "You are an expert meeting minutes analyzer. Extract and structure meeting information from the provided text into a standardized format. OUTPUT FORMAT: JSON {...}"

    def process_text_with_gemini(self, text: str) -> Dict[str, Any]:
        prompt = self.generate_mom_prompt() + f"\n\n{text}"
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            response_text = response.content
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text
            return json.loads(json_text)
        except Exception as e:
            st.error(f"Error processing with Gemini: {str(e)}")
            return self._get_default_structure()

    def _get_default_structure(self) -> Dict[str, Any]:
        return {
            "meeting_header": {
                "project_name": "Not specified",
                "meeting_subject": "Not specified",
                "meeting_date": "Not specified",
                "meeting_time": "Not specified",
                "venue": "Not specified",
                "mom_number": "Not specified",
                "minutes_by": "Not specified"
            },
            "participants": [],
            "discussion_points": [],
            "additional_info": {
                "distribution_list": "Not specified",
                "attachments": "Not specified",
                "next_meeting": {"date": "Not specified", "venue": "Not specified"},
                "response_deadline": "Not specified"
            }
        }

    def create_excel_file(self, mom_data: Dict[str, Any]) -> io.BytesIO:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Always write at least one sheet
            if 'meeting_header' in mom_data:
                pd.DataFrame([[k, v] for k, v in mom_data['meeting_header'].items()], columns=['Field', 'Value']).to_excel(writer, sheet_name='Meeting_Info', index=False)
            
            if mom_data.get('participants'):
                pd.DataFrame(mom_data['participants']).to_excel(writer, sheet_name='Participants', index=False)
            
            if mom_data.get('discussion_points'):
                pd.DataFrame(mom_data['discussion_points']).to_excel(writer, sheet_name='Minutes_of_Meeting', index=False)
            
            if 'additional_info' in mom_data:
                additional = mom_data['additional_info']
                add_data = [
                    ['Distribution List', additional.get('distribution_list', 'Not specified')],
                    ['Attachments', additional.get('attachments', 'Not specified')],
                    ['Next Meeting Date', additional.get('next_meeting', {}).get('date', 'Not specified')],
                    ['Next Meeting Venue', additional.get('next_meeting', {}).get('venue', 'Not specified')],
                    ['Response Deadline', additional.get('response_deadline', 'Not specified')]
                ]
                pd.DataFrame(add_data, columns=['Field', 'Value']).to_excel(writer, sheet_name='Additional_Info', index=False)
            
            # Fallback: if still no sheets written, write dummy data
            if not writer.sheets:
                pd.DataFrame([["No data extracted"]], columns=["Message"]).to_excel(writer, sheet_name="Summary", index=False)

        output.seek(0)
        return output
