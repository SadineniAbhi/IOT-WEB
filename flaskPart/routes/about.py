from flask import render_template
from flaskPart import app

@app.route("/about")
def about():
    return render_template("about.html")


###########################################################################
    #@@@@@@@@@ contributed by Abhijeeth Sadineni@@@@@@@@@@@@@@@@@@#
###########################################################################