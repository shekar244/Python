
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def login():
  return render_template('login1.html')

@app.route('/register')
def about():
  return render_template('Regis1.html')

if __name__=="__main__": 
  app.run(debug= True) 
