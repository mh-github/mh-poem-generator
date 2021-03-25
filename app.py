import random
from flask import Flask, request, render_template, jsonify
from PoemGenerator import PoemGenerator

app = Flask(__name__)

data_erica          = open('erica_jong_2012_3.txt', 'r').read().lower()
model_erica         = 'erica_pg.model.h5'

data_lavanya        = open('lavanya.txt', 'r').read().lower()
model_lavanya       = 'lavanya_pg.model.h5'

data_erica_lavanya  = open('erica_lavanya.txt', 'r').read().lower()
model_erica_lavanya = 'erica_lavanya_pg.model.h5'

default_seed_texts  = ["i love you", "break my heart", "my dreams with you",
                       "walk in rain"]

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

def makeHeader(poem_header, seed_text, poet):
    poem_header.append("Generated Poem")
    poem_header.append("[Seed Text = " + seed_text + " ]")
    poem_header.append("[Poems data corpus of " + poet + " ]")
    poem_header.append("=============================")

@app.route("/getpoem", methods=['GET'])
def generatePoem():
    seed_text = request.args.get("seed_text") or random.choice(default_seed_texts)
    poet      = request.args.get("poet") or "lavanya"

    if poet   == "erica":
        data      = data_erica
        model     = model_erica
    elif poet == "lavanya":
        data      = data_lavanya
        model     = model_lavanya
    elif poet == "erica_lavanya":
        data      = data_erica_lavanya
        model     = model_erica_lavanya

    pg   = PoemGenerator(seed_text, data, model)
    poem = pg.generate_poem()

    poem_header = []
    makeHeader(poem_header, seed_text, poet)

    return jsonify({'poem_header': poem_header, 'poem': poem})

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()