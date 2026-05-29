import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. get grade...
def get_grade_categ(score):
    if score >= 90:
        return 'A+🥇'
    elif score >= 75:
        return 'A✨'
    elif score >=60:
        return 'B😊'
    elif score >= 40:
        return 'C😕'
    else:
        return 'F❌'
# print(get_grade_categ(56))

# 2. Report card generator function...

def report_card_gene(student_data,pred_percentage):
    grade = get_grade_categ(pred_percentage)

    # making report...

    report = f"""
    Your report card 📉
    =====================================================

    **Student Academic Details**👤📚
    *********************************

    **Study Hours** :                        {student_data['study_hours']}\n
    **Attendence** :                         {student_data['attendance']}\n
    **Previous_Percentage** :                {student_data['previous_grade']}\n

    **Lifestyle Analysis** 📱 ⚖️
    *********************************

    **Screen Time Hours** :     {student_data['screen_time']}\n
    **Social media Hours** :    {student_data['social_media_hours']}\n
    **Sleep Hours** :                        {student_data['sleep_hours']}\n

    **Performance Factors**➕📖🧠 
    *********************************

    **Completed Assignments**  :  {student_data['assignments_completed']}\n
    **Practice test taken**  :    {student_data['practice_tests_taken']}\n
    **Notes Quality Score**  :    {student_data['notes_quality_score']}\n
    **Time Management Score** :  {student_data['time_management_score']}\n
    **Motivation level**  :           {student_data['motivation_level']}\n
    **Mental Health Score** :         {student_data['mental_health_score']}\n
    
    **Final Prediction** 🎯
    *********************************

    **Predicted Percentage** : {pred_percentage}%\n
    **Predicted Grade** : {grade}

    =============**END OF THE REPORT**======================
    """
    return report

# 3. Performance Graph....

def performance_graph(student_data,pred_percentage):
    labels = ['Study Hours',
              'Attendence',
              'Sleep Hours',
              'Motivation',
              'Screen Time',
              'Social Media',
              'Notes Quality',
              'Mental Health',]
    
    values = [student_data['study_hours'],
              student_data['attendance'],
              student_data['sleep_hours'],
              student_data['motivation_level'],
              student_data['screen_time'],
              student_data['social_media_hours'],
              student_data['notes_quality_score'],
              student_data['mental_health_score'],]
    
    plt.figure(figsize=(6,4))

    plt.barh(labels, values)

    plt.title(
        f"Predicted Score: {pred_percentage}%"
    )
    plt.tight_layout()

    plt.savefig("performance_graph.png")

    plt.close()

