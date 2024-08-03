# Research Report Generator

## Overview

The Research Report Generator is a web application built using Flask that allows users to generate detailed research reports based on a given topic. The application leverages OpenAI and YOU.com API to fetch and compile information into a comprehensive report.

## Features

- **Topic-based Research:** Users can input a topic, and the application will generate relevant queries.
- **Automated Report Generation:** The application fetches information from YOU.com, merges the responses, and uses OpenAI to generate a detailed HTML report.
- **Downloadable Reports:** Generated reports are saved as HTML files and can be accessed through a provided link.

## Prerequisites

- Python 3.7+
- Flask
- Requests
- OpenAI Python Client

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/research-report-generator.git
    cd research-report-generator
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Your API Keys:**

    - OpenAI API Key
    - YOU.com API Key

    Update the `app.py` file with your API keys.

## Folder Structure

```
project_folder/
│
├── static/
│   └── (generated HTML reports will be saved here)
│
├── templates/
│   └── index.html
│
├── app.py (your Flask application)
└── requirements.txt
```
## Algorithm

The following steps outline the algorithm used in the `app.py` file to generate the research report:

1. **Receive User Input:**
    - The user inputs a research topic via a form on the web page.

2. **Generate Queries:**
    - The `generate_queries` function is called with the input topic.
    - A prompt is sent to OpenAI to generate three relevant search queries based on the topic.
    - The function returns these queries in JSON format.

3. **Fetch Research Data:**
    - The `research_query` function is called for each of the generated queries.
    - This function uses the YOU.com API to fetch snippets of information for each query.
    - The responses are collected and returned as JSON.

4. **Merge Responses:**
    - The `merge_responses` function combines the snippets of information from the YOU.com API responses into a single string of merged content.

5. **Generate Report:**
    - The `generate_report` function is called with the topic and merged content.
    - A prompt is sent to OpenAI to generate a detailed HTML report based on the merged content.
    - The function returns the generated HTML report as a string.

6. **Save Report:**
    - The generated HTML report is saved as a file in the `static` folder with a filename based on the topic.

7. **Provide Report Link:**
    - A link to the saved HTML report is generated and returned to the user.
    - The user can click the link to view the detailed research report in a new web page.
## Usage

1. **Run the Flask Application:**

    ```bash
    python app.py
    ```

2. **Open Your Browser:**

    Navigate to `http://127.0.0.1:5000` to access the Research Report Generator.

3. **Generate a Report:**

    - Enter the topic you want to research.
    - Click on "Generate Report."
    - Once the report is generated, click on the provided link to view the report.

## Code Explanation

### `templates/index.html`

This file contains the HTML template for the web application. It includes a form for entering the research topic and a section to display the generated report link.

### `app.py`

This file contains the Flask application logic, including:

- **Home Route:** Renders the `index.html` template.
- **Generate Report Route:** Handles the form submission, generates queries, fetches research data, merges content, generates the report using OpenAI, and saves the report as an HTML file in the `static` folder.


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

