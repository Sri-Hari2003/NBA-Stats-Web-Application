from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

def one_dict(list_dict):
    keys = list_dict[0].keys()
    out_dict = {key: [] for key in keys}
    for dict_ in list_dict:
        for key, value in dict_.items():
            out_dict[key].append(value)
    return out_dict

nba_teams = teams.get_teams()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/results')
    return render_template('index.html', nba_teams=nba_teams)

@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        team_choice = request.form['team_choice']
        opponent_choice = request.form['opponent_choice']
        stats_type = request.form['stats_type']

        selected_team = next(team for team in nba_teams if team['full_name'] == team_choice)
        selected_opponent = next(team for team in nba_teams if team['full_name'] == opponent_choice)

        team_id = selected_team['id']
        opponent_id = selected_opponent['id']

        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, vs_team_id_nullable=opponent_id)
        gamefinder.get_json()
        games = gamefinder.get_data_frames()[0]

        games_home = games[games['MATCHUP'] == f"{selected_team['abbreviation']} vs. {selected_opponent['abbreviation']}"]
        games_away = games[games['MATCHUP'] == f"{selected_team['abbreviation']} @ {selected_opponent['abbreviation']}"]

        average_plus_minus_away = games_away['PLUS_MINUS'].mean()

        if stats_type == "Get Stats":
            return render_template(
                'results.html',
                selected_team=selected_team['full_name'],
                selected_opponent=selected_opponent['full_name'],
                average_plus_minus_away=average_plus_minus_away,
                games_home=games_home.to_html(),
                games_away=games_away.to_html(),
                display_graph=False
            )
        elif stats_type == "Get Stats graph":
            return redirect(f'/graph/{team_choice}/{opponent_choice}')
    return render_template('results.html', display_graph=False)

@app.route('/graph/<team_choice>/<opponent_choice>')
def graph(team_choice, opponent_choice):
    selected_team = next(team for team in nba_teams if team['full_name'] == team_choice)
    selected_opponent = next(team for team in nba_teams if team['full_name'] == opponent_choice)

    team_id = selected_team['id']
    opponent_id = selected_opponent['id']

    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, vs_team_id_nullable=opponent_id)
    gamefinder.get_json()
    games = gamefinder.get_data_frames()[0]

    games_home = games[games['MATCHUP'] == f"{selected_team['abbreviation']} vs. {selected_opponent['abbreviation']}"]
    games_away = games[games['MATCHUP'] == f"{selected_team['abbreviation']} @ {selected_opponent['abbreviation']}"]

    fig, ax = plt.subplots()
    games_away.plot(x='GAME_DATE', y='PLUS_MINUS', ax=ax)
    games_home.plot(x='GAME_DATE', y='PLUS_MINUS', ax=ax)
    ax.legend(["Away", "Home"])
    plt.title(f"{selected_team['full_name']} vs. {selected_opponent['full_name']} Plus-Minus")
    plt.xlabel("Game Date")
    plt.ylabel("Plus-Minus")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plot_base64 = b64encode(buffer.read()).decode()

    return render_template(
        'results.html',
        plus_minus_plot=plot_base64,
        display_graph=True
    )

if __name__ == '__main__':
    app.run(debug=True)
