from flask import Flask, request, render_template
from user import insert_user, insert_data


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    Nume = request.form['Nume']
    Prenume = request.form['Prenume']
    Companie = request.form['Companie']
    Id_Manager = request.form['Id_Manager']

    insert_user(Nume, Prenume, Companie, Id_Manager)

    return "Datele au fost primite și înregistrate în baza de date!"

@app.route('/admin', methods=['POST'])
def admin_add_user():
    Nume = request.form['Nume']
    Prenume = request.form['Prenume']
    Companie = request.form['Companie']
    Id_Manager = request.form['Id_Manager']

    insert_user(Nume, Prenume, Companie, Id_Manager)

    return "Utilizatorul a fost inregistrat de catre administrator!"

@app.route('/insert_data', methods=['POST'])
def insert_json_data():
    return insert_data()

if __name__ == '__main__':
    app.run(debug=True)
