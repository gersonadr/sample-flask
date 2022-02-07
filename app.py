from flask import Flask
from flask import render_template
import models
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/test")
def gimme_obj():
    park = models.Park(1, "my_house", ["swings", "shop"], 50, 60)
    park_dict = models.convert_park_to_dict(park)
    return json.dumps(park_dict, default=lambda o: o.__dict__, sort_keys=True, indent=4)
