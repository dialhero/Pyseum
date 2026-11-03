import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, render_template, request


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
DB_PATH = Path(__file__).resolve().parent.parent / "themetsql.db"

app = Flask(__name__, template_folder=str(FRONTEND_DIR), static_folder=str(FRONTEND_DIR))

# Map each query identifier to a dictionary containing its label and SQL.
QUERIES = {}


@app.get("/")
def home():
    selected_query = request.args.get("query")
    columns = []
    rows = []
    error = None

    if selected_query:
        query = QUERIES.get(selected_query)
        if query is None:
            error = "Unrecognised query."
            selected_query = None
        else:
            try:
                with closing(sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)) as connection:
                    cursor = connection.execute(query["sql"])
                    columns = [column[0] for column in cursor.description or ()]
                    rows = cursor.fetchall()
                if not rows:
                    error = "No rows match query parameters."
            except sqlite3.Error:
                error = "The query could not be completed."

    queries = [{"id": identifier, "label": query["label"]} for identifier, query in QUERIES.items()]
    return render_template(
        "home.html",
        queries=queries,
        selected_query=selected_query,
        columns=columns,
        rows=rows,
        error=error,
    )


if __name__ == "__main__":
    app.run()
