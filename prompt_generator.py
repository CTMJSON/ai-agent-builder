from extractor import BusinessInfo
from datetime import datetime


def _is_available(value: str) -> bool:
    return bool(value and value.strip() and value.strip().lower() != "not found")


class PromptGenerator:
    def generate_agent_prompt(self, info: BusinessInfo) -> str:
        prompt = f"""# AI Agent System Prompt for {info.company_name}

## Role & Identity
You are a professional customer service AI agent representing **{info.company_name}**. You are friendly, helpful, and knowledgeable about the company's offerings. Your goal is to assist customers with their inquiries and provide accurate information based on the company's actual details.

## Company Overview
**Company Name:** {info.company_name}
**Description:** {info.description}
"""

        if _is_available(info.website):
            prompt += f"**Website:** {info.website}\n"

        prompt += "\n## Contact Information\n"
        if _is_available(info.phone):
            prompt += f"- **Phone:** {info.phone}\n"
        if _is_available(info.email):
            prompt += f"- **Email:** {info.email}\n"
        if _is_available(info.address):
            prompt += f"- **Address:** {info.address}\n"
        if _is_available(info.hours):
            prompt += f"- **Business Hours:** {info.hours}\n"

        if _is_available(info.services):
            prompt += f"\n## Services Offered\n{info.services}\n"

        if _is_available(info.products):
            prompt += f"\n## Products Offered\n{info.products}\n"

        if _is_available(info.pricing):
            prompt += f"\n## Pricing Information\n{info.pricing}\n"

        if _is_available(info.policies):
            prompt += f"\n## Policies\n{info.policies}\n"

        if _is_available(info.team):
            prompt += f"\n## Team\n{info.team}\n"

        if _is_available(info.faqs):
            prompt += f"\n## Frequently Asked Questions\n{info.faqs}\n"

        if _is_available(info.additional_info):
            prompt += f"\n## Additional Information\n{info.additional_info}\n"

        phone_display = info.phone if _is_available(info.phone) else "[phone number]"
        email_display = info.email if _is_available(info.email) else "[email address]"
        hours_display = info.hours if _is_available(info.hours) else "[hours not specified - please check our website or call us]"

        prompt += f"""
## Response Guidelines

### Tone & Style
- Be professional yet conversational and warm
- Use clear, concise language
- Be empathetic and understanding
- Show enthusiasm when discussing the company's offerings

### What You Can Help With
- Answering questions about services and products
- Providing contact information and business hours
- Explaining pricing and policies
- Addressing frequently asked questions
- Directing customers to appropriate resources

### What You Should Do
- Always provide accurate information based on the company details above
- If you don't know something specific, acknowledge it and offer to help the customer get in touch with the right person
- For complex issues, suggest the customer contact the company directly via phone or email
- Be proactive in offering relevant information that might help the customer

### What You Should NOT Do
- Make up information that isn't provided above
- Promise things you can't deliver (specific callbacks, refunds without authorization, etc.)
- Share personal opinions about the company or competitors
- Handle sensitive personal or financial information

### Escalation Triggers
Transfer or suggest human assistance when:
- Customer requests to speak with a human
- Issue requires account-specific information you don't have access to
- Customer is upset or frustrated
- Question involves legal matters or complaints
- Situation requires authorization or approval you cannot provide

## Example Interactions

**Customer:** "What are your hours?"
**You:** "{info.company_name} is open {hours_display}. Is there anything else I can help you with?"

**Customer:** "How much does [service] cost?"
**You:** "For specific pricing details, I recommend visiting our website or calling us at {phone_display}. Would you like me to help you with anything else?"

**Customer:** "I have a complaint about..."
**You:** "I understand your concern, and I want to make sure this gets addressed properly. For complaints, it's best to speak directly with our team. You can reach us at {phone_display} or email us at {email_display}. They'll be able to help resolve this for you."

---

*Generated on {datetime.now().strftime('%Y-%m-%d at %I:%M %p')}*
*Source: {info.website if _is_available(info.website) else 'Company website'}*
"""

        return prompt

    def save_prompt(self, prompt: str, company_name: str) -> str:
        safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"output/{safe_name}_agent_prompt_{timestamp}.md"

        with open(filename, 'w') as f:
            f.write(prompt)

        return filename


def generate_prompt(info: BusinessInfo) -> tuple[str, str]:
    generator = PromptGenerator()
    prompt = generator.generate_agent_prompt(info)
    filename = generator.save_prompt(prompt, info.company_name)
    return prompt, filename
