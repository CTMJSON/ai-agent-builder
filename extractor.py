import os
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class FAQ(BaseModel):
    question: str = Field(description="The question")
    answer: str = Field(description="The answer")

class BusinessInfo(BaseModel):
    company_name: str = Field(description="The name of the company")
    description: str = Field(description="Brief description of what the company does")
    services: str = Field(description="List of services offered, separated by newlines")
    products: str = Field(description="List of products offered, separated by newlines")
    hours: str = Field(description="Business hours, or 'Not found' if not available")
    phone: str = Field(description="Main phone number, or 'Not found' if not available")
    email: str = Field(description="Main email address, or 'Not found' if not available")
    address: str = Field(description="Physical address, or 'Not found' if not available")
    website: str = Field(description="Website URL")
    faqs: str = Field(description="Frequently asked questions with answers, separated by newlines, or 'Not found' if not available")
    pricing: str = Field(description="Pricing information, or 'Not found' if not available")
    policies: str = Field(description="Key policies like returns or cancellations, or 'Not found' if not available")
    team: str = Field(description="Key team members or departments, or 'Not found' if not available")
    additional_info: str = Field(description="Any other relevant information, or 'Not found' if not available")

class BusinessExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def extract_business_info(self, pages: dict[str, str]) -> BusinessInfo:
        combined_content = ""
        for url, content in pages.items():
            combined_content += f"\n\n=== Page: {url} ===\n{content[:8000]}"
        
        combined_content = combined_content[:15000]
        
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at extracting business information from website content.
                    Extract all relevant information that would help an AI agent answer customer questions.
                    Be thorough but concise. If information is not found, leave fields empty or null."""
                },
                {
                    "role": "user",
                    "content": f"Extract business information from this website content:\n\n{combined_content}"
                }
            ],
            response_format=BusinessInfo,
            temperature=0.3,
        )
        
        return response.choices[0].message.parsed

def extract_info(pages: dict[str, str]) -> BusinessInfo:
    extractor = BusinessExtractor()
    return extractor.extract_business_info(pages)
