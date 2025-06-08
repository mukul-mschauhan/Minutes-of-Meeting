# File processing module for MoM Generator
# Handles extraction of text from various file formats

import pytesseract
from PIL import Image
import mammoth
import PyPDF2
import io
import streamlit as st
from typing import List, Union
from config import Config

class FileProcessor:
    """Handles file processing and text extraction"""
    
    def __init__(self):
        """Initialize file processor with configuration"""
        self.config = Config()
        # Set tesseract path if specified
        tesseract_path = self.config.get_tesseract_path()
        if tesseract_path != 'tesseract':
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def process_multiple_files(self, uploaded_files: List) -> str:
        """Process multiple uploaded files and combine text"""
        combined_text = ""
        
        for file in uploaded_files:
            try:
                st.info(f"Processing: {file.name}")
                text = self.extract_text_from_file(file)
                if text.strip():
                    combined_text += f"\n\n--- Content from {file.name} ---\n{text}"
                else:
                    st.warning(f"No text extracted from {file.name}")
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                continue
        
        return combined_text
    
    def extract_text_from_file(self, uploaded_file) -> str:
        """Extract text from various file formats"""
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
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            st.error(f"Error extracting text from file: {str(e)}")
            return ""
    
    def _extract_from_image(self, uploaded_file) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(uploaded_file)
            # Enhance image for better OCR
            image = self._preprocess_image(image)
            text = pytesseract.image_to_string(image, config=self.config.TESSERACT_CONFIG)
            return text
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def _extract_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                except Exception as e:
                    st.warning(f"Could not extract text from page {page_num + 1}: {str(e)}")
                    continue
            return text
        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def _extract_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX"""
        try:
            result = mammoth.extract_raw_text(uploaded_file)
            if result.messages:
                for message in result.messages:
                    st.info(f"DOCX processing note: {message}")
            return result.value
        except Exception as e:
            raise Exception(f"DOCX processing failed: {str(e)}")
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance contrast and brightness for better OCR
            from PIL import ImageEnhance
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            return image
        except Exception:
            # Return original image if preprocessing fails
            return image
    
    def validate_file(self, uploaded_file) -> bool:
        """Validate uploaded file"""
        # Check file type
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in self.config.SUPPORTED_FILE_TYPES:
            st.error(f"Unsupported file type: {file_extension}")
            return False
        
        # Check file size
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if file_size_mb > self.config.MAX_FILE_SIZE_MB:
            st.error(f"File size ({file_size_mb:.1f}MB) exceeds limit ({self.config.MAX_FILE_SIZE_MB}MB)")
            return False
        
        return True
    
    def get_file_info(self, uploaded_file) -> dict:
        """Get information about uploaded file"""
        return {
            'name': uploaded_file.name,
            'type': uploaded_file.type,
            'size': len(uploaded_file.getvalue()),
            'size_mb': len(uploaded_file.getvalue()) / (1024 * 1024)
        }