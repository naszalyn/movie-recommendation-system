import mysql.connector

cnx = mysql.connector.connect(user='user1', password='Passw0rd',
                              host='127.0.0.1',
                              database='recommendation_system_db',
                              use_pure=False)

cursor = cnx.cursor()



def execute(sql):
    try:
        cursor.execute(sql)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno != 1062:
            with open("insert_errors.txt", "a") as myfile:
                text = sql + ";" + str(err._full_msg) + "\n"
                myfile.write(text)

def read(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        with open("read_errors.txt", "a") as myfile:
                text = sql + ";" + str(err._full_msg) + "\n"
                myfile.write(text)


def close_connection():
    cursor.close()
    cnx.close()