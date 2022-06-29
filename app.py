from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

con = sqlite3.connect("rendezvous.db")
print("Database opened successfully")
# con.execute("create table Appt (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, surname TEXT UNIQUE NOT NULL, email TEXT NOT NULL)")
# print("Table created successfully")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/About")
def About():
    return render_template("About.html")


@app.route("/Contact")
def Contact():
    return render_template("contact.html")


@app.route("/Appointement")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            surname = request.form["surname"]
            email = request.form["email"]
            cell = request.form["cell"]
            appon = request.form["appon"]
            messg = request.form["messg"]
            with sqlite3.connect("rendezvous.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT into Appt (name, surname, email,cell, appon, messg) values (?,?,?,?,?)", (name, surname, email, cell, appon, messg))
                con.commit()
                msg = "rendezvous successfully Added"
        except:
            con.rollback()
            msg = "We can not add the rendezvous to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("rendezvous.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Appt")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
