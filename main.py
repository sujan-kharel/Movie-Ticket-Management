from flask import Flask, render_template, redirect, request
import mysql.connector

app = Flask(__name__)

## CONNECTION TO MYSQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'zany'
# app.config['MYSQL_DB'] = 'movie'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conn = mysql.connector.connect(user='root', password='zany',
                               host='localhost', database='ticket_management', auth_plugin='mysql_native_password')


# if conn:
#     print("Connection Successful")
# else:
#     print("connect failure")

# select_ticket = """SELECT*FROM movies"""
# cursor = conn.cursor()
# cursor.execute(select_ticket)
# result = cursor.fetchall()
# for r in result:
#     print(r)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/requestPage", methods=["POST"])
def getPage():
    if request.method == "POST":
        if request.form.get("main"):
            return redirect("/")
        if request.form.get("movies"):
            return redirect("/movies")
        elif request.form.get("tickets"):
            return redirect("/tickets")
        else:
            return render_template("index.html")


@app.route("/movies")
def showMovieList():
    select_ticket = """SELECT*FROM movies"""
    cursor = conn.cursor()
    cursor.execute(select_ticket)
    movies = cursor.fetchall()

    return render_template("movies.html", movies=movies)


@app.route("/tickets")
def showTable():
    select_ticket = """SELECT*FROM tickets"""
    cursor = conn.cursor()
    cursor.execute(select_ticket)
    tickets = cursor.fetchall()
    return render_template("tickets.html", tickets=tickets)


@app.route("/conform")
def showConform():
    return render_template("conform.html")


@app.route("/pick_movie", methods=['POST'])
def pickMovie():
    if request.method == "POST":
        try:
            movie_id = int(request.form.get("purchase"))
        except ValueError:
            return redirect("/movies")
        print("movie id ", movie_id)
        select_ticket = f"""SELECT * from movies INNER JOIN 
                            show_time on movies.movie_id = show_time.movie_id 
                            where movies.movie_id = {movie_id} """
        cursor = conn.cursor()
        cursor.execute(select_ticket)
        movies = cursor.fetchall()

        return render_template("conform.html", movies=movies)

    return redirect("/movies")


@app.route("/conformation", methods=["POST"])
def insertMovie():
    if request.method == "POST":
        try:

            movie_id = int(request.form.get("movie_id"))
            name = str(request.form.get("name"))
            email = str(request.form.get("email"))
            #  movie_name = str(request.form.get("movie_name"))
            # duration = str(request.form.get("duration"))
            seat_number = int(request.form.get("seat_number"))
            show_date = str(request.form.get("show_date"))
        except ValueError:
            return redirect("/movies")

        select_movie = f"""select movie_name, duration from movies where movie_id = {movie_id}"""
        cursor = conn.cursor()
        cursor.execute(select_movie)
        movie_description = cursor.fetchall()

        # insert_ticket = f"INSERT INTO tickets (ticket_number, movie_id, name, " \
        #                 f"email, movie_name, duration, seat_number, show_date) " \
        #                 f"VALUES(DEFAULT, {movie_id}, {name}, {email}, " \
        #                 f"{movie_name}, {duration}, {seat_number}, {show_date} )"

        cursor.execute(cursor.execute(f"""INSERT INTO tickets VALUES 
                        (NULL, "{movie_id}", "{name}", "{email}", "{movie_description[0][0]}",
                        "{movie_description[0][1]}", "{seat_number}", "{show_date}")"""))
        conn.commit()

        return redirect("/tickets")

    return redirect("/movies")


@app.route("/display", methods=["POST"])
def refund():
    if request.method == "POST":
        if request.form.get("refund"):
            try:
                ticket_number = int(request.form.get("refund"))
            except ValueError:
                return redirect("/tickets")

            delete_ticket = f"""DELETE FROM tickets WHERE ticket_number = {ticket_number}"""
            cursor = conn.cursor()
            cursor.execute(delete_ticket)
            conn.commit()
            return redirect("/tickets")
        if request.form.get("update"):
            try:
                ticket_number = int(request.form.get("update"))
            except ValueError:
                return redirect("/tickets")

            select_ticket = f"""SELECT*FROM tickets WHERE ticket_number = {ticket_number}"""
            cursor = conn.cursor()
            cursor.execute(select_ticket)
            ticket = cursor.fetchall()

            movie_id = ticket[0][1]

            select_ticket = f"""SELECT * from movies INNER JOIN 
                                        show_time on movies.movie_id = show_time.movie_id 
                                        where movies.movie_id = {movie_id} """

            cursor = conn.cursor()
            cursor.execute(select_ticket)
            date = cursor.fetchall()
            return render_template("update.html", ticket=ticket, date=date)

    return redirect("/tickets")


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        try:
            ticket_number = int(request.form.get("ticket_number"))
            date = str(request.form.get("show_date"))
        except ValueError:
            return redirect("/tickets")

        print(ticket_number, date)

        update_ticket = f"""UPDATE  tickets set show_date = "{date}" where ticket_number = {ticket_number}"""
        cursor = conn.cursor()
        cursor.execute(update_ticket)
        conn.commit()

        redirect("/tickets")
    return redirect("/tickets")


if __name__ == "__main__":
    app.run(debug=True)
