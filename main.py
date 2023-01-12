from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request, redirect, url_for,session
from sqlalchemy import create_engine
from generationstd import generate_student_id
import mysql.connector
import pandas as pd
import urllib.request
import os
import random
import json
import base64
import cv2
import numpy as np
import face_recognition


engine = create_engine('mysql+mysqlconnector://root:@localhost/student_exam_managemet')

# picsfolder=os.path.join()

app=Flask(__name__)

UPLOAD_FOLDER='static/uploads/'

app.config['UPLOAD_FOLDER']='static/images'

app.secret_key = 'hello'

# Enable sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True



from flask import Flask, request, redirect, url_for

# app = Flask(__name__)

# @app.route('/t', methods=['POST','GET'])
# def t():

#   # Get the image data from the request
#     print('kdkkd')
#     print(request.method)
#     print(request.form)
#     # print(request.files)
#     if request.method=='POST':
#         image_data = request.form['student_image']

#     # Save the image data to a file
#         with open('images/student_image.jpeg', 'wb') as f:
#             f.write(image_data.decode('base64'))
#         return 'Form submitted successfully!'
#     return render_template('test_image.html')


  # Redirect to the index page
#   return redirect(url_for('index'))

# @app.route('/question')
# def question():
#     return '0'
#     # Get the user with the specified ID
#     question = User.query.get(id)
#     return render_template('user.html', user=user)

# def removequestion():
#     print('in remove')
#     print(session['questions'])
#     return session['questions'].pop()

# @app.route('/question/<int:question_id>')
# def face():
#     student_id=session.get('student_id')
#     student_image=app.config['UPLOAD_FOLDER']+'/'+str(student_id)+'.jpg'
#     student_name = session.get('student_name')

#     student_image = face_recognition.load_image_file(student_image)
#     student_face_encoding = face_recognition.face_encodings(student_image)[0]
#     known_face_encodings = [
#     student_face_encoding]
#     known_face_names=[student_name]
#     cap=cv2.VideoCapture(0)
#     while True:
#         ret,frame=cap.read()
#         rgb_frame = frame[:, :, ::-1]

#         # Find all the faces and face enqcodings in the frame of video
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             # See if the face is a match for the known face(s)
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#             name = "Unknown"

#             # If a match was found in known_face_encodings, just use the first one.
#             # if True in matches:
#             #     first_match_index = matches.index(True)
#             #     name = known_face_names[first_match_index]

#             # Or instead, use the known face with the smallest distance to the new face
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)
#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]

#             # Draw a box around the face
#     #         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#             # Draw a label with a name below the face
#     #         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#     #         font = cv2.FONT_HERSHEY_DUPLEX
#     #         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#             print(name)


# #         cv2.imshow('Video',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()





@app.route('/your-route-url', methods=['POST'])
def handle_value():
    print(request.json)
    value = request.json.get('value')
    question = request.json.get('question')

    print(value,'--value',question)

    
    # do something with value
    return "Value received"


@app.route('/marks')
def marks():
    print('marks')

# @app.route('/lastquestion')
# def lastquestion():
#     return redirect


@app.route('/callnextquestion')
def callnextquestion():
    # print(request.args.get('choice'))
    # print(request.form,'req',request.args.get('choice'),request.method)
    # print(session['questions'])
    try:
        question=session['questions'].pop()
        print(question)
        return redirect(f'/question/{question}')
    except:
        try:
            question=session['questions'][0]
            print(question)
            return redirect(f'/question/{question}')
        except:
            return 'no more questions'

  # Render the template for the route


@app.route('/question/<int:question_id>')
def question(question_id):
    # face()
    
    # print(request.form,'req',request.method)
    student_id=session.get('student_id')
    student_image=app.config['UPLOAD_FOLDER']+'/'+str(student_id)+'.jpg'
    student_name = session.get('student_name')

    student_image = face_recognition.load_image_file(student_image)
    student_face_encoding = face_recognition.face_encodings(student_image)[0]
    known_face_encodings = [
    student_face_encoding]
    known_face_names=[student_name]
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        rgb_frame = frame[:, :, ::-1]
        cv2.imwrite(f"static/images/{student_id}screenshot.jpg",frame)

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if int(len(face_locations))>2:
            return 'cheating'


        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draw a box around the face
    #         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
    #         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #         font = cv2.FONT_HERSHEY_DUPLEX
    #         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            print(name)
        print(question_id)
        print(session['questions'])
        # print('in question')
        question_text=pd.read_sql_query(f'select text from questions where question_id={question_id}',engine).iloc[0][0]
        choice_text_list=pd.read_sql_query(f'select choice_text from choices where question_id={question_id}',engine ).iloc[:,0].to_list()
        print(question_text)
        session['iterator']=0
        question=session['questions'].pop()

        # if len(session['questions'])!=0:
        #     return redirect(f'/question?{question}')
        # try:
        #     question=session['questions'].pop(1)
        # except:
        #     try:
        #         question=session['questions'][0]
        #     except:
        #         return 'questions are empty'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cap.release()
        cv2.destroyAllWindows()
        return render_template('question.html',question=question_text,choices=choice_text_list,question_id=question)


#         cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    print(question_id)
    print(session['questions'])
    # print('in question')
    question_text=pd.read_sql_query(f'select text from questions where question_id={question_id}',engine).iloc[0][0]
    choice_text_list=pd.read_sql_query(f'select choice_text from choices where question_id={question_id}',engine ).iloc[:,0].to_list()
    print(question_text)
    session['iterator']=0
    question=session['questions'].pop()
    # if len(session['questions'])!=0:
    #     return redirect(f'/question?{question}')
    # try:
    #     question=session['questions'].pop(1)
    # except:
    #     try:
    #         question=session['questions'][0]
    #     except:
    #         return 'questions are empty'
    return render_template('question.html',question=question_text,choices=choice_text_list,question_id=question)


