from flask import Flask, request, jsonify
from flask import Flask, render_template
import mysql.connector
import os
from matplotlib import pyplot as plt
import io
import base64
from datetime import datetime
app = Flask(__name__)


config = {
    'user': 'root',
    'password': '123qwe',
    'host': '35.184.102.61',
    'database': 'team050',
    'raise_on_warnings': True
}

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/')
def index():
    return render_template('index.html')

def safe_val(value):
    return value if value is not None else 0


@app.route('/update_review', methods=['PUT'])
def update_review():
    data = request.get_json()
    review_id = data.get('ReviewID')
    new_content = data.get('Content')
    new_rate = data.get('Rate')
    if not review_id or new_content is None or new_rate is None:
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        new_rate = int(new_rate)
    except ValueError:
        return jsonify({'error': 'Rate must be an integer'}), 400
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        update_query = """
            UPDATE Review
            SET Content = %s, Rate = %s, Time = %s
            WHERE ReviewID = %s
        """
        cursor.execute(update_query, (new_content, new_rate, current_time, review_id))
        conn.commit()
        print("Review updated successfully")
    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': 'Failed to update review: {}'.format(err)}), 500
    cursor.close()
    conn.close()
    print("Review updated successfully")
    return jsonify({'success': 'Review updated successfully'}), 200

# @app.route('/add_review', methods=['POST'])
# def add_review():
#     data = request.get_json()
#     user_id = data.get('UserId')
#     course_code = data.get('Course_Code')
#     content = data.get('Content')
#     rate = data.get('Rate')
#     if not all([course_code, content, rate, user_id]):
#         return jsonify({'error': 'Missing required parameters'}), 400
#     # Check if rate is an integer
#     try:
#         rate = int(rate)
#     except ValueError:
#         return jsonify({'error': 'Rate must be an integer'}), 400
#     if rate < 1 or rate > 5:
#         return jsonify({'error': 'Rate must be between 1 and 5'}), 400
#     conn = mysql.connector.connect(**config)
#     cursor = conn.cursor()
#     try:
#         # start the transaction
#         conn.start_transaction()  
#         # First query: check if the user has already reviewed this course
#         cursor.execute("""
#             SELECT ReviewID FROM Review
#             WHERE UserId = %s AND Course_Code = %s
#         """, (user_id, course_code))
#         review_exists = cursor.fetchone()
#         if review_exists:
#             return jsonify({'error': 'User has already reviewed this course'}), 400
#         # Second query: insert the new review
#         cursor.execute("SELECT MAX(CAST(ReviewID AS UNSIGNED)) FROM Review")
#         max_id_result = cursor.fetchone()
#         new_id = str(int(max_id_result[0]) + 1) if max_id_result[0] else '1'
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         # try to insert the new review
#         insert_query = """
#             INSERT INTO Review (ReviewID, UserId, Course_Code, Content, Rate, Time)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(insert_query, (new_id, user_id, course_code, content, rate, current_time))
#         conn.commit()  
#         return jsonify({'success': 'Review added successfully', 'ReviewID': new_id}), 201
#     except mysql.connector.Error as err:
#         # if any error occurs, rollback the transaction
#         conn.rollback() 
#         return jsonify({'error': str(err)}), 500
#     finally:
#         cursor.close()
#         conn.close()


