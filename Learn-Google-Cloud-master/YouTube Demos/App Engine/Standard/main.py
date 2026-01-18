from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World Welcome to TechTrapture from Standard Environment - Version 3!!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
