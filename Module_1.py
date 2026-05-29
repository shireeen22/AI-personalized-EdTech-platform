import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error
from sklearn.preprocessing import StandardScaler
from pytorch_tabnet.tab_model import TabNetRegressor # Pre-rained DL model
import joblib

# Load dataset...
df = pd.read_csv('student_performance_prediction_dataset-2.csv')
print(f'Total rows: {df.shape[0]} and Total Columns: {df.shape[1]}')

# Handling Missing Values...
df['extracurriculars'] = df['extracurriculars'].fillna('None')
# in device_type...
df['device_type'] = df['device_type'].fillna('None')
# in grade_category...
print(f'null values are: {df['grade_category'].isnull().sum()}')
print(df['grade_category'].unique())
print(df['grade_category'].mode())
df['grade_category'] = df['grade_category'].fillna('F')  # fill by mode
# remove unnecessary column...
df = df.drop(columns=['student_id'])
# Encoding...
# create a list of categorical columns...
cat_col = ['gender','family_income',
       'parent_education', 'internet_access', 'device_type', 'school_type',
       'extracurriculars','grade_category', 'pass_fail']
le = LabelEncoder()
# create a loop...
label_encoders = {}

for col in cat_col:

    le = LabelEncoder()

    df[col] = le.fit_transform(df[col])

    label_encoders[col] = le

# check the labels...    
le = label_encoders['grade_category']

mapping = dict(zip(le.transform(le.classes_), le.classes_))
# print(mapping)

# **********************converting float into int...*****************************

float_cols = df.select_dtypes(include=['float64']).columns # taking all the float values...
float_cols = float_cols.drop('final_grade')
df[float_cols] = df[float_cols].round().astype(int) # convert into int...
df['final_grade'] = df['final_grade'].round(2) # round up the values

# remove weakly correlated features...
df = df.drop(columns=['age', 'gender', 'group_study_hours', 'family_income', 
                      'parent_education', 'internet_access', 'device_type', 
                      'school_type', 'extracurriculars','grade_category','pass_fail'])

#************************Train test split...*************************

x = df.drop(columns=['final_grade']) # input
y = df['final_grade'] # output

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

# ***********************SCALING****************************
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

x_train_scaled,x_test_scaled,y_train,y_test = train_test_split(x_scaled,y,test_size=0.2,random_state=42)

#*********************Model Building**********************************

model_1 = TabNetRegressor()
model_1.fit(X_train=x_train_scaled,y_train=y_train.values.reshape(-1,1),
            eval_set=[(x_test_scaled,y_test.values.reshape(-1,1))],
            eval_metric=['rmse'],
            max_epochs=100)
#***************************Prediction***********************
pred = model_1.predict(x_test_scaled)
pred = pred.flatten() #Convert shape from 2D

#************************Evaluation************************
mse = mean_squared_error(y_test,pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test,pred)

print(f'mse: {mse}')
print(f'rmse: {rmse}')
print(f'r2: {r2}')
# rmse: 5.328053987055402
# r2: 0.8088657061244788

#******************Save the model******************
joblib.dump(model_1,'model.pkl')
joblib.dump(scaler,'scaler.pkl')