@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    print(data)
    user_id = data.get('UserId')
    course_code = data.get('Course_Code')
    content = data.get('Content')
    rate = data.get('Rate')

    if not all([course_code, content, rate, user_id]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        rate = int(rate)
        if rate < 1 or rate > 5:
            return jsonify({'error': 'Rate must be between 1 and 5'}), 400
    except ValueError:
        return jsonify({'error': 'Rate must be an integer'}), 400

    conn = mysql.connector.connect(**config)
    print(conn)
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        args = (user_id, course_code, content, rate, 0, '')
        result_args = cursor.callproc('AddReview', args)
        conn.commit()
        print("ReviewID: ", result_args[4])
        print("Result: ", result_args[5])
        # print(review_id, message)
        if result_args[5] == 'Review added successfully':
            return jsonify({'success': result_args[5], 'ReviewID': result_args[4]}), 201
        else:
            conn.rollback()
            return jsonify({'error': result_args[5]}), 400
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_review', methods=['DELETE'])
def delete_review():
    data = request.get_json()
    review_id = data.get('ReviewID')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    print(review_id)
    try:
        cursor.execute("DELETE FROM Review WHERE ReviewID = %s", (review_id,))
        conn.commit()
        print("Review deleted successfully")
    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        print("Failed to delete review:")
        return jsonify({'error': 'Failed to delete review: {}'.format(err)}), 500
    cursor.close()
    conn.close()
    # print("Review deleted successfully")
    return jsonify({'success': 'Review deleted successfully'}), 200

@app.route('/insert_grade', methods=['POST'])
def insert_grade():

    data = request.get_json()  # Get JSON data from the request
    print(data)
    # Extract all required and optional parameters
    year_term = data.get('YearTerm')
    primary_instructor = data.get('PrimaryInstructor')
    course_code = data.get('Course_Code')
    grades = {
        'Number_of_A+': data.get('Number_of_A+', 0),
        'Number_of_A': data.get('Number_of_A', 0),
        'Number_of_A-': data.get('Number_of_A-', 0),
        'Number_of_B+': data.get('Number_of_B+', 0),
        'Number_of_B': data.get('Number_of_B', 0),
        'Number_of_B-': data.get('Number_of_B-', 0),
        'Number_of_C+': data.get('Number_of_C+', 0),
        'Number_of_C': data.get('Number_of_C', 0),
        'Number_of_C-': data.get('Number_of_C-', 0),
        'Number_of_D+': data.get('Number_of_D+', 0),
        'Number_of_D': data.get('Number_of_D', 0),
        'Number_of_D-': data.get('Number_of_D-', 0),
        'Number_of_F': data.get('Number_of_F', 0),
        'Number_of_W': data.get('Number_of_W', 0)
    }
    # Check for required fields
    if not all([year_term, primary_instructor, course_code]):
        print('Missing required fields')
        return jsonify({'error': 'Missing required fields'}), 400
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        conn.start_transaction()  # Start the transaction
        # Prepare the SQL statement
        insert_query = """
        INSERT INTO Grade (
            YearTerm, PrimaryInstructor, Course_Code,
            `Number_of_A+`, Number_of_A, `Number_of_A-`,
            `Number_of_B+`, Number_of_B, `Number_of_B-`,
            `Number_of_C+`, Number_of_C, `Number_of_C-`,
            `Number_of_D+`, Number_of_D, `Number_of_D-`,
            Number_of_F, Number_of_W
        ) VALUES (
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s
        )
        """
        # Execute the SQL statement
        cursor.execute(insert_query, (
            year_term, primary_instructor, course_code,
            grades['Number_of_A+'], grades['Number_of_A'], grades['Number_of_A-'],
            grades['Number_of_B+'], grades['Number_of_B'], grades['Number_of_B-'],
            grades['Number_of_C+'], grades['Number_of_C'], grades['Number_of_C-'],
            grades['Number_of_D+'], grades['Number_of_D'], grades['Number_of_D-'],
            grades['Number_of_F'], grades['Number_of_W']
        ))
        conn.commit()  # Commit the transaction
        print('successful insert grade')
        return jsonify({'success': 'Grade entry added successfully'}), 201
    except mysql.connector.Error as err:
        print('connect error')
        conn.rollback()  # Rollback in case of error
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_user_reviews', methods=['GET'])
def get_user_reviews():
    user_id = request.args.get('user_id')  
    print(user_id)
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True) 
    try:
        cursor.callproc('GetUserReviewedCourses', [user_id])
        for result in cursor.stored_results():
            user_reviews = result.fetchall()  
            print('retrevial successfully')

        print(user_reviews)
        return jsonify({'user_reviews': user_reviews}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    print(data)
    course_code = data.get('Course_Code')
    YearTerm = data.get('YearTerm')
    if not course_code or not YearTerm:
        return jsonify({'error': 'Missing course_code parameter'}), 400
    # Format the input course code to be more flexible for matching
    # For instance, converting 'ECE408' to '%ECE%408%'
    formatted_code = "%" + "%".join(course_code.split()) + "%"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Course WHERE Course_Code LIKE %s"
    cursor.execute(query, (formatted_code,))
    result = cursor.fetchone()
    if result:
        formatted_code = result['Course_Code']
        review_query = "SELECT ReviewID, Time, Content, Rate, UserId FROM Review WHERE Course_Code = %s"
        cursor.execute(review_query, (formatted_code,))
        reviews = cursor.fetchall()
        if reviews:
            result['Reviews'] = reviews
        query_gpa = "SELECT * FROM Grade WHERE Course_Code = %s AND YearTerm = %s"
        cursor.execute(query_gpa, (formatted_code, YearTerm))
        GPAs = cursor.fetchall()
        if GPAs:
            result['GPA'] = GPAs
            grades_distribution_query = """
                    SELECT
                        SUM(`Number_of_A+`) as `A+`,
                        SUM(Number_of_A) as `A`,
                        SUM(`Number_of_A-`) as `A-`,
                        SUM(`Number_of_B+`) as `B+`,
                        SUM(Number_of_B) as `B`,
                        SUM(`Number_of_B-`) as `B-`,
                        SUM(`Number_of_C+`) as `C+`,
                        SUM(Number_of_C) as `C`,
                        SUM(`Number_of_C-`) as `C-`,
                        SUM(`Number_of_D+`) as `D+`,
                        SUM(Number_of_D) as `D`,
                        SUM(`Number_of_D-`) as `D-`,
                        SUM(Number_of_F) as `F`
                    FROM Grade
                    WHERE Course_Code = %s AND YearTerm = %s
                """
            cursor.execute(grades_distribution_query, (formatted_code, YearTerm))
            grades_distribution = cursor.fetchone()
            if grades_distribution:  
                grades_distribution = {k: safe_val(v) for k, v in grades_distribution.items()}
                total = sum(grades_distribution.values())       
                if total > 0:
                    for grade in grades_distribution:
                        grades_distribution[grade] = (grades_distribution[grade] / total) * 100
                fig, ax = plt.subplots()
                ax.bar(grades_distribution.keys(), grades_distribution.values(), color='blue')
                ax.set_xlabel('Grades')
                ax.set_ylabel('Percentage (%)')
                ax.set_title('Grade Distribution')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                buf.close()
                result['Grade_Distribution_Chart'] = img_base64
    cursor.close()
    conn.close()
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Course not found'}), 404

    
@app.route('/signup', methods=['POST'])
def signup():
    # print("a")
    data = request.json
    id = data.get('id')
    password = data.get('password')
    gender = data.get('gender')
    age = data.get('age')
    degree = data.get('degree')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO User (UserId, Password, Gender, Age, Degree) VALUES (%s, %s, %s, %s, %s)',
                   (id, password, gender, age, degree))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Sign Up successfull!'}), 200

@app.route('/signin', methods=['POST'])
def login():
    data = request.json
    id = data.get('id')
    password = data.get('password')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    # Check if ID and password are correct
    query = "SELECT * FROM User WHERE UserId = %s AND Password = %s"
    cursor.execute(query, (id, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify({'status': 'ok'}),200
    else:
        return jsonify({'status': 'error', 'message': 'Incorrect ID or password'}), 401

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
