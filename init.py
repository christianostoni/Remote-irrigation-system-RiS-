from flask import Flask, render_template, url_for, redirect, request, Response
import time
from datetime import datetime, timedelta
import serial
import RPi.GPIO as gpio
import os
from database import Database

led = 14
global sec
app = Flask(__name__)

# Inizializza il database
database = Database()

ser = serial.Serial('/dev/ttyACM0', 9600)
gpio.setmode(gpio.BCM)
gpio.setup(led, gpio.OUT)

@app.route('/')
def login():
    if request.cookies.get('token') != None:
        user = database.retrive_token(request.cookies.get('token'))
        if user: return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/login/success', methods = ['POST'])
def login_success():
    if request.method == 'POST':
            udata = request.get_json()
            if database.login(udata['user'], udata['password']):
                login = Response(status=200)
                login.set_cookie("token",
                    value=database.gen_token(udata['user'], udata['password']), 
                    expires=(datetime.today() + timedelta(days=14)),
                    samesite="Strict"
                )
                return login
            else:
                return Response(status=500)

@app.route('/register/success', methods = ['POST'])
def register_success():
    if request.method == 'POST':
        udata = request.get_json()
        if database.register(udata['user'], udata['password']):
            register = Response(status=200)
            register.set_cookie('token', value=request.cookies.get('token'), expires=0, samesite="Strict")
            database.delete_account('admin')
            return register
        else:
            return Response(status=500)

@app.route('/logout')
def logout():
    logout = redirect('/')
    database.destroy_token(request.cookies.get('token'))
    logout.set_cookie('token', value=request.cookies.get('token'), expires=0, samesite="Strict")
    return logout

@app.route('/home', methods=['GET'])
def home():
    # controlla se l'utente è autorizzato
    if not database.retrive_token(request.cookies.get('token')): return Response(response="<h3>Errore 405:</h3>Token d'accesso <u>mancante</u> o <u>scaduto</u>", status=405)

    value = ser.readline().decode().strip()
    if int(value) >= 200:
        stato = 'bagnata'
    else:
        stato = 'da irrigare'
    data = {'umidita': value,
            'stato': stato}
    gpio.output(led, gpio.LOW)
    return render_template('index.html', **data)

@app.route('/irriga', methods=['GET'])
def irriga():
    # controlla se l'utente è autorizzato
    if not database.retrive_token(request.cookies.get('token')): return Response(response="<h3>Errore 405:</h3>Token d'accesso <u>mancante</u> o <u>scaduto</u>", status=405)

    sec = request.form.get('secondi')
    if len(sec) == 0:
        sec = 5
    gpio.output(led, gpio.HIGH)
    time.sleep(int(sec))
    gpio.output(led, gpio.LOW)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug = True, port = 4444, host='127.0.0.1')