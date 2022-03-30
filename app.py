
from flask import Flask
from flask import render_template
# import compiler
import models
import price
import json


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/price/<chain_id>/<ref_token>/<my_token>")
def get_price(chain_id, ref_token, my_token):
    return json.dumps(price.get_price(chain_id, ref_token, my_token))

@app.route("/test")
def gimme_obj():
    park = models.Park(1, "my_house", ["swings", "shop"], 50, 60)
    park_dict = models.convert_park_to_dict(park)
    return json.dumps(park_dict, default=lambda o: o.__dict__, sort_keys=True, indent=4)

# @app.route("/price/<contract_address>")
# def compile_sol(initial_supply):

#     contract_file = "./contracts/OurToken.sol"
#     return compiler.compile(contract_file, initial_supply)

# @app.route("/compile/<initial_supply>")
# def compile_sol(initial_supply):

#     contract_file = "./contracts/OurToken.sol"
#     return compiler.compile(contract_file, initial_supply)
