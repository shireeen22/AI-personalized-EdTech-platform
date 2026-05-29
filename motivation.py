import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
import os
import requests
import uuid
import shutil

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

llm = HuggingFaceEndpoint(repo_id='meta-llama/Llama-3.1-8B-Instruct',
                          task='text-generation',
                          huggingfacehub_api_token= HF_API_TOKEN,
                          max_new_tokens=700,
                          temperature=0.7)

chat_model = ChatHuggingFace(llm=llm)



def motivation_ai(student_name,weak_subject,problem_solving,stress_management,backup_plan,communication,motivation_level):
    
    prompt = f"""
    You are an AI student mentor and psychologist.
    Analyze the student's personality and learning behavior.
    Student Details:
    Name : {student_name}
    Weak subject: {weak_subject}
    Problem Solving Ability:{problem_solving}/10
    Stress Management: {stress_management}
    Backup plan: {backup_plan}
    Communication Skill: {communication}
    Motivation Level: {motivation_level}

    Give:

    1. Personality analysis
    2. Motivation
    3. Study improvement techniques
    4. Confidence boosting advice
    5. Time management tips
    6. Stress handling advice

    Instructions:
    - Keep response student friendly
    - Use simple language
    - Make response motivational
    - Keep answer structured
    - Use bullet points
    """

    response = chat_model.invoke(prompt)
    return response.content



