# AI Agent Builder

Generate custom AI agent system prompts from any company website. Crawls the site, extracts business info with GPT-4, and outputs a ready-to-use prompt for voice or chat AI agents.

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
2. **AI Extraction** — GPT-4 extracts company info, hours, contact details, products, pricing, FAQs
3. **Prompt Generation** — Outputs a complete AI agent system prompt with response guidelines, escalation triggers, and example interactions

## Project Structure

```
├── app.py              # Flask web server
├── crawler.py          # Smart multi-page crawler (crawl4ai)
├── extractor.py        # GPT-4 business info extraction
├── prompt_generator.py # Agent prompt generation
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
