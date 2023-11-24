from flaskPart import app
from flask import render_template
from flaskPart.forms.open import Open
from flaskPart.forms.close import Close


@app.route("/")
def home():
    form1 = Open()
    form2 = Close()
    if form1.validate_on_submit():
        print("open!!")
    
    if form2.validate_on_submit():
        print("close!!!")

    return render_template("home.html",form1 = form1,form2 = form2)

