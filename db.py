import pymysql 
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:@localhost/student_exam_managemet')

# connection = mysql.connector.connect(host='localhost',
#                              user='root',
#                              password='',
#                              db='student_exam_managemet',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# con=connection.cursor()

df=pd.read_sql('select * from students;',engine)

print(df)

