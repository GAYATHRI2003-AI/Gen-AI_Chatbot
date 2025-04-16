# Gen-AI_Chatbot

# 🎓 Overseas Consultancy Bot 🌍  
**Your friendly AI-powered study abroad advisor!**

This is a personalized AI chatbot built using **Streamlit**, **LangChain**, and **Google Gemini Pro** to help students explore **universities**, **scholarships**, **visa options**, and **job markets** for studying abroad.  

It acts like a human-like **student counselor**, guiding users through tailored recommendations based on their profile, academic background, and financial situation.

---

## 🚀 Features

- ✅ Warm onboarding: asks for name, academics, goals, and budget  
- ✅ Real-time web search using **DuckDuckGo** to find:  
  - 📚 University programs  
  - 🎓 Scholarships  
  - 🛂 Visa requirements  
  - 💼 Job market trends  
- ✅ Categorizes universities into: **Dream**, **Reach**, and **Safe**  
- ✅ Gives advice on **application deadlines**, **admission criteria**, and **funding options**  
- ✅ Friendly and supportive tone throughout the chat  

---

## 🧠 Technologies Used

| Tool                      | Purpose                                 |
|---------------------------|-----------------------------------------|
| `Streamlit`               | UI for chat                             |
| `LangChain`               | Agent and tool orchestration            |
| `Google Gemini Pro`       | Chat model for AI responses             |
| `DuckDuckGo Search API`   | Web search for real-time information    |
| `LangGraph`               | Workflow and agent state management     |
| `MemorySaver`             | Maintains memory of past messages       |

---

## 📦 Installation

Install the required Python libraries:

```bash
pip install streamlit langchain langgraph langchain-google-genai duckduckgo-search

📦 Required Libraries
To run this bot, install the following dependencies:
pip install streamlit langchain langgraph langchain-google-genai duckduckgo-search

If you encounter SSL issues with duckduckgo-search, try:
pip install duckduckgo-search --upgrade --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org

Note: Set the environment variable for Gemini API Replace with your Google AI Studio API key.

## ✨ How It Works: 
  Loads an LLM (Gemini Pro) using your API key.
  Creates tools (web_search, scholarship_search, visa_info_search, job_market_analysis) using LangChain’s Tool.from_function.
  Builds a LangGraph state machine to manage message history and agent calls.
  Uses Streamlit to render a clean, interactive chat interface.
  On user input:
    Appends user message to state
    Agent processes it with memory + tools
    Outputs a helpful response
    Outputs are styled in a chat bubble format.
