from flask import Flask, render_template, request, redirect, url_for
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

app = Flask(__name__)

# Fetch the list of NBA teams
nba_teams = teams.get_teams()

@app.route('/')
def index():
    return render_template('index.html', nba_teams=nba_teams)

@app.route('/results', methods=['POST'])
def results():
    team_choice = request.form['team_choice']
    opponent_choice = request.form['opponent_choice']
    
    # Convert team_choice and opponent_choice to team_ids
    selected_team = next(team for team in nba_teams if team['full_name'] == team_choice)
    selected_opponent = next(team for team in nba_teams if team['full_name'] == opponent_choice)
    
    team_id = selected_team['id']
    opponent_id = selected_opponent['id']
    
    # Retrieve game data for the selected teams
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, vs_team_id_nullable=opponent_id)
    gamefinder.get_json()
    games = gamefinder.get_data_frames()[0]

    # Separate games into home and away matchups
    games_home = games[games['MATCHUP'] == f"{selected_team['abbreviation']} vs. {selected_opponent['abbreviation']}"]
    games_away = games[games['MATCHUP'] == f"{selected_team['abbreviation']} @ {selected_opponent['abbreviation']}"]

    # Calculate the average plus-minus for away games
    average_plus_minus_away = games_away['PLUS_MINUS'].mean()
    
    return render_template(
        'results.html',
        selected_team=selected_team['full_name'],
        selected_opponent=selected_opponent['full_name'],
        average_plus_minus_away=average_plus_minus_away,
        games_home=games_home.to_html(),
        games_away=games_away.to_html()
    )

if __name__ == '__main__':
    app.run(debug=True)
