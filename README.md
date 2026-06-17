
# After-Hours Answering Service Builder

Generate AI agent prompts for fielding after-hours calls from any company website. Crawls the site, extracts business info with ChatGPT, and outputs a ready-to-use prompt that collects caller information and guarantees a callback.
=======
<img width="1214" height="780" alt="Screenshot 2026-06-16 at 5 01 31 PM" src="https://github.com/user-attachments/assets/adeb9689-e425-4722-b30c-e68190908c6b" />



# AI Agent Builder

Generate custom AI agent system prompts from any company website. Crawls the site, extracts business info with GPT, and outputs a ready-to-use prompt for voice or chat AI agents.
>>>>>>> 092a92f544c048c801e89519291b94e4f699bbcd

## Quick Start

```bash
cd ai-agent-builder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
crawl4ai-setup
```

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
```

```bash
python app.py
```

Open **http://localhost:5001** in your browser.

## How It Works

1. **Smart Crawling** — Enter a URL, the app crawls the homepage and key pages (about, contact, FAQ, services, products)
<<<<<<< HEAD
2. **AI Extraction** — GPT-4 extracts company info, hours, contact details, products, pricing, FAQs
3. **Prompt Generation** — Outputs an after-hours answering service prompt with call handling protocol, information collection checklist, escalation triggers, and sample dialogue

## What the Prompt Does

- Answers calls when the office is closed
- Collects caller name, phone number, reason for calling, and urgency
- Reassures callers their message will be returned ASAP
- Answers basic questions using real website content
- Escalates urgent matters appropriately
=======
2. **AI Extraction** — ChatGPT extracts company info, hours, contact details, products, pricing, FAQs
3. **Prompt Generation** — Outputs a complete AI agent system prompt with response guidelines, escalation triggers, and example interactions
>>>>>>> 092a92f544c048c801e89519291b94e4f699bbcd

## Project Structure

```
├── app.py              # Flask web server
├── crawler.py          # Smart multi-page crawler (crawl4ai)
<<<<<<< HEAD
├── extractor.py        # GPT-4 business info extraction
├── prompt_generator.py # After-hours agent prompt generation
=======
├── extractor.py        # ChatGPT business info extraction
├── prompt_generator.py # Agent prompt generation
>>>>>>> 092a92f544c048c801e89519291b94e4f699bbcd
├── templates/
│   ├── index.html      # Input form
│   └── result.html     # Generated prompt display
├── static/
│   └── style.css       # UI styling
└── output/             # Saved prompts
```

## Requirements

- Python 3.12+
- OpenAI API key
- Playwright Chromium browser (installed via `crawl4ai-setup`)

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Crawl4AI](https://github.com/unclecode/crawl4ai) — Web crawling
- [OpenAI](https://platform.openai.com/) — LLM extraction

## License

MIT
