from solcx import compile_standard
from flask import Flask
from flask import render_template
import models
import solcx
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

@app.route("/compile/<initial_supply>")
def compile_sol(initial_supply):
    solcx.install_solc("0.8.0")

    with open("./contracts/OurToken.sol", "r") as file:
        our_token = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"OurToken.sol": {"content": our_token}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )

    result = compiled_sol["contracts"]["OurToken.sol"]["BEP20NoDependencies"]["evm"]["bytecode"]["object"]

    if not initial_supply:
        initialSupplyInt = 1000000000000000000000000
    else:
        initialSupplyInt = int(initial_supply)

    result += str(hex(initialSupplyInt)[2:]).zfill(64)
    return result
