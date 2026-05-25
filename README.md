# ⚽ Football Tracker

A full-stack football match tracking web app built with **Python Flask** and **vanilla JavaScript**. Track match results, view live league standings, and follow top scorers — all with a clean REST API backend.

## 🚀 Features

- Log match results with home/away scores and goal scorers
- Auto-calculated league table (points, goal difference, ranking)
- Top scorers leaderboard with goals per player
- Filter matches by team
- Add custom teams and players
- Full REST API — every feature is API-driven

## 🛠 Tech Stack

| Layer    | Technology |
|----------|------------|
| Backend  | Python 3, Flask |
| Database | SQLite — real SQL with JOINs, CTEs, GROUP BY, CASE WHEN |
| Frontend | Vanilla HTML, CSS, JavaScript (zero frameworks) |
| API      | REST — GET, POST, DELETE |

## 📁 Project Structure

```
football-tracker/
├── app.py          # Flask routes & REST API
├── database.py     # SQLite schema, queries, seed data
├── requirements.txt
└── static/
    └── index.html  # Full frontend — HTML + CSS + JS in one file
```

## ⚡ Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/football-tracker.git
cd football-tracker

python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000**

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teams` | List all teams |
| POST | `/api/teams` | Add a team |
| GET | `/api/players` | List players (optional `?team_id=`) |
| POST | `/api/players` | Add a player |
| GET | `/api/matches` | List matches (optional `?team_id=`) |
| POST | `/api/matches` | Log a match result + scorers |
| DELETE | `/api/matches/<id>` | Remove a match |
| GET | `/api/table` | League standings (auto-calculated) |
| GET | `/api/scorers` | Top scorers leaderboard |

## 💡 Key SQL — League Table

The league table is computed entirely in SQL using a CTE and aggregation:

```sql
WITH all_games AS (
    SELECT home_team_id AS team_id, home_goals AS gf, away_goals AS ga FROM matches
    UNION ALL
    SELECT away_team_id, away_goals, home_goals FROM matches
)
SELECT t.name,
    COUNT(*)                                          AS played,
    SUM(CASE WHEN gf > ga THEN 3 WHEN gf = ga THEN 1 ELSE 0 END) AS points,
    SUM(gf) - SUM(ga)                                AS gd
FROM all_games ag JOIN teams t ON ag.team_id = t.id
GROUP BY t.id ORDER BY points DESC, gd DESC
```

---

Built by **Md Nafiz Al Ifat** — [LinkedIn](https://linkedin.com/in/YOUR_PROFILE) | [GitHub](https://github.com/YOUR_USERNAME)
