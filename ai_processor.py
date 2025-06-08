# AI processing module for MoM Generator
# Handles interaction with Gemini AI for text processing


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import json
import streamlit as st
from typing import Dict, Any
from config import Config, PromptTemplates

class AIProcessor:
    """Handles AI processing using Gemini"""
    
    def __init__(self, api_key: str):
        """Initialize AI processor with API key"""
        self.config = Config()
        self.prompt_templates = PromptTemplates()
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.config.GEMINI_MODEL,
                google_api_key=api_key,
                temperature=self.config.GEMINI_TEMPERATURE
            )
        except Exception as e:
            st.error(f"Failed to initialize Gemini AI: {str(e)}")
            raise
    
    def process_text_to_mom(self, text: str) -> Dict[str, Any]:
        """Process extracted text with Gemini to generate structured MoM"""
        if not text.strip():
            st.warning("No text provided for processing")
            return self._get_default_structure()
        
        try:
            # Create prompt with input text
            prompt = self.prompt_templates.get_extraction_prompt(text)
            
            # Process with Gemini
            with st.spinner("Processing with Gemini AI..."):
                response = self.llm.invoke([HumanMessage(content=prompt)])
            
            # Extract and parse JSON response
            mom_data = self._parse_gemini_response(response.content)
            
            # Validate and clean the data
            mom_data = self._validate_and_clean_data(mom_data)
            
            return mom_data
            
        except Exception as e:
            st.error(f"Error processing with Gemini: {str(e)}")
            return self._get_default_structure()
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Gemini"""
        try:
            # Try to extract JSON from response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                # Try to find JSON object in response
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                json_text = response_text[start_idx:end_idx]
            else:
                json_text = response_text
            
            # Parse JSON
            parsed_data = json.loads(json_text)
            return parsed_data
            
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON response: {str(e)}")
            st.error(f"Response text: {response_text[:500]}...")
            return self._get_default_structure()
        except Exception as e:
            st.error(f"Error parsing Gemini response: {str(e)}")
            return self._get_default_structure()
    
    def _validate_and_clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the extracted MoM data"""
        try:
            # Ensure all required keys exist
            validated_data = self._get_default_structure()
            
            # Update with extracted data
            if isinstance(data, dict):
                # Meeting header
                if 'meeting_header' in data and isinstance(data['meeting_header'], dict):
                    validated_data['meeting_header'].update(data['meeting_header'])
                
                # Participants
                if 'participants' in data and isinstance(data['participants'], list):
                    validated_data['participants'] = self._validate_participants(data['participants'])
                
                # Discussion points
                if 'discussion_points' in data and isinstance(data['discussion_points'], list):
                    validated_data['discussion_points'] = self._validate_discussion_points(data['discussion_points'])
                
                # Additional info
                if 'additional_info' in data and isinstance(data['additional_info'], dict):
                    validated_data['additional_info'].update(data['additional_info'])
            
            return validated_data
            
        except Exception as e:
            st.error(f"Error validating data: {str(e)}")
            return self._get_default_structure()
    
    def _validate_participants(self, participants: list) -> list:
        """Validate and clean participants data"""
        validated_participants = []
        
        for i, participant in enumerate(participants):
            if isinstance(participant, dict):
                validated_participant = {
                    'sl_no': participant.get('sl_no', i + 1),
                    'consultant_organization': participant.get('consultant_organization', self.config.DEFAULT_VALUES['not_specified']),
                    'participant_name': participant.get('participant_name', self.config.DEFAULT_VALUES['not_specified'])
                }
                validated_participants.append(validated_participant)
        
        return validated_participants
    
    def _validate_discussion_points(self, discussion_points: list) -> list:
        """Validate and clean discussion points data"""
        validated_points = []
        
        for i, point in enumerate(discussion_points):
            if isinstance(point, dict):
                validated_point = {
                    'sl_no': point.get('sl_no', i + 1),
                    'topic_head': point.get('topic_head', f"Discussion Point {i + 1}"),
                    'discussion_decision': point.get('discussion_decision', self.config.DEFAULT_VALUES['not_specified']),
                    'responsible_team': point.get('responsible_team', self.config.DEFAULT_VALUES['not_specified']),
                    'target_date': point.get('target_date', self.config.DEFAULT_VALUES['for_information'])
                }
                validated_points.append(validated_point)
        
        return validated_points
    
    def _get_default_structure(self) -> Dict[str, Any]:
        """Return default MoM structure if processing fails"""
        return {
            "meeting_header": {
                "project_name": self.config.DEFAULT_VALUES['not_specified'],
                "meeting_subject": self.config.DEFAULT_VALUES['not_specified'],
                "meeting_date": self.config.DEFAULT_VALUES['not_specified'],
                "meeting_time": self.config.DEFAULT_VALUES['not_specified'],
                "venue": self.config.DEFAULT_VALUES['not_specified'],
                "mom_number": self.config.DEFAULT_VALUES['not_specified'],
                "minutes_by": self.config.DEFAULT_VALUES['not_specified']
            },
            "participants": [],
            "discussion_points": [],
            "additional_info": {
                "distribution_list": self.config.DEFAULT_VALUES['not_specified'],
                "attachments": self.config.DEFAULT_VALUES['not_specified'],
                "next_meeting": {
                    "date": self.config.DEFAULT_VALUES['not_specified'], 
                    "venue": self.config.DEFAULT_VALUES['not_specified']
                },
                "response_deadline": self.config.DEFAULT_VALUES['not_specified']
            }
        }
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate Gemini API key"""
        if not api_key or api_key.strip() == "":
            return False
        
        try:
            # Test the API key with a simple request
            test_llm = ChatGoogleGenerativeAI(
                model=self.config.GEMINI_MODEL,
                google_api_key=api_key,
                temperature=0.1
            )
            
            test_response = test_llm.invoke([HumanMessage(content="Test connection")])
            return True
            
        except Exception as e:
            st.error(f"API key validation failed: {str(e)}")
            return False