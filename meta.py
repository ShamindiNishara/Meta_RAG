import streamlit as st
import os
import pandas as pd
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor

# Load API key and set up environment
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
embedding_model = HuggingFaceEmbeddings()

# Load the feedback dataset
feedback_df = pd.read_csv("./dataset/modified_dataset.csv")  # Replace with actual path

# Load learning materials
loader = PyPDFDirectoryLoader("./pdf_files")
docs = loader.load()

# Split documents into chunks for efficient retrieval
documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)

# Store chunks into a vector database for retrieval
vectordb = FAISS.from_documents(documents, embedding_model)
retriever = vectordb.as_retriever()

# Create retrieval tool for learning materials
pdf_tool = create_retriever_tool(retriever, "pdf_search",
                     "Search for information about given question")
tools = [pdf_tool]

# Set up the LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

# Define the feedback generation prompt
prompt = ChatPromptTemplate.from_template(
"""
Generate feedback for the student's programming task based on their metacognitive profile and question context.
- Use similar metacognitive feedback retrieved from past data to shape the response.
- Use the learning materials to enhance question-specific guidance where applicable.

Student Question: {question}
Student Answer: {answer}
Metacognitive Profile: {profile}
Similar Feedback: {similar_feedback}
Learning Context:
<context>
{context}
<context>

Provide detailed feedback to help the student improve.
{agent_scratchpad}
"""
)

# Create the LLM agent with tools
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Streamlit Interface
st.title("Metacognitive Feedback Generator")

# Input fields for question, student answer, and metacognitive profile
question = st.text_area("Enter the programming question")
student_answer = st.text_area("Enter the student's answer")
metacognitive_profile = st.text_input("Enter the metacognitive profile as a list of 16 integers, e.g., [1,3,2,...]")

# Convert the input metacognitive profile to a list of integers
if metacognitive_profile:
    try:
        profile_vector = list(map(int, metacognitive_profile.strip("[]").split(",")))
    except ValueError:
        st.write("Please enter a valid list of 16 integers for the metacognitive profile.")

# Process and retrieve similar feedback if inputs are provided
if st.button("Generate Feedback") and question and student_answer and len(profile_vector) == 16:
    start_time = time.time()

    # Retrieve similar feedback from the dataset based on the profile
    feedback_df['distance'] = feedback_df['metacognitive_profile'].apply(
        lambda x: sum(abs(a - b) for a, b in zip(profile_vector, eval(x)))
    )
    similar_feedbacks = feedback_df.nsmallest(3, 'distance')['metacognitive_feedback'].tolist()
    similar_feedback = " ".join(similar_feedbacks)

    # Use the retriever to get context from learning materials
    # context_documents = retriever.retrieve(question)
    # learning_context = " ".join([doc.page_content for doc in context_documents])

    # Use the agent to generate feedback with the retrieved information
    try:
        response = agent_executor.invoke({
            "question": question,
            "answer": student_answer,
            "profile": profile_vector,
            "similar_feedback": similar_feedback,
            "context": "",
            "agent_scratchpad": ""
        })
        response_time = time.time() - start_time
        st.write(response['output'])
        st.markdown(f"<p style='color:blue;'>Response Time: {response_time:.2f} seconds</p>", unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please enter all required fields.")
