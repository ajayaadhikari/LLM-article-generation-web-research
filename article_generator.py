import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

#load environment variables
load_dotenv()

# --- Set up LLM and Tools ---
llm = ChatOpenAI(temperature=0.1, model="gpt-4")

search = SerpAPIWrapper()


def scrape_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join(p.get_text() for p in paragraphs)
        return text[:5000] # Limit to 5000 characters
    except Exception as e:
        return ""


def is_relevant(document_text, query):

    prompt = f"""
    You are a helpful assistant. A user asked this query:
    "{query}"
    Below is a document:
    "{document_text}"
    Does the document contain useful information for answering the query? Reply with only "Yes" or "No".
    """
    response = llm.predict(prompt).strip().lower()
    return response.startswith("yes")


def search_and_scrape_relevant_articles(query: str) -> str:
    # st.write("Query: {}".format(query))
    try:
        search_results = search.results(query)
        # st.write(search_results)
        if not isinstance(search_results, dict) or "organic_results" not in search_results:
            st.warning("Search results are not in expected format.")
            return ""

    except Exception as e:
        st.warning(f"Search failed: {e}")
        return ""
    
    # Extract URLs from raw search result string
    urls = [result['link'] for result in search_results.get('organic_results', [])]
    source_urls = [result['source'] for result in search_results.get('organic_results', [])]
    # st.write("All URLs: {}".format(urls))
    urls, source_urls = urls[:10], source_urls[:10]  # Limit to top 10 URLs

    contents = [scrape_url(url) for url in urls]
    # st.write(list(zip(urls, contents)))

    relevant_urls_and_content = []
    for url, source_url, content in zip(urls, source_urls, contents):
        if is_relevant(content, query):
            relevant_urls_and_content.append("url: {}, url_source: {},  webcontent: {}".format(url, source_url, content))
    # st.write("Urls and content: {}".format(relevant_urls_and_content[:2]))
    return "\n\n".join(relevant_urls_and_content)


def create_article(context: str, topic: str) -> str:
    article_generation_prompt = f"""
        Using the following web research context, write an article on the topic: "{topic}".

        Ensure the article is informative, clearly written, and includes key facts found in the research.
        Where appropriate, cite the sources.
        Provide each source with a number in the text and list the number with the corresponding url at this end
        (every url in a new line).
        If the context empty, indicate that online 
        search for relevant articles was unsucessfull and clearly state that your article is based on generic knowledge.

        Sources with URLs and their content:
        {context}
        """
    return llm.predict(article_generation_prompt)

# --- Streamlit UI ---
st.title("🧠 Web Research Article Generator")
topic = st.text_input("Enter a topic for article generation:", "Climate change impact on agriculture in Nepal")

if st.button("Generate Article"):
    with st.spinner("🔍 Researching the web..."):
        context = search_and_scrape_relevant_articles(topic)
    
    if not context.strip():
        context = "No relevant articles were found online."

    with st.spinner("Generating article with ChatGPT..."):
        response = create_article(context, topic)

    st.subheader("📝 Generated Article")
    st.write(response)
