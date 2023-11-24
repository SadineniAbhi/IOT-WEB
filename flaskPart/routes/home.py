from flaskPart import app
from flask import render_template
from flaskPart.forms.open import Open
from flaskPart.forms.close import Close
from ArdChip import set
@app.route("/",methods=["POST","GET"])
def home():
    form1 = Open()
    form2 = Close()
    if form1.open.data and form1.validate():
        set(1)
    if form2.close.data and form2.validate():
        set(2)

    return render_template("home.html",form1 = form1,form2 = form2)

###########################################################################
    #@@@@@@@@@ contributed by Abhijeeth Sadineni@@@@@@@@@@@@@@@@@@#
###########################################################################