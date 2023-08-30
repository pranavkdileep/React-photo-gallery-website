import mysql.connector

connection = mysql.connector.connect(
    host='sql.freedb.tech',
    user='freedb_pkdart',
    password='e2Q#U?#QD$2ms7v',
    database='freedb_testingkk'
)
cursor = connection.cursor()

cursor.execute("CREATE TABLE prompts (image_id INT, prompt VARCHAR(255), negative_prompt VARCHAR(255), height INT, width INT)")
connection.commit()
cursor.close()
connection.close()
