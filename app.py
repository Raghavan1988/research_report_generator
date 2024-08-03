from flask import Flask, request, jsonify, render_template, url_for
import requests
import json
from openai import OpenAI
client = OpenAI()

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Set your OpenAI and YOU.com API keys
you_com_api_key = ''

def generate_queries(topic):
    prompt = f"You are going to create a research report. Understand the topic {topic}. Inorder to understand the topic, think about the queries that you would issue to a web search. \
    Generate 3 queries and return them in a json format following the schema \
    OUTPUT SHOULD BE STRICTLY JSON \
     Schema: \
       q1:String \
       q2:String \
       q3:String "
    
    response = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role": "system", "content": "You are an assistant who is going to research on a TOPIC"},{"role": "user", "content": prompt}, ])
    gpt4o_response =  response.choices[0].message.content
    if "```" in gpt4o_response:
        gpt4o_response = gpt4o_response.replace("```json", "")
        gpt4o_response = gpt4o_response.replace("```", "")

    print(gpt4o_response)
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
        f"https://api.ydc-index.io/search?query={query}",
        params=params,
        headers=headers,
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
    
    response = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role": "system", "content": "You are a RESEARCH REPORT WRITER"},{"role": "user", "content": prompt}, ])
   
    return response.choices[0].message.content.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_report', methods=['POST'])
def generate_report_route():
    data = request.json
    topic = data.get('topic')
    
    if not topic:
        return jsonify({"error": "Please provide a topic"}), 400

    # Generate queries
    queries = generate_queries(topic)
    
    # Research each query using YOU.com
    responses = []
    queries = [queries["q1"],queries["q2"],queries["q3"]]
    for query in queries:
        responses.append(research_query(query))
    
    # Merge responses
    merged_content = " ".join(responses)
    print(merged_content)
    
    # Generate report
    report = generate_report(topic, merged_content)
    print(report)
    report = report.replace("```html","")
    report = report.replace("```","")
    
    # Save report to HTML file in static folder
    report_filename = f'static/report_{topic}.html'
    with open(report_filename, 'w') as file:
        file.write(report)
    
    report_url = url_for('static', filename=f'report_{topic}.html')
    return jsonify({"report_url": report_url})

if __name__ == '__main__':
    app.run(debug=True)
