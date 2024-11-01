import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import Tool
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState

# Set environment variable for the API key
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBsDwt27kOVM1CrRyTLmHZPCEjswt-6qUM'

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# DuckDuckGo search wrapper
ddg_search = DuckDuckGoSearchAPIWrapper()

# Search tool function
def web_search(query: str) -> str:
    """Searches the web for the provided query."""
    return ddg_search.run(query)

# Create search tool
search_tool = Tool.from_function(
    name="web_search",
    func=web_search,
    description="Searches the web to get information about all the related universities and colleges based on course."
)

def scholarship_search(query: str) -> str:
    """Searches the web for scholarships based on student criteria."""
    return ddg_search.run(f"{query} scholarships")

# Visa info tool
def visa_info_search(query: str) -> str:
    """Searches for visa and immigration information for studying abroad."""
    return ddg_search.run(f"visa information for {query} study abroad")

# Job market analysis tool
def job_market_analysis(query: str) -> str:
    """Searches for job market trends for a specific field in a country."""
    return ddg_search.run(f"job market for {query}")


scholarship_tool = Tool.from_function(
    name="scholarship_search",
    func=scholarship_search,
    description="Searches for scholarships based on student's academic background and financial needs."
)

visa_tool = Tool.from_function(
    name="visa_search",
    func=visa_info_search,
    description="Provides visa information for specific countries."
)

job_market_tool = Tool.from_function(
    name="job_market_analysis",
    func=job_market_analysis,
    description="Analyzes the job market for the student's target field and location."
)



# Create memory store
memory = MemorySaver()

# Create the agent
tools = [search_tool]
agent = create_react_agent(llm, tools, checkpointer=memory)

# Create workflow graph
workflow = StateGraph(MessagesState)

# Define the agent call function
def call_model(state: MessagesState):
    messages = state['messages']
    response = agent.invoke({"messages": messages})
    return {"messages": [response["messages"][-1]]}

# Add edges to workflow graph
workflow.add_node("agent", call_model)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Compile the workflow
app = workflow.compile()

# Define the chatbot conversation
def run_chatbot():
    # Initial counselor prompt
    counselor_prompt_text = '''
    
    You are a friendly and supportive student counselor chatbot named "Overseas Consultancy Bot!" specializing in helping students explore university options worldwide. Think of yourself as a personalized, all-knowing study abroad advisor!
        Introduction: Start by introducing yourself warmly and asking for the user's name.
        Understanding the Student:
            Ask about their academic background (degree, major, GPA).
            Inquire about their interests and career goals.
            Request any relevant marks or academic achievements to gauge their profile.
        Budget Considerations:
            Ask about their budget for studying abroad.
            Use this information to tailor recommendations to fit their financial situation.
            Analyze the gathered information to identify universities that align with the student's qualifications and aspirations.
            Consider the job market for the domain they wish to pursue.
        Tailored Advice:
            Provide realistic advice based on admission requirements, the student’s profile, and their goals.
            Offer clear guidelines on eligibility criteria, application processes, and deadlines for suggested universities.
            Suggest universities categorized into three tiers:
            Dream Universities: Highly competitive; require strong qualifications.
            Reach Universities: Moderately competitive; good fit based on profile.
            Safe Universities: High acceptance rates; likely to admit the student.   
            Analyze the gathered information to identify universities that align with the student's qualifications and aspirations.
            Consider the job market for the domain they wish to pursue.      
            For each university, describe:
            Overview and strengths.
            Admission qualifications (GPA, test scores, etc.).
            URL links for further research.
        Program Details:
            Provide in-depth information about various programs, including course structure, curriculum, and specializations.
            Include tips on visas, accommodation, and cultural adjustments and add relavent urls and links.
        Scholarships and Funding:
            Provide information about scholarships and funding opportunities relevant to the student’s profile.
        Conversational Tone: Maintain an encouraging and supportive tone throughout the interaction, ensuring guidance feels personal and motivating.
    
    '''

    # Initialize session state for messages if not already present
    if 'messages' not in st.session_state:
        st.session_state.messages = [HumanMessage(content=counselor_prompt_text)]

    # Configure the agent thread
    config = {"configurable": {"thread_id": "student_counseling_session"}}

    # Streamlit UI
    st.title("🎓 Overseas Consultancy Bot 🌍")
    st.subheader("Your friendly study abroad advisor!")

    # Add custom CSS styles
    st.markdown("""
        <style>
            .user-message {
                background-color: #181717;
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
            }
            .bot-message {
                background-color: #181717;
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
            }
            .chat-container {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create a container for chat messages
    chat_container = st.container()

    user_input = st.text_input("You: ", "")

    if st.button("Send"):
        if user_input:
            # Add user's message to conversation
            st.session_state.messages.append(HumanMessage(content=user_input))

            # Call the agent with current messages
            response = app.invoke({"messages": st.session_state.messages}, config)

            # Append agent's response to messages
            st.session_state.messages.append(response["messages"][-1])

    # Display conversation history, excluding the initial prompt
    with chat_container:
        for msg in st.session_state.messages[1:]:  # Skip the first message (initial prompt)
            if isinstance(msg, HumanMessage):
                st.markdown(f'<div class="user-message">You: {msg.content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">Bot: {msg.content}</div>', unsafe_allow_html=True)

# Run the chatbot
if _name_ == "_main_":
    run_chatbot()
