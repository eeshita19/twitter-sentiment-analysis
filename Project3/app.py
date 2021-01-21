import flask
from flask import Flask, request, render_template  
from datetime import datetime
import tweetcheck
from tweetcheck import main_app


app = Flask(__name__)

@app.route('/',methods =["GET", "POST"])



#return HELLO_HTML.format(name, str(datetime.now())) 

def index():
      
    if request.method == "POST":
        screen_name = request.form.get("sname") 
        main_app(str(screen_name))
        
        return render_template('IMG.html', name = str(screen_name), url ='/static/images/new_plot.png')

       
        #return "Checking for screen name " + screen_name
    return render_template("form.html")



if __name__ == "__main__":
    app.debug = True
    print("Started!!")
    app.run(host='0.0.0.0', port = 5000)