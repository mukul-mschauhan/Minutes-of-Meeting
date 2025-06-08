
# Configuration module for MoM Generator
# Contains all configuration settings and constants

import os
from typing import List, Dict, Any

class Config:
    """Configuration class for MoM Generator"""
    
    # File upload settings
    SUPPORTED_FILE_TYPES: List[str] = [
        'txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'
    ]
    
    MAX_FILE_SIZE_MB: int = 200
    
    # API settings
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_TEMPERATURE: float = 0.1
    
    # OCR settings
    TESSERACT_CONFIG: str = r'--oem 3 --psm 6'
    
    # Excel settings
    EXCEL_ENGINE: str = 'openpyxl'
    
    # Sheet names for Excel output
    SHEET_NAMES: Dict[str, str] = {
        'meeting_info': 'Meeting_Info',
        'participants': 'Participants',
        'minutes': 'Minutes_of_Meeting',
        'additional_info': 'Additional_Info'
    }
    
    # Date format
    DATE_FORMAT: str = "%d-%m-%Y"
    
    # Default values for missing data
    DEFAULT_VALUES: Dict[str, str] = {
        'not_specified': 'Not specified',
        'for_information': 'For Information'
    }
    
    @staticmethod
    def get_gemini_api_key() -> str:
        """Get Gemini API key from environment variables"""
        return os.getenv('GOOGLE_API_KEY', '')
    
    @staticmethod
    def get_tesseract_path() -> str:
        """Get Tesseract executable path"""
        return os.getenv('TESSERACT_CMD', 'tesseract')

class PromptTemplates:
    """Prompt templates for Gemini AI"""
    
    MAIN_PROMPT = """
    You are an expert meeting minutes analyzer. Extract and structure meeting information from the provided text into a standardized format.

    **REQUIRED OUTPUT FORMAT (JSON):**
    ```json
    {
        "meeting_header": {
            "project_name": "Extract project name",
            "meeting_subject": "Extract meeting subject/purpose",
            "meeting_date": "DD-MM-YYYY format",
            "meeting_time": "Start time - End time",
            "venue": "Meeting location",
            "mom_number": "Meeting reference number if available",
            "minutes_by": "Person who recorded minutes"
        },
        "participants": [
            {
                "sl_no": 1,
                "consultant_organization": "Organization/Company name",
                "participant_name": "Full name of participant"
            }
        ],
        "discussion_points": [
            {
                "sl_no": 1,
                "topic_head": "Brief topic title",
                "discussion_decision": "Detailed description of discussion and decisions made",
                "responsible_team": "Team/person responsible for action",
                "target_date": "DD-MM-YYYY or 'For Information'"
            }
        ],
        "additional_info": {
            "distribution_list": "List of people to receive these minutes",
            "attachments": "Any attachments mentioned",
            "next_meeting": {
                "date": "Next meeting date if mentioned",
                "venue": "Next meeting venue if mentioned"
            },
            "response_deadline": "Deadline for comments on minutes"
        }
    }
    ```

    **EXTRACTION GUIDELINES:**
    1. **Meeting Header**: Extract all basic meeting information
    2. **Participants**: List all attendees with their organizations
    3. **Discussion Points**: Each point should have:
       - Sequential numbering
       - Clear topic heading
       - Complete discussion summary and decisions
       - Responsible party identification
       - Target completion date or "For Information"
    4. **Dates**: Convert all dates to DD-MM-YYYY format
    5. **Missing Information**: Use "Not specified" for unavailable data
    6. **Action Items**: Clearly identify who is responsible for what
    7. **Decisions**: Distinguish between decisions made and discussions held

    **INPUT TEXT TO ANALYZE:**
    """
    
    @classmethod
    def get_extraction_prompt(cls, text: str) -> str:
        """Get complete prompt with input text"""
        return cls.MAIN_PROMPT + f"\n\n{text}"