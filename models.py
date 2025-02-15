from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List

from dotenv import load_dotenv
import os

from prompts import Prompts
import json

load_dotenv()

class ActionItem(BaseModel):
    action_item: str = Field(..., description="Description of the action item")
    assignee: str = Field(..., description="Person responsible for the action item")
    due_date: str = Field(..., description="Due date for the action item")
    status: str = Field(..., description="Current status of the action item")

class MeetingMinute(BaseModel):
    minute: str = Field(..., description="The minute's title or summary")
    speaker: str = Field(..., description="Speaker who provided the minute")
    content: str = Field(..., description="Content of the meeting minute")

class MeetingOfMinutesSchema(BaseModel):
    agenda: str = Field(..., description="Agenda of the meeting")
    participants: List[str] = Field(..., description="List of participants in the meeting")
    summary: str = Field(..., description="Summary of the meeting")
    action_items: List[ActionItem] = Field(..., description="List of action items")
    meeting_minutes: List[MeetingMinute] = Field(..., description="List of meeting minutes")

class MeetingOfMinutesLLM:
    def __init__(self):
        parser = JsonOutputParser(pydantic_object=MeetingOfMinutesSchema)
        prompt = PromptTemplate(
            template=Prompts.SYSTEM_PROMPT,
            input_variables=["transcript"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        model = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-lite-preview-02-05", api_key=os.getenv("GOOGLE_API_KEY"))

        self.chain = prompt | model | parser
    
    def generate_minutes(self, transcript: str) -> dict:
        return json.dumps(self.chain.invoke({"transcript": transcript}), indent=4)

class SpamSchema(BaseModel):
    spam: bool = Field(..., description="True if the transcript is spam, False otherwise")

class SpamDetectorLLM:
    def __init__(self):
        parser = JsonOutputParser(pydantic_object=SpamSchema)
        prompt = PromptTemplate(
            template=Prompts.SPAM_DETECTOR_PROMPT,
            input_variables=["transcript"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        model = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-lite-preview-02-05", api_key=os.getenv("GOOGLE_API_KEY"))
        self.chain = prompt | model | parser
    
    def detect_spam(self, transcript: str) -> dict:
        return json.dumps(self.chain.invoke({"transcript": transcript}), indent=4)
