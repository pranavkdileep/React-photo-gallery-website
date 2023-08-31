import mysql.connector

connection = mysql.connector.connect(
    host='sql9.freesqldatabase.com',
    user='sql9643553',
    password='VL7BkQ7ta8',
    database='sql9643553'
)
cursor = connection.cursor()

cursor.execute("CREATE TABLE prompts (image_id INT, prompt VARCHAR(255), negative_prompt VARCHAR(255), height INT, width INT)")
connection.commit()
cursor.close()
connection.close()
