import mysql.connector
from flask import request, jsonify  
from datetime import datetime



def insert_user(nume, prenume, companie, id_manager):
   
    connection = mysql.connector.connect(host='localhost', user='root', password='', database='')
    cursor = connection.cursor()

    query = "INSERT INTO users (nume, prenume, companie, id_manager) VALUES (%s, %s, %s, %s)"
    values = (nume, prenume, companie, id_manager)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def insert_data():
    # Codul pentru inserarea datelor JSON în baza de date MySql
    try:
        data = request.json
        data_date_str = data['data']
        data_date = datetime.strptime(data_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database=''
        )
        cursor = connection.cursor()

        query = "INSERT INTO access (data, sens, id, id_poarta) VALUES (%s, %s, %s, %s)"
        values = (data_date, data['sens'],
                  data['idPersoana'], data['idPoarta'])

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        # Creaza un nou obiect JSON in formatul dorit
        new_json = {
            "data": data_date.strftime('%Y-%m-%d %H:%M:%S'),
            "sens": data['sens'],
            "id": data['idPersoana'],
            "id_poarta": data['idPoarta']
        }

        return jsonify(new_json), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
