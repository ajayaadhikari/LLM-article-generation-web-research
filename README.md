# 🧠 Web Research Article Generator

This is a Streamlit-based web application that generates informative articles on user-specified topics by performing real-time web searches and summarizing relevant content using OpenAI's GPT-4.

## 🌟 Why This Project?

This project is a **great example of combining real-time data with a large language model (LLM)** to create useful applications. It demonstrates how to:

- Integrate live web data through a search API (SerpAPI)
- Automatically scrape and filter relevant content
- Use a language model to process and generate high-quality textual output
- Build a user-friendly interface for real-time interaction

Such a pattern is foundational for many modern AI applications like intelligent agents, knowledge assistants, and autonomous research bots.

## 🚀 Features

- 🔍 Real-time web search using **SerpAPI**
- 🧠 Web scraping and relevance filtering with **GPT-4**
- ✍️ Article generation using **OpenAI ChatGPT**
- 📄 User interface built with **Streamlit**

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ajayaadhikari/LLM-article-generation-web-research.git
cd article-generator
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Required Dependencies
pip install -r requirements.txt

### 4. Set Up Environment Variables
Create a .env file in the project root with the following content:

OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key

### 5. Run the app
streamlit run article_generator.py
