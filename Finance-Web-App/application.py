import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query the db for user
    users = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])

    # Find the stocks of this user
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                        user_id=session["user_id"])
    quotes = {}

    # Iterate over stocks
    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])

    # Remember the cash balance
    cash_balance = users[0]["cash"]
    total = cash_balance

    # Send user to the index page
    return render_template("index.html", quotes=quotes, stocks=stocks, total=total, cash_balance=cash_balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST
    if request.method == "POST":

        # Search for stock
        quote = lookup(request.form.get("symbol"))

        # Check if symbol is valid
        if quote == None:
            return apology("Invalid symbol", 400)

        # Check if number of shares is positive
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Check if shares is not 0
        if shares <= 0:
            return apology("Can't buy less than 1 share", 400)

        # Query db for this user
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # User cash balance
        cash_balance = rows[0]["cash"]
        price_per_share = quote["price"]
        total_price = price_per_share * shares

        # See if user has enough money
        if total_price > cash_balance:
            return apology("insufficient funds", 400)

        # Update database with the transaction
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=price_per_share)

        # Confirmation
        flash("Stock purchased!")

        # Redirect the user to homepage
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # Receive username from form
    username = request.args.get("username")

    # Query db for username
    taken_usernames = db.execute("SELECT username FROM users WHERE username = :username", username=username)

    # Check if username and db query match
    if taken_usernames and username:
        return jsonify(False)
    elif not taken_usernames and username:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query db for variables
    transactions = db.execute("SELECT * FROM purchases WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User wants to check a price
    if request.method == "POST":

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Check the stock
        quote = lookup(request.form.get("symbol"))

        # Return error if symbol can't be found
        if quote == None:
            return apology("stock symbol not found", 400)

        # Show user notification that was quoted
        flash("Quoted!")

        # Return values
        return render_template("quoted.html", quote=quote)

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must be the same", 400)

        # Hash password
        hash_password = generate_password_hash(request.form.get("password"))

        # Append user to db
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hash_password)

        # If username exists, return error
        if not result:
            return apology("username already exists", 400)

        # Confirmation message
        flash("Registered!")

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached URL through POST
    if request.method == "POST":

        # Lookup the stock
        quote = lookup(request.form.get("symbol"))

        # Check if symbol is valid
        if quote == None:
            return apology("invalid symbol", 404)

        # Check if number of shares is positive
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must be positive", 400)

        # Check if shares is bigger than 0
        if shares <= 0:
            return apology("Can't sell less than 1 share", 400)

        # Query db for shares of this user
        stock = db.execute("SELECT SUM(shares) as total_shares FROM purchases WHERE user_id = :user_id AND symbol = :symbol",
                           user_id=session["user_id"], symbol=request.form.get("symbol"))

        # Check if user has enough shares
        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("Can't sell less than 1 share or shares you don't own!", 400)

        # Query db for user's cash
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # User cash balance
        cash_balance = rows[0]["cash"]
        price_per_share = quote["price"]
        total_price = price_per_share * shares

        # Update database with the transaction
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])

        db.execute("INSERT INTO purchases (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=price_per_share)

        # Confirmation of sell
        flash("Shares sold!")

        # Redirect user to index
        return redirect("/")

    # User reached route via GET
    else:
        stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                            user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
