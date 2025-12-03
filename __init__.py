from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  

@app.route("/contact/", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #com

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/extract-minutes/<date_string>/')
def extract_minutes(date_string):
    # date_string : "2024-02-11T11:57:27Z"
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/github-commits/')
def github_commits():
    # 1) Appel à l'API GitHub
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    commits_json = json.loads(raw_content.decode('utf-8'))

    # 2) Dictionnaire minute -> nombre de commits
    stats_par_minute = {}  # ex: {0: 3, 12: 5, 57: 2, ...}

    for commit in commits_json:
        # La date est dans commit["commit"]["author"]["date"]
        date_str = commit["commit"]["author"]["date"]  # "2024-02-11T11:57:27Z"
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute = dt.minute

        if minute not in stats_par_minute:
            stats_par_minute[minute] = 0
        stats_par_minute[minute] += 1

    # 3) On prépare la liste de résultats pour le JSON
    results = []
    for minute, nb in sorted(stats_par_minute.items()):
        results.append({
            'minute': minute,
            'nb_commits': nb
        })

    # 4) On renvoie les données
    return jsonify(results=results)

@app.route("/commits/")
def commits():
    return render_template("commits.html")



if __name__ == "__main__":
  app.run(debug=True)



