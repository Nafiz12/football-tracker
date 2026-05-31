from flask import Blueprint, jsonify, request, send_from_directory
from . import models

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return send_from_directory('../static', 'index.html')

@main.route('/api/teams', methods=['GET'])
def get_teams():
    return jsonify(models.get_teams())

@main.route('/api/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Team name required'}), 400
    return jsonify(models.add_team(data['name'], data.get('city', ''))), 201

@main.route('/api/players', methods=['GET'])
def get_players():
    return jsonify(models.get_players(request.args.get('team_id')))

@main.route('/api/players', methods=['POST'])
def create_player():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('team_id'):
        return jsonify({'error': 'Player name and team required'}), 400
    return jsonify(models.add_player(data['name'], data['team_id'], data.get('position', 'FW'))), 201

@main.route('/api/matches', methods=['GET'])
def get_matches():
    return jsonify(models.get_matches(request.args.get('team_id')))

@main.route('/api/matches', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ('home_team_id', 'away_team_id', 'home_goals', 'away_goals', 'match_date', 'round')
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    if data['home_team_id'] == data['away_team_id']:
        return jsonify({'error': 'Teams must be different'}), 400
    match = models.add_match(
        data['home_team_id'], data['away_team_id'],
        int(data['home_goals']), int(data['away_goals']),
        data['match_date'], data['round'],
        data.get('scorers', [])
    )
    return jsonify(match), 201

@main.route('/api/matches/<int:match_id>', methods=['DELETE'])
def remove_match(match_id):
    models.delete_match(match_id)
    return jsonify({'deleted': match_id})

@main.route('/api/table', methods=['GET'])
def get_table():
    return jsonify(models.get_league_table())

@main.route('/api/scorers', methods=['GET'])
def get_scorers():
    return jsonify(models.get_top_scorers())