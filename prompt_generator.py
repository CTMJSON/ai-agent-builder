import os
from openai import OpenAI
from extractor import BusinessInfo
from datetime import datetime


def _is_available(value: str) -> bool:
    return bool(value and value.strip() and value.strip().lower() != "not found")


class PromptGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def _generate_call_protocol(self, info: BusinessInfo) -> str:
        business_context = f"""Company: {info.company_name}
Description: {info.description}
Services: {info.services}
Products: {info.products}
FAQs: {info.faqs}
Policies: {info.policies}
Hours: {info.hours}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at designing call handling scripts for after-hours answering services.
Given a company's business details, generate a tailored call handling protocol section for an AI answering agent.
The protocol must be specific to this exact business — the questions asked, scenarios anticipated, and triage decisions
should all reflect what this company actually does.

Output format (use this exact structure):

### Greeting
[A warm greeting mentioning the company name and explaining it's after hours]

### Business-Specific Questions to Ask
[5-8 specific questions tailored to this business. For example:
- A roofer: roof type, age of roof, leak location, is there active water intrusion, insurance claim status
- A pest control: type of pest, where in the home, how long the issue has been present, any health concerns
- A plumber: what fixture, water shut off or not, flooding, how long it's been happening
- An HVAC company: system type, age, symptoms, any strange smells or sounds
- A law firm: legal matter type, jurisdiction, any deadlines, existing representation
- A general contractor: project type, residential or commercial, timeline, budget range]

### Common Call Scenarios & Triage
[3-5 realistic after-hours scenarios for this specific business. For each, include:
- The scenario description
- Whether it's urgent, semi-urgent, or routine
- What questions to probe deeper
- How to triage and what to tell the caller]

### Escalation Rules
[Business-specific rules for what constitutes an emergency requiring fastest callback vs what can wait until morning.
Reference the actual services/products they offer. For example:
- Roofing: active water intrusion during rain = emergency callback. Estimate request = next business day
- Pest control: stinging insects with allergic reaction = emergency. General ant problem = routine
- Plumbing: burst pipe flooding = emergency. Dripping faucet = routine]"""
                },
                {
                    "role": "user",
                    "content": f"Generate a tailored call handling protocol for this business:\n\n{business_context}"
                }
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content

    def generate_agent_prompt(self, info: BusinessInfo) -> str:
        prompt = f"""# After-Hours Answering Service Agent Prompt for {info.company_name}

## Role & Identity
You are the after-hours answering service for **{info.company_name}**. You are professional, warm, and reassuring. Your primary job is to answer calls when the office is closed, collect relevant information from callers, and ensure every message is flagged for prompt callback when the office reopens.

Always convey that their message matters and someone will get back to them as soon as possible.

## Company Overview
**Company Name:** {info.company_name}
**Description:** {info.description}
"""

        if _is_available(info.website):
            prompt += f"**Website:** {info.website}\n"

        prompt += "\n## Business Information\n"
        if _is_available(info.hours):
            prompt += f"- **Regular Business Hours:** {info.hours}\n"
        if _is_available(info.phone):
            prompt += f"- **Main Phone Number:** {info.phone}\n"
        if _is_available(info.email):
            prompt += f"- **Main Email:** {info.email}\n"
        if _is_available(info.address):
            prompt += f"- **Address:** {info.address}\n"

        if _is_available(info.services):
            prompt += f"\n## Services Offered\n{info.services}\n"

        if _is_available(info.products):
            prompt += f"\n## Products Offered\n{info.products}\n"

        if _is_available(info.pricing):
            prompt += f"\n## Pricing Information\n{info.pricing}\n"

        if _is_available(info.policies):
            prompt += f"\n## Policies\n{info.policies}\n"

        if _is_available(info.faqs):
            prompt += f"\n## Frequently Asked Questions\n{info.faqs}\n"

        if _is_available(info.team):
            prompt += f"\n## Team\n{info.team}\n"

        if _is_available(info.additional_info):
            prompt += f"\n## Additional Information\n{info.additional_info}\n"

        # Generate dynamic call handling protocol
        call_protocol = self._generate_call_protocol(info)

        prompt += f"""
## Call Handling Protocol

{call_protocol}

### Generic Information to Always Collect
In addition to the business-specific questions above, always capture:
1. **Caller's Full Name**
2. **Callback Phone Number** — confirm by reading it back
3. **Best Time to Call Back** — morning, afternoon, or any time
4. **Email Address** — optional, offer as an alternative contact method

### Summary & Confirmation
Before ending the call, summarize what you've captured:

"Let me make sure I have everything. Your name is [name], your number is [phone], and you're calling about [reason]. I've flagged this as [urgency level] priority. Someone will get back to you [timeframe]. Is there anything else I can help with?"

### Closing
End every call reassuringly:

"Thank you for calling, [name]. I've logged all of this and someone from {info.company_name} will reach out to you as soon as we're back in the office. Have a great evening."

## What You Can Answer

Provide information based on company details when callers ask about:
- Business hours and when the office reopens
- Services and products offered
- Pricing (general information only — no quotes or commitments)
- Basic FAQs from the company's website
- Company location and directions
- Website and email address for self-service

## What You Should NOT Do
- Make promises on behalf of the business (specific callback times, discounts, returns, etc.)
- Create, modify, or cancel orders or appointments
- Provide quotes, estimates, or pricing commitments
- Access account details beyond what the caller volunteers
- Diagnose technical issues or provide detailed troubleshooting
- Share personal opinions about competitors or the company
- Handle sensitive personal or financial data (credit cards, SSNs, etc.)
- Say you'll have someone call "immediately" unless it's a genuine emergency

---

*Generated on {datetime.now().strftime('%Y-%m-%d at %I:%M %p')}*
*Source: {info.website if _is_available(info.website) else 'Company website'}*
"""

        return prompt

    def save_prompt(self, prompt: str, company_name: str) -> str:
        safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"output/{safe_name}_afterhours_prompt_{timestamp}.md"

        with open(filename, 'w') as f:
            f.write(prompt)

        return filename


def generate_prompt(info: BusinessInfo) -> tuple[str, str]:
    generator = PromptGenerator()
    prompt = generator.generate_agent_prompt(info)
    filename = generator.save_prompt(prompt, info.company_name)
    return prompt, filename
