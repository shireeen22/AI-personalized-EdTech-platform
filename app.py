import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from PIL import Image
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


BASE_URL = "http://127.0.0.1:8000"

#===========================================================================
#****************** Logein and Registration process*********************
#===========================================================================
st.set_page_config(

    page_title="AI Personalized EDTech Platform",

    page_icon="🎓",

    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* =========================
   LABEL STYLING
========================= */

.stTextInput label,
.stSelectbox label,
.stTextArea label,
.stNumberInput label,
.stSlider label {

    color: #38bdf8 !important;

    font-size: 18px !important;

    font-weight: 700 !important;

    letter-spacing: 0.5px !important;

    text-shadow: 0px 0px 8px rgba(56,189,248,0.7);

    margin-bottom: 8px !important;
}


/* =========================
   INPUT BOX
========================= */

.stTextInput input,
.stTextArea textarea {

    background-color: #0f172a !important;

    color: white !important;

    border: 2px solid #38bdf8 !important;

    border-radius: 12px !important;

    padding: 12px !important;

    font-size: 16px !important;
}


/* =========================
   PLACEHOLDER TEXT
========================= */

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {

    color: #94a3b8 !important;

    font-size: 15px !important;
}


/* =========================
   INPUT FOCUS EFFECT
========================= */

.stTextInput input:focus,
.stTextArea textarea:focus {

    border: 2px solid #7c3aed !important;

    box-shadow: 0px 0px 15px rgba(124,58,237,0.8) !important;
}


/* =========================
   SELECT BOX
========================= */

.stSelectbox div[data-baseweb="select"] {

    background-color: #0f172a !important;

    color: white !important;

    border: 2px solid #38bdf8 !important;

    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    left, center, right = st.columns([1,2,1])
    with center:
        st.markdown(
            """
            <div class="auth-box">
            """,
            unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align:center;'>🎓 AI Student EdTech Platform</h1>",
            unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center;color:lightgray;'>"
            "Smart Learning • AI Assistant • Quiz System"
            "</p>",
            unsafe_allow_html=True)
        st.divider()
        tab1,tab2 = st.tabs(["Signup","Login"])

        #*********************Sign up option************

        with tab1:
            full_name = st.text_input("Enter your Full name")
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password",type="password")

            if st.button("Create account"):
                if(full_name.strip()== ""
                   or
                   email.strip()== ""
                   or 
                   username.strip()== ""
                   or 
                   password.strip()== ""):
                    st.warning("Please fill all the fields⚠️")
                else:
                    try:
                        response = requests.post(f"{BASE_URL}/register",json={
                            "full_name":full_name,
                            "email":email,
                            "username":username,
                            "password":password})
                        data = response.json()
                        if data["success"]:
                            st.success("Account created successfully!✅")
                        else:
                            st.error(data["error"])
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        st.markdown(

            "</div>",

            unsafe_allow_html=True
        )

    #****************Login option**************************
    
        with tab2:
            username = st.text_input("Username",key="login_username")
            password = st.text_input("Password",key="login_password",type="password")
            if st.button("Login"):
                if username.strip()=="" or password.strip()=="":
                    st.warning("Please fill both fields⚠️ ")
                else:
                    try:
                        response = requests.post(f"{BASE_URL}/login",
                                             json={
                                                 "username":username,
                                                 "password":password})
                        data = response.json()
                        if data["success"]:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success("Login Successful!✅")
                            st.rerun()
                        else:
                            st.error(data["error"])
                    except Exception as e:
                            st.error(f"Error: {str(e)}")

# **************After login************

if st.session_state.logged_in:
    st.sidebar.success(f"Welocome {st.session_state.username}👋")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.success("Logein successful!🎓Enjoye🎓")
    
    #********************Main app start**************************
    #************************************************************

    st.set_page_config(
    page_title='AI EdTech Student Platform',
    page_icon='🎓🤖',
    layout='wide')
    st.markdown("""
    <style>
    /* Main Background */
    .stApp {
                background: linear-gradient(
                to right,#dbeafe,#fce7f3,#fef9c3);}

    /* Sidebar */
    section[data-testid="stSidebar"] {background: linear-gradient(
                to bottom,
                #7c3aed,
                #3b82f6);
                # color: pink;}

    /* Buttons */
    .stButton>button {background: linear-gradient(
        to right,
        #ec4899,
        #8b5cf6);color: white;border: none;border-radius: 15px;padding: 12px 25px;font-size: 18px;font-weight: bold;transition: 0.3s;}

    .stButton>button:hover {
                transform: scale(1.05);background: linear-gradient(to right,
                #8b5cf6,#3b82f6);}

    /* Metric Cards */
    .metric-card {background: white;padding: 25px;border-radius: 20px;text-align: center;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.1);}

    /* Feature Cards */
    .feature-card {padding: 25px;border-radius: 25px;
                color: white;text-align: center;font-size: 20px;
                font-weight: bold;box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
                transition: 0.3s;}

    .feature-card:hover {transform: translateY(-5px);
                }
    /* Welcome Box */
    .welcome-box {background: rgba(255,255,255,0.6);padding: 40px;
                border-radius: 30px;
                backdrop-filter: blur(10px);}

    /* Title */
    .main-title {font-size: 55px;font-weight: 800;
                color: #1e293b;}

    /* Subtitle */
    .sub-title {font-size: 22px;
                color: #475569;}

    </style>
    """, unsafe_allow_html=True)

    # *************************Sidebar****************************************************
    st.sidebar.title('AI EdTech Student Platform')

    #********************** Menu bar*******************************************************

    menu = st.sidebar.radio('Navigation',['Home','Performance Prediction','AI Study Assistant','Quiz',
                                          'Teacher Panel',
                                          'AI Motivation'])
    if menu == "Home":
        col1, col2 = st.columns([2,1])
        with col1:
            st.markdown("""
                        <div class="welcome-box">
                        <div class="main-title">
                        Welcome To Your AI Learning World
                        </div>
                        <br>
                        <div class="sub-title">
                        Smart AI learning platform powered by
                        AI + ML + GenAI.
                        Predict student performance,
                        generate quizzes,
                        upload notes,
                        and learn interactively
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
            
        with col2:
            st.image(
                "27409da6-9339-455d-9c16-febb687ae5ed.jpg",
                width=350)
            st.write("")
            st.write("")

        #*************************************************
        # FEATURE CARDS
        st.subheader("Platform Features")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                        <div class="feature-card"
                        style="background: linear-gradient(to right,#ec4899,#f97316);">
                        📈<br><br>
                        Performance Prediction
                        </div>
                        """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
                        <div class="feature-card"
                        style="background: linear-gradient(to right,#3b82f6,#06b6d4);">
                        🤖<br><br>
                        AI Study Assistant
                        </div>
                        """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
                        <div class="feature-card"
                        style="background: linear-gradient(to right,#22c55e,#84cc16);">
                        ❓<br><br>
                        Quiz Generator
                        </div>
                        """, unsafe_allow_html=True)
            st.write("")
            
            c4, c5, c6 = st.columns(3)
        
        with c4:
            st.markdown("""
                        <div class="feature-card"
                        style="background: linear-gradient(to right,#8b5cf6,#d946ef);">
                        📝<br><br>
                        Notes & Summary
                        </div>
                        """, unsafe_allow_html=True)

        with c5:
            st.markdown("""
                        <div class="feature-card"
                        style="background: linear-gradient(to right,#0f766e,#14b8a6);">
                        🧠<br><br>
                        Teacher panel
                        </div>
                        """, unsafe_allow_html=True)

        with c6:
            st.markdown("""
                        <div class="feature-card"
                        style="background: linear-gradient(to right,#f59e0b,#ef4444);">
                        🔥<br><br>
                        AI Motivation
                        </div>
                        """, unsafe_allow_html=True)
            st.write("")
            st.write("")

        # ======================================
        # STATS SECTION
        # ======================================
        st.subheader("Platform Analytics")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown("""
            <div class="metric-card">
            <h1>1200+</h1>
            <p>Students</p>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown("""
            <div class="metric-card">
            <h1>80%</h1>
            <p>Prediction Accuracy</p>
            </div>
            """, unsafe_allow_html=True)    
       

        with m3:
            st.markdown("""
            <div class="metric-card">
            <h1>100+</h1>
            <p>AI Quizzes</p>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown("""
            <div class="metric-card">
            <h1>24/7</h1>
            <p>AI Assistance</p>
            </div>
            """, unsafe_allow_html=True)    

        st.divider()
        st.markdown("""<center>Made with ❤️ using FastAPI + LangChain + RAG + DeepSeek</center>""", unsafe_allow_html=True)
        st.markdown("""<center>**CREATOR: SHIREEN KHAN**""", unsafe_allow_html=True) 

    #========================================================================
    # **********************2nd option selected****************************
    #========================================================================

    elif menu == 'Performance Prediction':
        st.title('📈 Student Performance Prediction')
        study_hours = st.slider('Study Hours',0,10)
        attendance = st.slider('Attendance',0,100)
        sleep_hours = st.slider('Sleep Hours',0,10)
        previous_grade = st.slider('Previous Percentage',0,100)
        assignments_completed =st.slider('Complete Asiignment',0,10)
        practice_tests_taken = st.slider('Practice Test Taken',0,10)
        notes_quality_score = st.slider('Notes quality score',0,10)
        time_management_score = st.slider('Time Management score',0,10)
        motivation_level = st.slider('Motivation Level',0,10)
        mental_health_score = st.slider('Mental Health score',0,10)
        screen_time = st.slider('Screen Timing',0,12)
        social_media_hours = st.slider('Spend Social Media hours',0,8)
        
        if st.button('Predict Performance🚀'):
            with st.spinner("Analyzing your Performance...."):
                try:
                    data = {'study_hours':study_hours,
                            'attendance':attendance,
                            'sleep_hours':sleep_hours,
                            'previous_grade':previous_grade,
                            'assignments_completed':assignments_completed,
                            'practice_tests_taken':practice_tests_taken,
                            'notes_quality_score':notes_quality_score,
                            'time_management_score':time_management_score,
                            'motivation_level':motivation_level,
                            'mental_health_score':mental_health_score,
                            'screen_time':screen_time,
                            'social_media_hours':social_media_hours}
                    
                    response = requests.post(f"{BASE_URL}/predict",
                                              json=data)
                    result = response.json()

                    if response.status_code==200 and result["success"]:
                        st.success(
                            f"🎯 Predicted Percentage: "
                            f"{result['pred_percentage']}%")
                        st.divider()
                        #report**************
                        st.subheader("AI generated Performance report")
                        st.markdown(result["report"])
                        st.divider()
                        # visualization********
                        st.subheader("Performance visualization")
                        st.image(result["graph"],use_container_width=True)
                        #********progress bar************
                        percentage = int(result["pred_percentage"])
                        st.subheader("Performance score")
                        st.progress(percentage)
                        st.markdown(
                            f"""
                            <h3 style='text-align:center;
                            color:#38bdf8;'>
                            {percentage}%
                            </h3>
                            """,
                            unsafe_allow_html=True)
                    else:
                        st.error(result.get("error","Prediction failed"))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                            
        st.divider()
        st.markdown("""<center>Made with ❤️ using FastAPI + LangChain + RAG + DeepSeek</center>""", unsafe_allow_html=True)
        st.markdown("""<center>**CREATOR: SHIREEN KHAN**""", unsafe_allow_html=True) 

    #=========================================================================
    #************************3rd Option**************************************
    #=========================================================================

    elif menu == "AI Study Assistant":
        st.title('AI Study Assistant📚')
        st.subheader('Ask❓Generate❇️Explain❣️')
        
        with st.sidebar:
            st.markdown("<div class='sidebar-title'>🎓 Study AI</div>",unsafe_allow_html=True)
            st.image("stunning-creative-happy-graduate-in-cap-and-gown-genuine-free-png.webp",width=300)
            st.markdown("<div class='section-title'>⚡ Features</div>",unsafe_allow_html=True)
            features = ["Student Friendly Explanation",
                        "AI Generated Notes",
                        "Quiz Generation",
                        "Ask Questions",
                         "RAG + LLM Support"]
            for feature in features:
                st.markdown(f"<div class='feature-card'>{feature}</div>",unsafe_allow_html=True)
                st.markdown("---")
            with st.expander("ℹ️ About Platform"):
                st.write("""This AI-powered platform helps students:
                        - Understand topics easily

                        - Generate AI powered smart notes

                        - Create quizzes from the notes instantly

                        - Predict academic performance
                         """)
                
        #************Text Input***************************    
        
        if "chapter_processed" not in st.session_state:
            st.session_state.chapter_processed = False
        st.subheader("📖 Paste Chapter Text")
        chapter_text = st.text_area("Enter your chapter or book text",height=300,
        placeholder="Paste your chapter text here...")
            
        if st.button("🚀 Process Chapter"):
            if chapter_text.strip() == "":
                st.warning("Please paste some chapter text.")

            else: 
                with st.spinner("Processing chapter..."):
                    try:
                        response = requests.post(f"{BASE_URL}/process-chapter",json={"text": chapter_text})
                        data = response.json()
                        if response.status_code == 200 and data["success"]:
                            st.session_state.chapter_processed = True
                            st.success("✅ Chapter processed successfully!")
                        else:
                            st.error(data.get("error", "Error processing chapter"))
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # ******************FEATURE BUTTONS********************

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Explain Chapter"):
                if not st.session_state.chapter_processed:
                    st.warning("⚠️ Please process chapter first.")
                else:
                    with st.spinner("Generating explanation..."):
                        try:
                            response = requests.get(f"{BASE_URL}/explain")
                            data=response.json()
                            if response.status_code == 200 and data["success"]:
                                st.subheader("Student Friendly Explanation")
                                st.markdown(data["explanation"])
                            else:
                                st.error(data.get("error", "Error generating explanation"))
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
    
        # ***********************2nd option Notes generator******************************************
        with col2:
            if st.button('Notes'):
                if not st.session_state.chapter_processed:
                    st.warning("⚠️ Please process chapter first.")
                else:
                    with st.spinner("Wait! Your Notes are generating....."):
                        try:
                            response = requests.get(f'{BASE_URL}/notes')  # notes route
                            data = response.json()
                            if response.status_code == 200 and data['success']:
                                st.subheader('AI Generated Notes')
                                st.markdown(data['notes'])
                            else:
                                st.error(data.get('error','Error generating notes'))
                        except Exception as e:
                            st.error(f'Error: {str(e)}')

    #*******************************3rd option******************************************************
        with col3:
            if st.button('Quiz'):
                if not st.session_state.chapter_processed:
                    st.warning("⚠️ Please process chapter first.")
                else:
                    with st.spinner('Wait! Quiz are Generating...'):
                        try:
                            response = requests.get(f'{BASE_URL}/quiz')  # quiz route
                            data = response.json()
                            if response.status_code == 200 and data['success']:
                                st.subheader('AI generated Quizz')
                                st.markdown(data['quiz'])
                            else:
                                st.error(data.get('error','Error generating quiz'))
                        except Exception as e:
                            st.error(f'Error: {str(e)}')
    
    # **********************************4th option*********************************************
        st.divider()
        st.subheader('Ask question from given text.')
        user_question = st.text_input('Enter your question') # taking input from user.........

        if st.button('Ask AI'):
            if not st.session_state.chapter_processed:
                st.warning("⚠️ Please process chapter first.")

            elif user_question.strip() == "":    # if blank input....
                st.warning('Please enter a question')
            
            else:
                with st.spinner('Thinking....'):  # Generating Answer.....
                    try:
                        response = requests.post(f'{BASE_URL}/ask',
                                            json={'question':user_question})
                        data = response.json()
                        if response.status_code==200 and data['success']:
                            st.subheader('Answer')
                            st.markdown(data['answer'])
                        else:
                            st.error(data.get('error','Error generating answer'))

                    except Exception as e:
                        st.error(f'Error: {str(e)}')

        st.divider()
        st.markdown("""<center>Made with ❤️ using FastAPI + LangChain + RAG + DeepSeek</center>""", unsafe_allow_html=True)
        st.markdown("""<center>**CREATOR: SHIREEN KHAN**""", unsafe_allow_html=True) 

    #===============================================================
    #*******************4th option***********************
    #===============================================================

    elif menu == 'Quiz':
        st.title('Quiz system🧠')

        #****************Load the quiz.json file******************************
        with open("quiz_data.json","r") as file:
            quiz_data = json.load(file)

        #************************ Take student's details***********************
        st.subheader('Please enter your details')  
        stu_name = st.text_input("Name")                 # name
        stu_roll_no = st.text_input("Roll no.")          # roll number
        select_class = st.selectbox("Class",list(quiz_data.keys()))   # class
        subjects = list(quiz_data[select_class].keys())
        select_sub = st.selectbox("Subject",subjects)   #  subject

        # ********************** Load questions*******************************

        questions = quiz_data[select_class][select_sub]

        st.divider()
        st.subheader("Your quiz")
        student_answer = []  # store student's answers

        #***************************Display the questions*********************

        for i, q in enumerate(questions[:15]):
            st.write(f"### Q{i+1}. {q['question']}")
            answer = st.radio('Choose your answer:',
                              q["options"],key=i)
            student_answer.append(answer)

        #************************Submit quiz*********************************
        if st.button("Submit"):
            correct = 0
            wrong = 0
            total = len(questions[:15])
            st.divider()
        #**************************Performance card***********************
            st.subheader("Result")
            for i, q in enumerate(questions[:15]):
                st.write(f"### Q{i+1}: {q['question']}")
                st.write(f'Your answers: {student_answer[i]}')
                st.write(f'Correct answers: {q['answer']}')
                if student_answer[i] ==q['answer']:
                    st.success('Correct✅')
                    correct += 1      # Increment
                else:
                    st.error("Wrong❌")
                    wrong += 1 
            marks = correct * 1
            percentage = (correct/total) * 100

            st.divider()

            st.subheader('Final Result')
            st.write(f'Name: {stu_name}')
            st.write(f'Roll no. {stu_roll_no}')
            st.write(f'Correct answers: {correct}')
            st.write(f'Wrong attempted: {wrong}')
            st.write(f'Total marks obtained: {marks}/{total}')
            st.write(f'Percentage: {percentage:.2f}%')   

            #**************Save the name of students who attempted quiz and show the leaderboard********************

            # *********************1.Save result*******************
            result_data = {
                "Name":stu_name,
                "Roll no.": stu_roll_no,
                "Class":select_class,
                "Subject": select_sub,
                "Marks":marks,
                "Percentage":percentage}
            
            #***************2.Create Pandas DF********************************

            result_df = pd.DataFrame([result_data]) 

            #************************File name*****************************
            file_name = "student_result.csv"

        #*******************3.Data append in file**************************
            if os.path.exists(file_name):
                result_df.to_csv(file_name,mode='a',header=False,index=False)
            else:
                result_df.to_csv(file_name,index=False)

        #************LeaderBoard Section***************************
            st.divider()
            st.subheader("Leaderboard")

        #************************4.Load csv file***********************
            if os.path.exists("student_result.csv"):
                leader_df = pd.read_csv("student_result.csv") # final Df
                # apply sorting
                sort_values = leader_df.sort_values(by='Marks',ascending=False)

                # extract top students**********
                top_students = sort_values.head(5)

                # Add ranking column also*******************
                top_students.reset_index(drop=True,inplace=True)
                top_students.index += 1      # add one column more for Rank...........
                top_students.index.name = 'Rank'    # name of the new column

                styled_df = top_students.style \
                    .background_gradient(cmap="viridis",subset=["Marks", "Percentage"]) \
                        .set_properties(**{'background-color': '#0E1117','color': 'white','border-color': '#262730',
                                           'text-align': 'center','font-size': '14px'}) \
                                            .set_table_styles([{'selector': 'th','props': [('background-color', '#6C63FF'),
                                                                                           ('color', 'white'),('font-size', '15px'),
                                                                                           ('text-align', 'center')]}])
                # streamlit df*******************
                st.dataframe(styled_df,use_container_width=True)
            else:
                st.info("No quiz attempts yet!")

    


            #***********************Visualization*************************************
            st.divider()
            st.subheader('Perfromance visualization')
            labels =['Correct attemted',
                     'Wrong attempted']
            sizes = [correct,wrong]
        
            #********************explode effect*****************
            explode = (0.08,0)
            fig, ax = plt.subplots(figsize=(2,2))
            ax.pie(sizes,labels=labels,autopct='%1.1f%%',explode=explode,shadow=True,startangle=90)
            ax.set_title('Answers analysis')
            ax.axis('equal')
            #*******************Remove white background*****************
            fig.patch.set_alpha(0)
            st.pyplot(fig)

            #********************Progress bar**************************************

            st.subheader("Performance score")
            st.progress(int(percentage))
            st.write(f"### {percentage:.2f}%")

            #********************Performance message*******************************
            if percentage >=90:
                st.subheader("Excellent performance🌟")
            elif percentage >= 80:
                st.subheader("Good Performance👍")
            elif percentage >= 60:
                st.subheader("Keep it up👍")
            else:
                st.subheader("Need more practice!")
    

        st.divider()
        st.markdown("""<center>Made with ❤️ using FastAPI + LangChain + RAG + DeepSeek</center>""", unsafe_allow_html=True)  
        st.markdown("""<center>**CREATOR: SHIREEN KHAN**""", unsafe_allow_html=True) 
        
    #===============================================================
    #****************** 5th option***********************
    #===============================================================

    elif menu == 'Teacher Panel':
        st.title("Welcome into Teacher panel❤️")
        st.subheader("This panel is only for Teachers to Update the quiz!")

        #************* 1.Load existing quiz data******************************
        if os.path.exists('quiz_data.json'):
            with open("quiz_data.json","r") as file:
                quiz_data = json.load(file)
        else:
            quiz_data = {}

        #****************** 2.Taking inputs****************   
        # Class......
        classes = ["Class 10",
                   "Class 9",
                   "Class 8",
                   "Class 5"]
        class_name = st.selectbox("Select class",classes)

        # Subject...........
        subjects = [
            "English",
            "Maths",
            "Science"]
        subject_name = st.selectbox("Enter subject",subjects)
        st.divider()

        #**************Question input******************
        question = st.text_area("Enter your question")

        # *****************Options input********************
        option_1 = st.text_input("Option 1")
        option_2 = st.text_input("Option 2")
        option_3 = st.text_input("Option 3")
        option_4 = st.text_input("Option 4")

        options = [option_1,option_2,option_3,option_4]

        # ***************Correct answer**********************

        corre_ans = st.selectbox("Select correct answer",options)
 
        #***********Add the quizz*********************
        if st.button("Add quiz"):

            if(question.strip() == "" 
               or option_1.strip() == ""
               or option_2.strip() == ""
               or option_3.strip() == ""
               or option_4.strip() == ""):
                st.warning("⚠️ Please fill all fields.")
            else: 
                # If want to create or add a new class***************
                if class_name not in quiz_data:
                    quiz_data[class_name] = {}
            
                if (subject_name not in quiz_data[class_name]
                    or
                    not isinstance(quiz_data[class_name][subject_name],list)):
                    quiz_data[class_name][subject_name] = []


                new_quest = {"question": question,
                             "options": [option_1,option_2,option_3,option_4],"answer": corre_ans}
        
                #***********append new question in quiz data*************
                quiz_data[class_name][subject_name].append(new_quest)

                # save json*************
                with open("quiz_data.json","w") as file:
                    json.dump(quiz_data,file,indent=4,ensure_ascii=False)

                st.success("Question added successfully!✅")    
        st.divider()
        st.markdown("""<center>Made with ❤️ using FastAPI + LangChain + RAG + DeepSeek</center>""", unsafe_allow_html=True)
        st.markdown("""<center>**CREATOR: SHIREEN KHAN**""", unsafe_allow_html=True)  

    #=======================================================
    #*********************** Last option*******************
    #=======================================================

    else:
        st.title("AI Motivation💡")       
        st.subheader("Personalized AI based student mentor")
        st.divider()

        #*********************Taking inputs**********************
        student_name = st.text_input("Enter Your Name")

        weak_subject = st.selectbox("Choose your weak subject",["Maths","English",
                                             "Science","Hindi","SST","Biology","Physics",
                                             "Chemistry","Third language","Computer"])
    
        problem_solving = st.slider("Your problem solving ability from 1 to 10",1,10,5)

        stress_management = st.selectbox("Your Stress management level",["Low","Medium","High"])

        backup_plan = st.selectbox("Your back up plan",["Goverment job","Freelancing","Family Business",
                                                    "Higher study","Startup"])
    
        communication = st.selectbox("Your communication type",["Introvert","Extrovert","Average","Friendly","Social"])

        motivation_level = st.selectbox("Your motivation level",["Low","Medium","High"])

        st.divider()

        if st.button("AI generate motivation"):
            if student_name.strip() == "":
                st.warning("Please enter your name⚠️")  # for validity
            else:
                with st.spinner("Analyzing...."):
                    try:
                        response = requests.post(f"{BASE_URL}/student-motivation",
                                             json={"student_name" : student_name,
                                                   "weak_subject" : weak_subject,
                                                   "problem_solving" : problem_solving,
                                                   "stress_management" : stress_management,
                                                   "backup_plan" : backup_plan,
                                                   "communication" : communication,
                                                   "motivation_level" : motivation_level})
                        data = response.json()
                        if(response.status_code==200 and data["success"]):
                            st.success("AI analysis generated✨")
                            st.markdown(data["motivation"])      # response from main.py
                            st.balloons()
                        else:
                            st.error(data.get("error","Error generating motivation"))    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                   


    #student_name,weak_subject,problem_solving,stress_management,backup_plan,communication,motivation_level



