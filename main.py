from fastapi import FastAPI, UploadFile
from predict import predict_student
from report_card import (report_card_gene, performance_graph)
from llm import (create_vector_store,load_vector_store,explain_text,generate_notes,quiz_generator,ask_question)
from pydantic import BaseModel
from motivation import motivation_ai, chat_model
from database import register_user,user_login


class ChapterRequest(BaseModel):
    text: str

class QuestionRequest(BaseModel):
    question: str

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Student Performance Prediction API is Running Successfully 🚀"
    }

class PredictionRequest(BaseModel):
        study_hours: int
        attendance: int
        sleep_hours: int
        previous_grade: int
        assignments_completed: int
        practice_tests_taken: int
        notes_quality_score: int
        time_management_score: int
        motivation_level: int
        mental_health_score: int
        screen_time: int
        social_media_hours: int

@app.post("/predict")
def predict(request:PredictionRequest):
    try:
        data = request.model_dump()    # convert to dict......
        # predict percentage***********
        pred_percentage = predict_student(data)
        
        # generate report********************
        report = report_card_gene(data,pred_percentage)

        performance_graph(data,pred_percentage)

        # return response**************
        return {
            "success":True,
            "pred_percentage":round(pred_percentage,2),
            "report":report,
            "graph": "performance_graph.png"}
    except Exception as e:
        return {
            "success":False,
            "error": str(e)
        }










@app.post("/predict")
def predict(data: dict):

    try:

        # Predict Percentage
        pred_percentage = predict_student(data)

        # Generate Report
        report = report_card_gene(data, pred_percentage)

        # Generate Graph
        performance_graph(data)

        return {
            'pred_percentage': pred_percentage,
            'report': report,
            'graph': 'performance_graph.png'
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/process-chapter")
def process_chapter(request: ChapterRequest):

    try:

        create_vector_store(request.text)

        return {
            "success": True,
            "message": "Chapter processed successfully"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
#************************************Explaination Route**************************

@app.get("/explain")
def explain():

    try:

        vector_store = load_vector_store()

        response = explain_text(vector_store)

        return {
            "success": True,
            "explanation": response
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
#***************************************Generate Notes route***********************************
@app.get("/notes")
def notes():
    try:
        vector_store = load_vector_store()
        response = generate_notes(vector_store)
        return {
            'success': True,
            'notes': response
        }
    except Exception as e:
        return{
            'success': False,
            'error': str(e)
        }
    
#***************************************quizz generator route****************
@app.get("/quiz")
def quiz():
    try:
        vector_store = load_vector_store()
        response = quiz_generator(vector_store)
        return {
            'success':True,
            'quiz':response
        }
    except Exception as e:
        return{
            'success':False,
            'error': str(e)
        }

#**************************************ask question route************************
@app.post("/ask")
def ask_ai(request:QuestionRequest):
    try:
        vector_store = load_vector_store()
        response = ask_question(vector_store,request.question)
        return {
            'success':True,
            'question': request.question,
            'answer': response
        }
    except Exception as e:
        return{
            'success': False,
            'error': str(e)
        }


class MotivationRequest(BaseModel):
    student_name: str
    weak_subject: str
    problem_solving: int
    stress_management: str
    backup_plan: str
    communication: str
    motivation_level: str

@app.post("/student-motivation")

def student_motivation(request:MotivationRequest):
    try:
        response = motivation_ai(request.student_name,
                                 request.weak_subject,
                                 request.problem_solving,
                                 request.stress_management,
                                 request.backup_plan,
                                 request.communication,
                                 request.motivation_level)
        return {
            "success": True,
            "motivation": response
        }
    except Exception as e:
        return {
            "success":False,
            "error": str(e)
        }
        


class RegisterRequest(BaseModel):
    full_name : str
    email : str
    username: str
    password : str

class LoginRequest(BaseModel):
    username: str
    password:str

#**************Ragister route**********************
@app.post("/register")
def register(request:RegisterRequest):
    success = register_user(
        request.full_name,
        request.email,
        request.username,
        request.password)
    if success:
        return {"success":True,
                "message": "User registered successfully!"}
    else:
        return {"success":False,
                "error": "Username or email already exists"}
    
#*********************Login route***************************

@app.post("/login")
def login(request:LoginRequest):
    user = user_login(
        request.username,
        request.password
    )
    if user:
        return {"success":True,
                "message": "Login successful"}
    else:
        return {
            "success":False,
            "error": "Invalid username or password"
        }
