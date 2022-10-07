import os
from flask import Flask, render_template, redirect, request
import csv
from datetime import datetime

PET_FOLDER = os.path.join('static', 'fotos')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = PET_FOLDER

@app.route("/")
def bemvindo():
    return render_template('bemvindo.html')

@app.route("/animais")
def animais():
    animais = []
    with open('animais.csv', newline='') as ficheiro:
        for row in csv.reader(ficheiro):
            if(len(row) > 0):
                data = row[4].replace('-', '')
                ano = int(data[:4])
                dia = int(data[6:8])
                mes = int(data[4:6])

                if(dia < 10):
                    dia = '0'+str(dia)

                if(mes < 10):
                    mes = '0'+str(mes)

                animais.append({"nome": row[0],
                                "tutor": row[1],
                                "especie": row[2],
                                "peso": row[3],
                                "data_nascimento": str(dia)+'/'+str(mes)+'/'+str(ano),
                                "contato": row[5],
                                "endereco": row[6],
                                "cidade": row[7],
                                "uf": row[8],
                                "foto": row[9],
                                })
    return render_template('animais.html', animais=animais)

@app.route("/animais/novo")
def formulario():
    return render_template('cadastro.html')

@app.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == "POST":
        if request.files:
            image = request.files["foto"]
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))
            filename = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            with open('animais.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([request.form.get('nome'),
                                 request.form.get('tutor'),
                                 request.form.get('especie'),
                                 request.form.get('peso'),
                                 request.form.get('data_nascimento'),
                                 request.form.get('contato'),
                                 request.form.get('endereco'),
                                 request.form.get('cidade'),
                                 request.form.get('uf'),
                                 filename])

    return redirect('animais')