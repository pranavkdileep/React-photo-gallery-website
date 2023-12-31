from flask import Flask, render_template, request
import mysql.connector
import random
from flask import jsonify
import os

dbhost = os.environ.get('DB_HOST') or 'sql9.freesqldatabase.com'
user = os.environ.get('DB_USER') or 'sql9643553'
password = os.environ.get('DB_PASSWORD') or 'VL7BkQ7ta8'
database = os.environ.get('DB_DATABASE') or 'sql9643553'


app = Flask(__name__,template_folder="template")

@app.route('/')
def prompt_form():
    return render_template('form.html')

@app.route('/save', methods=['POST'])
def save_to_database():
    # Retrieve form data
    prompt = request.form['prompt']
    negative_prompt = request.form['negative_prompt']
    height = request.form['height']
    width = request.form['width']
    image_id = random.randint(100000,999999)
    
    # Create a connection to the MySQL database
    connection = mysql.connector.connect(
        host=dbhost,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    
    # Save the data to the databasej
    query = "INSERT INTO prompts (image_id, prompt, negative_prompt, height, width) VALUES (%s, %s, %s, %s, %s)"
    values = (image_id, prompt, negative_prompt, height, width)
    cursor.execute(query, values)
    connection.commit()
    
    # Close the database connection
    cursor.close()
    connection.close()
    
    return str(image_id)

@app.route('/getprompt')
def get_prompt():
    connection = mysql.connector.connect(
        host=dbhost,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM prompts"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    if count == 0:
        return "No prompts in database"
    else:
        query = "SELECT * FROM prompts ORDER BY RAND() LIMIT 1"
        cursor.execute(query)
        prompt = cursor.fetchone()
        response_data = {
            'image_id': prompt[0],
            'prompt': prompt[1],
            'negative_prompt': prompt[2],
            'height': prompt[3],
            'width': prompt[4]
        }
        return jsonify(response_data)

@app.route('/del_image/<image_id>', methods=['GET'])
def del_image(image_id):
    # You can perform any processing or validation here if needed
    
    # Returning the image ID in the response
    response_data = {
        'image_id': image_id
    }
    connection = mysql.connector.connect(
        host=dbhost,
        user=user,
        password=password,
        database=database
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to delete the prompt with the specified image_id
    query = "DELETE FROM prompts WHERE image_id = %s"

    # Execute the query with the image_id as a parameter
    cursor.execute(query, (image_id,))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return jsonify(response_data)

@app.route('/upload_db', methods=['POST'])
def upload_db():
    image_link = request.form['image_link']
    image_id = request.form['image_id']
    prompt = request.form['prompt']
    negative_prompt = request.form['negative_prompt']
    height = request.form['height']
    width = request.form['width']
    connection = mysql.connector.connect(
        host=dbhost,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    #check if image_id already exists
    query = "SELECT COUNT(*) FROM images WHERE image_id = %s"
    cursor.execute(query, (image_id,))
    count = cursor.fetchone()[0]
    if count != 0:
        return 'Image ID already exists'
    else:
        qury = "INSERT INTO images (image_link, image_id, prompt, negative_prompt, height, width) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (image_link, image_id, prompt, negative_prompt, height, width)
        cursor.execute(qury, values)
        connection.commit()
        cursor.close()
        connection.close()
        return 'Data saved successfully'


if __name__ == '__main__':
    app.run()
