from flask import Flask, render_template, url_for, redirect, request
import time
import serial
import RPi.GPIO as gpio
import asyncio

led = 14
global sec
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600)
gpio.setmode(gpio.BCM)
gpio.setup(led, gpio.OUT)

@app.route('/', methods=["POST", "GET"])
def home():

    value = ser.readline().decode().strip()
    data = {'val1': value}
    gpio.output(led, gpio.LOW)
    return render_template('index.html', **data)
    

@app.route('/irriga', methods=["POST", "GET"])
def irriga():
    sec = request.form.get('secondi')
    if len(sec) == 0:
        sec = 5
    gpio.output(led, gpio.HIGH)
    time.sleep(int(sec))
    gpio.output(led, gpio.LOW)
    return redirect(url_for("home"))

    
if __name__ == '__main__':
    app.run(debug = True, port = 8080, host='192.168.1.20')
