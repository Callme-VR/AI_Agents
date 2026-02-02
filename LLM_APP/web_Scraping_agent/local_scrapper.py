import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph

st.title("Web scapping Ai agent:")
st.caption("This app allow to Scrape the Websites Using the Ai")

# setup configuration
Graph_config={
    "llm":{
        "model":"ollama/llama3.2",
        "temperature":0,
        "format":"json",
        "base_url":"http://localhost:11434",
        "max_retries": 5,
        "timeout": 30
    },
    "embeddings":{
        "model":"ollama/nomic-embed-text",
         "base_url":"http://localhost:11434"
    },
   "verbose":True
}
url=st.text_input("Enter The Url of the Websites You want to Scrape")
user_prompt=st.text_input("What you want the Ai to Scrape from the Websites")
smart_scaph_agent=SmartScraperGraph(
    prompt=user_prompt,
    source=url,
    config=Graph_config
)

if st.button("Scrape"):
    result=smart_scaph_agent.run()
    st.write(result)

