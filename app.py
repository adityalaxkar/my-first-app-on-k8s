from flask import Flask
import os

app = Flask(name)

@app.route('/')
def hello():
    return '<h1> welcome to My First Python Web App!'</h1><p>Running on Kuberenetes Deployed by Adityal</p>

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)