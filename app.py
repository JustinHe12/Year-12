from flask import Flask, g, render_template
import sqlite3


DATABASE = 'database.db'


app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._databse = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv




@app.route('/')
def home():
    #homepage
    db = get_db()
    cursor = db.cursor()
    sql = """
        SELECT Bikes.BikeID, Makers.Name, Bikes.Model, Bikes.Image_URL
        FROM Bikes
        LEFT JOIN Makers ON Makers.MakerID = Bikes.MakerID;
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("home.html", results=results)
   
@app.route("/bike/<int:id>")
def bike(id):
    sql = """
    SELECT * FROM Bikes
    JOIN Makers ON Makers.MakerID=Bikes.MakerID
    WHERE Bikes.BikeID =?;
"""
    results = query_db(sql,(id,), True)
    return render_template("bike.html", bike=results)
#render_template("bike.html", bike=result)

   


if __name__ == "__main__":
    app.run(debug=True)
   
