import os
from flask import Flask, jsonify, request, send_from_directory
from database import (
    init_db, get_matches, add_match, delete_match,
    get_league_table, get_top_scorers, get_teams, add_team,
    get_players, add_player
)

app = Flask(__name__, static_folder='static')

# ── Frontend ──────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ── Teams ─────────────────────────────────────────────────────
@app.route('/api/teams', methods=['GET'])
def teams():
    return jsonify(get_teams())

@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Team name required'}), 400
    team = add_team(data['name'], data.get('city', ''))
    return jsonify(team), 201

# ── Players ───────────────────────────────────────────────────
@app.route('/api/players', methods=['GET'])
def players():
    team_id = request.args.get('team_id')
    return jsonify(get_players(team_id))

@app.route('/api/players', methods=['POST'])
def create_player():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('team_id'):
        return jsonify({'error': 'Player name and team required'}), 400
    player = add_player(data['name'], data['team_id'], data.get('position', 'FW'))
    return jsonify(player), 201

# ── Matches ───────────────────────────────────────────────────
@app.route('/api/matches', methods=['GET'])
def matches():
    team_id = request.args.get('team_id')
    return jsonify(get_matches(team_id))

@app.route('/api/matches', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ('home_team_id', 'away_team_id', 'home_goals', 'away_goals', 'match_date', 'round')
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    if data['home_team_id'] == data['away_team_id']:
        return jsonify({'error': 'Teams must be different'}), 400
    scorers = data.get('scorers', [])  # list of {player_id, goals}
    match = add_match(
        data['home_team_id'], data['away_team_id'],
        int(data['home_goals']), int(data['away_goals']),
        data['match_date'], data['round'], scorers
    )
    return jsonify(match), 201

@app.route('/api/matches/<int:match_id>', methods=['DELETE'])
def remove_match(match_id):
    delete_match(match_id)
    return jsonify({'deleted': match_id})

# ── Stats ─────────────────────────────────────────────────────
@app.route('/api/table', methods=['GET'])
def table():
    return jsonify(get_league_table())

@app.route('/api/scorers', methods=['GET'])
def scorers():
    return jsonify(get_top_scorers())

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