@app.route('/test/<int:test_id>')
def test(test_id):
    d=pd.read_sql_query(f'select question_id from test_questions where test_id={test_id} ',engine)
    question_ids=[]
    for _,i in d.iterrows():
        question_ids.append(str(i['question_id']))
    # print(question_ids)
    # questions_length=len(question_ids)
    # a=question_ids.copy()
    # print(type(a),type(question_ids),a,question_ids)
    session['questions']=question_ids
    print(session['questions'])
    random.shuffle(session['questions'])
    print(session['questions'])
    # question=removequestion()
    # print(question)

    session['marks']=0



    # for question in question_ids:
    #     question_fun(question)
    
    return render_template('firstquestion.html')


    
#     # Get the user with the specified ID
#     question = User.query.get(id)
#     return render_template('user.html', user=user)

@app.route('/taketest')
def taketest():
    student_id=session.get('student_id')
    image=app.config['UPLOAD_FOLDER']+'/'+str(student_id)+'.jpg'
    # student_tests=pd.read_sql_query(f'''select test_name from test t inner join student_tests st on t.test_id=st.test_id inner join students s on st.student_id=s.student_id  where s.student_id={student_id}''',engine).iloc[:,0].to_list()
    df=pd.read_sql_query(f'''select test_name,t.test_id from test t inner join student_tests st on t.test_id=st.test_id inner join students s on st.student_id=s.student_id  where s.student_id={student_id}''',engine)
    test_list=[]
    for _,i in df.iterrows():
        test={}
        test['test_id']=int(i['test_id'])
        test['test_name']=i['test_name']
        test_list.append(test)
    return render_template('take_test.html',student_tests=test_list,image=image)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    #check if student is logged in properly
    if 'login' in session:
        student_name = session.get('student_name')
        student_image = session.get('student_image')
        student_id=session.get('student_id')
        image=app.config['UPLOAD_FOLDER']+'/'+str(student_id)+'.jpg'
        return render_template('student.html',student_name=student_name,image=image)
    else:
        return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        student_emails=pd.read_sql_query('select student_email from students;',engine)

        student_email_new=request.form['email']
        student_password_new=request.form['password']
        print(student_email_new)
        print(student_emails)
        if student_email_new in student_emails.values:
            std_pswd=pd.read_sql_query(f'''select student_password from students where student_email='{student_email_new}';''',engine)
            if student_password_new == std_pswd.values:
                session['student_name']=pd.read_sql_query(f'''select student_name from students where student_email='{student_email_new}';''',engine).values[0][0]
                session['image_path']=pd.read_sql_query(f'''select student_image from students where student_email='{student_email_new}';''',engine).values[0][0]
                print('ok')
                session['student_id']=str(pd.read_sql_query(f'''select student_id from students where student_email='{student_email_new}';''',engine).values[0][0])
                session['login']='student'

                return redirect('/dashboard')
            else:
                return 'password is wrong'
        else:
            return 'email not found'


    return render_template('student_login.html')

@app.route('/signup')
def hello():
    return render_template('student_signup.html')

# @app.route('/test')
# def test():
#     return render_template('test_image.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     print('im in')
#     # Get the image file from the request
#     image = request.files['image']
#     print(request.files['image'])

    

#     # return 'hello'
    
#     # Save the image file to the filesystem
#     image.save('images/image.jpg')
    
#     return redirect(url_for('hello'))

@app.route('/signup', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get the form data
        student_id = generate_student_id()
        student_name = request.form['student_name']
        student_email = request.form['student_email']
        student_password = request.form['student_password']
        # student_image = request.files['student_image']
        student_image=request.form['image_hidden']
        student_image = bytes(student_image, 'utf-8')
        student_image = base64.decodebytes(student_image)
        student_age = int(request.form['student_age'])
        student_course = request.form['student_course']

        print(student_id, 'student id')

        print(request.files)


        print(student_image)
        # exit(0)

        # student_image.save(f'static/images/{student_id}.jpg')
        with open(f'static/images/{student_id}.jpg', 'wb') as f:
            f.write(student_image)

        
        a=[student_id,student_name,student_email,student_password,student_age,student_course]
        for i in a :
            print(i,type(i))
       

        # Connect to the database
        connection = mysql.connector.connect(host='localhost',
                                             user='root',
                                             password='',
                                             database='student_exam_managemet')

        # Save the form data to the database
        cursor = connection.cursor()

        # query=f'INSERT INTO students (student_id, student_name, student_email, student_password, student_age, student_course) VALUES \
        #     ({str(student_id)}, {str(student_name)}, {str(student_email)}, {str(student_password)}, {int(student_age)}, {str(student_course)});'
        
        # print(query)
        student_id=int(student_id)
        cursor.execute(cursor.execute('INSERT INTO students (student_id,student_name, student_email, student_password,student_image ,student_age, student_course) VALUES (%s, %s, %s, %s,%s, %s, %s)', (student_id,student_name, student_email, student_password,f'images/{student_id}.jpg', student_age, student_course)))
        connection.commit()
        cursor.close()

        # Process the form data (e.g., save to a database, send an email, etc.)

        return redirect(url_for('success'))
    return render_template('student_signup.html')

@app.route('/success')
def success():
    return 'Form submitted successfully!'


if __name__ == '__main__':
    app.run()