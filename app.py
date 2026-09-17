"""Research Report Generator.

A small Flask application that turns a user-supplied topic into a detailed
HTML research report. It generates search queries with OpenAI, fetches
supporting snippets from the YOU.com API, and asks OpenAI to compile the
merged content into a formatted report served from the ``static`` folder.
"""
from flask import Flask, request, jsonify, render_template, url_for
import os
import re
import logging
import requests
import json
from openai import OpenAI
client = OpenAI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Reject request bodies larger than 1 MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# Set your OpenAI and YOU.com API keys
you_com_api_key = os.environ.get('YOU_COM_API_KEY', '')

# OpenAI model used for both query generation and report writing
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

def generate_queries(topic):
    prompt = f"You are going to create a research report. Understand the topic {topic}. Inorder to understand the topic, think about the queries that you would issue to a web search. \
    Generate 3 queries and return them in a json format following the schema \
    OUTPUT SHOULD BE STRICTLY JSON \
     Schema: \
       q1:String \
       q2:String \
       q3:String "
    
    response = client.chat.completions.create(model=OPENAI_MODEL,messages=[{"role": "system", "content": "You are an assistant who is going to research on a TOPIC"},{"role": "user", "content": prompt}, ])
    gpt4o_response =  response.choices[0].message.content
    if "```" in gpt4o_response:
        gpt4o_response = gpt4o_response.replace("```json", "")
        gpt4o_response = gpt4o_response.replace("```", "")

    logger.info("Generated queries: %s", gpt4o_response)
    try:
        D = json.loads(gpt4o_response.strip())
    except:
        D = {}
        D["q1"] = topic
        return D
    return D

def get_ai_snippets_for_query(query):
    headers = {"X-API-Key": you_com_api_key}
    params = {"query": query}
    return requests.get(
        "https://api.ydc-index.io/search",
        params=params,
        headers=headers,
        timeout=30,
    ).json()

def research_query(query):
    output= get_ai_snippets_for_query(query)
    output_str = json.dumps(output)
    return output_str

def merge_responses(responses):
    merged_content = ""
    for response in responses:
        for result in response.get('results', []):
            merged_content += result.get('snippet', '') + "\n\n"
    return merged_content

def generate_report(topic, merged_content):
    prompt = f"Generate a detailed research report based on the following content: READ the CONTENT below and use HTML to write detailed research report on the TOPIC {topic} \
          Decide several subtopics based on the MERGED CONTENT \
          each subtopic should have a heading and have meaty content with links to web pages \
          The HTML should be MODERN and easy to READ \
          The content should not overflow and should be WORD WRAPPED without having to scroll horizontally\
          Generate Introduction,  several sub topics, Conclusion. \n\n MERGED CONTENT {merged_content}"
    
    response = client.chat.completions.create(model=OPENAI_MODEL,messages=[{"role": "system", "content": "You are a RESEARCH REPORT WRITER"},{"role": "user", "content": prompt}, ])
   
    return response.choices[0].message.content.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/generate_report', methods=['POST'])
def generate_report_route():
    data = request.json
    topic = (data.get('topic') or '').strip()

    if not topic:
        return jsonify({"error": "Please provide a topic"}), 400

    # Generate queries
    queries = generate_queries(topic)
    
    # Research each query using YOU.com
    responses = []
    queries = [queries.get("q1"), queries.get("q2"), queries.get("q3")]
    queries = [q for q in queries if q]
    if not queries:
        queries = [topic]
    for query in queries:
        responses.append(research_query(query))
    
    # Merge responses
    merged_content = " ".join(responses)
    logger.info("Merged content length: %d chars", len(merged_content))
    
    # Generate report
    report = generate_report(topic, merged_content)
    logger.info("Generated report (%d chars)", len(report))
    report = report.replace("```html","")
    report = report.replace("```","")
    
    # Save report to HTML file in static folder
    safe_topic = re.sub(r'[^A-Za-z0-9_-]+', '_', topic).strip('_') or 'report'
    report_filename = f'static/report_{safe_topic}.html'
    with open(report_filename, 'w') as file:
        file.write(report)
    
    report_url = url_for('static', filename=f'report_{safe_topic}.html')
    return jsonify({"report_url": report_url})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
