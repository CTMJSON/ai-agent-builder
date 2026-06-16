import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from crawler import crawl_website
from extractor import extract_info
from prompt_generator import generate_prompt

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'Please provide a URL'}), 400
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        print(f"Crawling {url}...")
        pages = crawl_website(url)
        
        if not pages:
            return jsonify({'error': 'Could not crawl any content from the website'}), 400
        
        print(f"Crawled {len(pages)} pages")
        print("Extracting business information...")
        business_info = extract_info(pages)
        
        print("Generating agent prompt...")
        prompt, filename = generate_prompt(business_info)
        
        print(f"Prompt saved to {filename}")
        
        return render_template('result.html', 
                             prompt=prompt, 
                             filename=filename,
                             company_name=business_info.company_name)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        exit(1)
    
    port = int(os.getenv('PORT', 5001))
    print(f"Starting AI Agent Builder...")
    print(f"Open http://localhost:{port} in your browser")
    app.run(debug=False, host='0.0.0.0', port=port)
