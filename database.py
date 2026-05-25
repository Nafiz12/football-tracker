import sqlite3
from datetime import datetime

DB = 'football.db'

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS teams (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL UNIQUE,
            city    TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS players (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            team_id  INTEGER NOT NULL REFERENCES teams(id),
            position TEXT DEFAULT 'FW'
        );
        CREATE TABLE IF NOT EXISTS matches (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER NOT NULL REFERENCES teams(id),
            away_team_id INTEGER NOT NULL REFERENCES teams(id),
            home_goals   INTEGER NOT NULL DEFAULT 0,
            away_goals   INTEGER NOT NULL DEFAULT 0,
            match_date   TEXT NOT NULL,
            round        TEXT NOT NULL,
            created_at   TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS goals (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id   INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
            player_id  INTEGER NOT NULL REFERENCES players(id),
            goals      INTEGER NOT NULL DEFAULT 1
        );
    ''')

    count = conn.execute('SELECT COUNT(*) FROM teams').fetchone()[0]
    if count == 0:
        # Real EPL 2025/26 teams
        teams = [
            ('Arsenal',                  'London'),
            ('Manchester City',          'Manchester'),
            ('Manchester United',        'Manchester'),
            ('Aston Villa',              'Birmingham'),
            ('Liverpool',                'Liverpool'),
            ('AFC Bournemouth',          'Bournemouth'),
            ('Sunderland',               'Sunderland'),
            ('Brighton & Hove Albion',   'Brighton'),
            ('Brentford',                'London'),
            ('Chelsea',                  'London'),
            ('Fulham',                   'London'),
            ('Newcastle United',         'Newcastle'),
            ('Everton',                  'Liverpool'),
            ('Leeds United',             'Leeds'),
            ('Crystal Palace',           'London'),
            ('Nottingham Forest',        'Nottingham'),
            ('Tottenham Hotspur',        'London'),
            ('West Ham United',          'London'),
            ('Burnley',                  'Burnley'),
            ('Wolverhampton Wanderers',  'Wolverhampton'),
        ]
        for name, city in teams:
            conn.execute('INSERT INTO teams (name, city) VALUES (?,?)', (name, city))

        # Key players per team
        players = [
            # Arsenal (id=1)
            ('Saka',        1,'FW'),('Odegaard',    1,'MF'),('Havertz',     1,'FW'),
            ('White',       1,'DF'),('Raya',         1,'GK'),
            # Man City (id=2)
            ('Haaland',     2,'FW'),('De Bruyne',    2,'MF'),('Foden',       2,'MF'),
            ('Dias',        2,'DF'),('Ederson',      2,'GK'),
            # Man United (id=3)
            ('Rashford',    3,'FW'),('Bruno Fernandes',3,'MF'),('Hojlund',   3,'FW'),
            ('Maguire',     3,'DF'),('Onana',        3,'GK'),
            # Aston Villa (id=4)
            ('Watkins',     4,'FW'),('McGinn',       4,'MF'),('Bailey',      4,'FW'),
            ('Konsa',       4,'DF'),('Martinez',     4,'GK'),
            # Liverpool (id=5)
            ('Salah',       5,'FW'),('Nunez',        5,'FW'),('Mac Allister',5,'MF'),
            ('Van Dijk',    5,'DF'),('Alisson',      5,'GK'),
            # Bournemouth (id=6)
            ('Solanke',     6,'FW'),('Christie',     6,'MF'),('Kluivert',   6,'FW'),
            # Sunderland (id=7)
            ('Stewart',     7,'FW'),('Neil',         7,'MF'),
            # Brighton (id=8)
            ('Mitoma',      8,'FW'),('Gross',        8,'MF'),('Welbeck',    8,'FW'),
            # Brentford (id=9)
            ('Toney',       9,'FW'),('Mbeumo',       9,'FW'),('Jensen',     9,'MF'),
            # Chelsea (id=10)
            ('Palmer',     10,'MF'),('Jackson',     10,'FW'),('Gallagher',  10,'MF'),
            # Fulham (id=11)
            ('Jimenez',    11,'FW'),('Andreas',     11,'MF'),
            # Newcastle (id=12)
            ('Isak',       12,'FW'),('Gordon',      12,'FW'),('Bruno G',    12,'MF'),
            # Everton (id=13)
            ('Calvert-Lewin',13,'FW'),('Doucoure',  13,'MF'),
            # Leeds (id=14)
            ('Bamford',    14,'FW'),('Gnonto',      14,'FW'),
            # Crystal Palace (id=15)
            ('Olise',      15,'FW'),('Eze',         15,'MF'),
            # Nottingham Forest (id=16)
            ('Awoniyi',    16,'FW'),('Hudson-Odoi', 16,'FW'),
            # Tottenham (id=17)
            ('Son',        17,'FW'),('Kane',        17,'FW'),('Maddison',   17,'MF'),
            # West Ham (id=18)
            ('Antonio',    18,'FW'),('Ward-Prowse', 18,'MF'),
            # Burnley (id=19)
            ('Rodriguez',  19,'FW'),('Benson',      19,'MF'),
            # Wolves (id=20)
            ('Hwang',      20,'FW'),('Neves',       20,'MF'),
        ]
        for name, tid, pos in players:
            conn.execute('INSERT INTO players (name, team_id, position) VALUES (?,?,?)', (name, tid, pos))

        # Today's real final day results (May 24, 2026)
        final_day = [
            (8,  3,  0, 3, '2026-05-24', 'Matchday 38'),  # Brighton 0-3 Man Utd
            (19, 20, 1, 1, '2026-05-24', 'Matchday 38'),  # Burnley 1-1 Wolves
            (15, 1,  1, 2, '2026-05-24', 'Matchday 38'),  # Crystal Palace 1-2 Arsenal
            (11, 12, 2, 0, '2026-05-24', 'Matchday 38'),  # Fulham 2-0 Newcastle
            (5,  9,  1, 1, '2026-05-24', 'Matchday 38'),  # Liverpool 1-1 Brentford
            (2,  4,  1, 2, '2026-05-24', 'Matchday 38'),  # Man City 1-2 Aston Villa
            (16, 6,  1, 1, '2026-05-24', 'Matchday 38'),  # Nottm Forest 1-1 Bournemouth
            (7,  10, 2, 1, '2026-05-24', 'Matchday 38'),  # Sunderland 2-1 Chelsea
            (17, 13, 1, 0, '2026-05-24', 'Matchday 38'),  # Tottenham 1-0 Everton
            (18, 14, 3, 0, '2026-05-24', 'Matchday 38'),  # West Ham 3-0 Leeds
        ]
        # Earlier matchdays sample
        earlier = [
            (1,  2,  2, 1, '2026-05-17', 'Matchday 37'),  # Arsenal 2-1 Man City
            (5,  1,  0, 1, '2026-05-10', 'Matchday 36'),  # Liverpool 0-1 Arsenal
            (2,  5,  3, 1, '2026-05-03', 'Matchday 35'),  # Man City 3-1 Liverpool
            (1,  3,  3, 0, '2026-04-26', 'Matchday 34'),  # Arsenal 3-0 Man Utd
            (10, 1,  1, 2, '2026-04-19', 'Matchday 33'),  # Chelsea 1-2 Arsenal
            (2,  3,  2, 0, '2026-04-12', 'Matchday 32'),  # Man City 2-0 Man Utd
        ]

        all_matches = final_day + earlier
        match_ids = []
        for hid, aid, hg, ag, date, rnd in all_matches:
            cur = conn.execute(
                'INSERT INTO matches (home_team_id,away_team_id,home_goals,away_goals,match_date,round,created_at) VALUES (?,?,?,?,?,?,?)',
                (hid, aid, hg, ag, date, rnd, datetime.now().strftime('%Y-%m-%d %H:%M'))
            )
            match_ids.append(cur.lastrowid)

        # Seed some goal scorers for top matches
        goal_seeds = [
            # Crystal Palace 1-2 Arsenal: Saka x2, Olise
            (match_ids[2], 1, 2), (match_ids[2], 15*5-4, 1),
            # Man Utd 3-0 Brighton: Rashford, Hojlund x2
            (match_ids[0], 11, 1), (match_ids[0], 13, 2),
            # Arsenal 2-1 Man City (MD37): Saka, Havertz, Haaland
            (match_ids[10], 1, 1), (match_ids[10], 3, 1), (match_ids[10], 6, 1),
            # Man City 3-1 Liverpool: Haaland x2, De Bruyne, Salah
            (match_ids[12], 6, 2), (match_ids[12], 7, 1), (match_ids[12], 21, 1),
            # Arsenal 3-0 Man Utd: Saka, Havertz x2
            (match_ids[13], 1, 1), (match_ids[13], 3, 2),
        ]
        for mid, pid, g in goal_seeds:
            try:
                conn.execute('INSERT INTO goals (match_id, player_id, goals) VALUES (?,?,?)', (mid, pid, g))
            except:
                pass

    conn.commit()
    conn.close()

def row_to_dict(row):
    return dict(row)

def get_teams():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM teams ORDER BY name').fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

def add_team(name, city=''):
    conn = get_conn()
    cur = conn.execute('INSERT INTO teams (name, city) VALUES (?,?)', (name, city))
    conn.commit()
    row = conn.execute('SELECT * FROM teams WHERE id=?', (cur.lastrowid,)).fetchone()
    conn.close()
    return row_to_dict(row)

def get_players(team_id=None):
    conn = get_conn()
    if team_id:
        rows = conn.execute(
            'SELECT p.*, t.name as team_name FROM players p JOIN teams t ON p.team_id=t.id WHERE p.team_id=? ORDER BY p.name',
            (team_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            'SELECT p.*, t.name as team_name FROM players p JOIN teams t ON p.team_id=t.id ORDER BY p.name'
        ).fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

def add_player(name, team_id, position='FW'):
    conn = get_conn()
    cur = conn.execute('INSERT INTO players (name, team_id, position) VALUES (?,?,?)', (name, team_id, position))
    conn.commit()
    row = conn.execute(
        'SELECT p.*, t.name as team_name FROM players p JOIN teams t ON p.team_id=t.id WHERE p.id=?',
        (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return row_to_dict(row)

def get_matches(team_id=None):
    conn = get_conn()
    sql = '''
        SELECT m.*, ht.name AS home_team, at.name AS away_team
        FROM matches m
        JOIN teams ht ON m.home_team_id = ht.id
        JOIN teams at ON m.away_team_id = at.id
        {where}
        ORDER BY m.match_date DESC, m.id DESC
    '''
    if team_id:
        rows = conn.execute(sql.format(where='WHERE m.home_team_id=? OR m.away_team_id=?'), (team_id, team_id)).fetchall()
    else:
        rows = conn.execute(sql.format(where='')).fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

def add_match(home_id, away_id, home_goals, away_goals, match_date, round_name, scorers):
    conn = get_conn()
    cur = conn.execute(
        'INSERT INTO matches (home_team_id,away_team_id,home_goals,away_goals,match_date,round,created_at) VALUES (?,?,?,?,?,?,?)',
        (home_id, away_id, home_goals, away_goals, match_date, round_name, datetime.now().strftime('%Y-%m-%d %H:%M'))
    )
    mid = cur.lastrowid
    for s in scorers:
        if s.get('player_id') and s.get('goals', 0) > 0:
            conn.execute('INSERT INTO goals (match_id,player_id,goals) VALUES (?,?,?)', (mid, s['player_id'], s['goals']))
    conn.commit()
    row = conn.execute(
        'SELECT m.*, ht.name AS home_team, at.name AS away_team FROM matches m JOIN teams ht ON m.home_team_id=ht.id JOIN teams at ON m.away_team_id=at.id WHERE m.id=?',
        (mid,)
    ).fetchone()
    conn.close()
    return row_to_dict(row)

def delete_match(match_id):
    conn = get_conn()
    conn.execute('DELETE FROM matches WHERE id=?', (match_id,))
    conn.commit()
    conn.close()

def get_league_table():
    conn = get_conn()
    rows = conn.execute('''
        WITH all_games AS (
            SELECT home_team_id AS team_id, home_goals AS gf, away_goals AS ga FROM matches
            UNION ALL
            SELECT away_team_id, away_goals, home_goals FROM matches
        )
        SELECT t.name, t.city,
            COUNT(*)                                                          AS played,
            SUM(CASE WHEN gf > ga THEN 1 ELSE 0 END)                        AS won,
            SUM(CASE WHEN gf = ga THEN 1 ELSE 0 END)                        AS drawn,
            SUM(CASE WHEN gf < ga THEN 1 ELSE 0 END)                        AS lost,
            SUM(gf)                                                           AS gf,
            SUM(ga)                                                           AS ga,
            SUM(gf) - SUM(ga)                                                AS gd,
            SUM(CASE WHEN gf > ga THEN 3 WHEN gf = ga THEN 1 ELSE 0 END)   AS points
        FROM all_games ag JOIN teams t ON ag.team_id = t.id
        GROUP BY t.id
        ORDER BY points DESC, gd DESC, gf DESC
    ''').fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

def get_top_scorers():
    conn = get_conn()
    rows = conn.execute('''
        SELECT p.name AS player, t.name AS team, p.position, SUM(g.goals) AS goals
        FROM goals g
        JOIN players p ON g.player_id = p.id
        JOIN teams   t ON p.team_id   = t.id
        GROUP BY p.id ORDER BY goals DESC LIMIT 10
    ''').fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]
