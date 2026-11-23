"""Math Study Coach - minimal Flask app for Render.com (baseline deploy)."""
import os
from flask import Flask, jsonify

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Math Study Coach</title>
  <style>
    body{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem;line-height:1.5}
    li{margin:.25rem 0}
  </style>
</head>
<body>
  <h1>Math Study Coach</h1>
  <p>Tutor de matemáticas: Honors Algebra 2, AP Precalculus, AP Calculus AB/BC y AP Statistics.</p>
  <h2>Modos</h2>
  <ol>
    <li>Learn a Topic</li><li>Vocabulary &amp; Meaning</li><li>Life &amp; Career Applications</li>
    <li>Personal Finance &amp; Business</li><li>Diagnose &amp; Practice</li><li>Mistake Detective</li>
    <li>Graphs &amp; Representations</li><li>Retrieval &amp; Exam Practice</li>
    <li>Study Planner</li><li>Explain &amp; Defend</li>
  </ol>
  <p>Estado del servicio: <a href="/health">/health</a></p>
</body>
</html>"""


@app.route("/")
def home():
    return PAGE


@app.route("/health")
def health():
    return jsonify(status="ok", app="math-study-coach")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
