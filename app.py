from flask import Flask, render_template
import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    with open('ids.txt', 'r') as archivo:
        ids = archivo.readlines()

    scores = []
    teams = []
    for id in ids:
        url = f"https://api.angstromctf.com/competitions/6/teams/{id.strip()}"

        respuesta = requests.get(url.strip())
        contenido = respuesta.text
        team = ""
        score = 0
        datos = json.loads(contenido)
        team = datos['name']
        for solve in datos['solves']:
            score += solve['challenge']['value']
        scores.append(score)
        teams.append(team)

    sns.set_style('whitegrid')
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=teams, y=scores)
    ax.set_title('team score chart')
    ax.set_xlabel('Team')
    ax.set_ylabel('Score')
    plt.tight_layout()

    img_data = plt.savefig('static/images/grafica.png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
