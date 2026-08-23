from flask import Flask, render_template_string, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

DATABASE = "users.db"


# =========================================================
# ADMIN DETAILS
# =========================================================

ADMIN_ID = "hadi"
ADMIN_PASSWORD = "hadi1010"


# =========================================================
# DATABASE
# =========================================================

def init_db():

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================================
# REGISTER PAGE
# =========================================================

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no">

<title>Register</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    min-height: 100vh;
    font-family: Arial, sans-serif;
    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );
}

.top {
    height: 260px;

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            rgba(25,5,50,.35),
            rgba(25,5,50,.88)
        ),
        url("https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1200&auto=format&fit=crop");

    background-size: cover;
    background-position: center;
}

.back {
    position: absolute;
    top: 15px;
    left: 18px;
    font-size: 42px;
}

.language {
    position: absolute;
    top: 20px;
    right: 18px;
    font-size: 14px;
}

.logo {
    position: absolute;
    top: 90px;
    width: 100%;
    text-align: center;
}

.logo h1 {
    font-size: 43px;
    font-style: italic;
    color: #b65cff;
}

.logo h2 {
    font-size: 35px;
    color: #ff9d16;
}

.container {
    width: calc(100% - 32px);
    max-width: 430px;
    margin: 15px auto;
}

.message {
    padding: 10px;
    margin-bottom: 12px;
    border-radius: 10px;
    text-align: center;
    color: #ffd75a;
    background: rgba(255,255,255,.08);
}

.input-box {
    height: 58px;
    margin-bottom: 13px;

    display: flex;
    align-items: center;

    padding: 0 13px;

    border-radius: 14px;

    border: 1px solid
        rgba(190,145,230,.42);

    background: #2b1846;
}

.icon {
    width: 32px;
    min-width: 32px;
    text-align: center;
    font-size: 19px;
}

.country {
    margin-right: 8px;
    font-size: 18px;
    font-weight: bold;
}

input {
    width: 100%;
    height: 100%;
    min-width: 0;

    border: none;
    outline: none;

    background: transparent;

    color: white;

    font-size: 16px;
}

input::placeholder {
    color: #9d88b7;
}

.eye {
    width: 30px;
    min-width: 30px;
    height: 30px;

    display: flex;

    align-items: center;
    justify-content: center;

    cursor: pointer;
}

.eye-shape {
    width: 21px;
    height: 13px;

    border: 2px solid #bda5d6;

    border-radius: 80% 20%;

    transform: rotate(45deg);

    position: relative;
}

.eye-shape::after {
    content: "";

    width: 5px;
    height: 5px;

    position: absolute;

    top: 2px;
    left: 6px;

    border-radius: 50%;

    background: #bda5d6;
}

.register {
    width: 100%;
    height: 58px;

    margin-top: 20px;

    border: none;

    border-radius: 30px;

    background:
        linear-gradient(
            #ffe66b,
            #efa800
        );

    color: #28132f;

    font-size: 20px;

    cursor: pointer;
}

.login-link {
    display: block;

    margin-top: 20px;

    text-align: center;

    color: #d7c5e5;

    text-decoration: none;

    font-size: 16px;
}

</style>

</head>

<body>

<div class="top">

    <div class="back">
        ‹
    </div>

    <div class="language">
        🎧 &nbsp; 🇬🇧 EN
    </div>

    <div class="logo">
        <h1>Dhani</h1>
        <h2>Win</h2>
    </div>

</div>


<div class="container">

{% with messages = get_flashed_messages() %}

    {% for message in messages %}

        <div class="message">
            {{ message }}
        </div>

    {% endfor %}

{% endwith %}


<form method="POST" action="/register">


<div class="input-box">

    <div class="icon">
        📱
    </div>

    <div class="country">
        +91
    </div>

    <input
        type="tel"
        name="phone"
        placeholder="Enter your phone number"
        maxlength="10"
        inputmode="numeric"
        required>

</div>


<div class="input-box">

    <div class="icon">
        🔒
    </div>

    <input
        type="password"
        id="password"
        name="password"
        placeholder="Password: 8-15 characters"
        minlength="8"
        maxlength="15"
        required>

    <div
        class="eye"
        onclick="showPassword('password')">

        <div class="eye-shape"></div>

    </div>

</div>


<div class="input-box">

    <div class="icon">
        🔒
    </div>

    <input
        type="password"
        id="confirm"
        name="confirm_password"
        placeholder="Enter the password again"
        minlength="8"
        maxlength="15"
        required>

    <div
        class="eye"
        onclick="showPassword('confirm')">

        <div class="eye-shape"></div>

    </div>

</div>


<button
    type="submit"
    class="register">

    Register

</button>


</form>


<a
    href="/login"
    class="login-link">

    Already registered? Login

</a>


</div>


<script>

function showPassword(id) {

    const input =
        document.getElementById(id);

    if (input.type === "password") {

        input.type = "text";

    } else {

        input.type = "password";

    }

}

</script>

</body>

</html>
"""


# =========================================================
# LOGIN PAGE
# =========================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html>

<head>

<meta name="viewport"
content="width=device-width,
initial-scale=1.0">

<title>User Login</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    min-height: 100vh;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 20px;

    font-family: Arial;

    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );
}

.box {

    width: 100%;

    max-width: 390px;

    padding: 28px 20px;

    border-radius: 22px;

    background: #2b1746;

    border: 1px solid
        rgba(190,145,230,.35);
}

h1 {

    text-align: center;

    color: #ffd044;

    margin-bottom: 25px;
}

.message {

    margin-bottom: 15px;

    padding: 10px;

    border-radius: 8px;

    text-align: center;

    color: #ffd75a;

    background:
        rgba(255,255,255,.08);
}

input {

    width: 100%;

    height: 55px;

    margin-bottom: 14px;

    padding: 0 15px;

    border: 1px solid #65457f;

    border-radius: 12px;

    outline: none;

    background: #1d1030;

    color: white;

    font-size: 16px;
}

button {

    width: 100%;

    height: 55px;

    border: none;

    border-radius: 28px;

    background:
        linear-gradient(
            #ffe66b,
            #efa800
        );

    color: #28132f;

    font-size: 19px;

    cursor: pointer;
}

a {

    display: block;

    margin-top: 18px;

    text-align: center;

    color: #bda5d6;

    text-decoration: none;
}

</style>

</head>

<body>

<div class="box">

<h1>User Login</h1>


{% with messages = get_flashed_messages() %}

    {% for message in messages %}

        <div class="message">
            {{ message }}
        </div>

    {% endfor %}

{% endwith %}


<form method="POST" action="/login">

<input
    type="tel"
    name="phone"
    placeholder="Phone Number"
    maxlength="10"
    required>


<input
    type="password"
    name="password"
    placeholder="Password"
    required>


<button type="submit">
    Login
</button>

</form>


<a href="/">
    Don't have an account? Register
</a>

</div>

</body>

</html>
"""


# =========================================================
# ADMIN LOGIN PAGE
# =========================================================

ADMIN_LOGIN_HTML = """
<!DOCTYPE html>
<html>

<head>

<meta name="viewport"
content="width=device-width,
initial-scale=1.0">

<title>Admin Login</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    min-height: 100vh;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 20px;

    font-family: Arial;

    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );
}

.box {

    width: 100%;

    max-width: 390px;

    padding: 28px 20px;

    border-radius: 22px;

    background: #2b1746;

    border: 1px solid
        rgba(190,145,230,.35);
}

h1 {

    margin-bottom: 25px;

    text-align: center;

    color: #ffd044;

    font-size: 27px;
}

.message {

    margin-bottom: 15px;

    padding: 10px;

    border-radius: 8px;

    text-align: center;

    color: #ffd75a;

    background:
        rgba(255,255,255,.08);
}

input {

    width: 100%;

    height: 55px;

    margin-bottom: 14px;

    padding: 0 15px;

    border: 1px solid #65457f;

    border-radius: 12px;

    outline: none;

    background: #1d1030;

    color: white;

    font-size: 16px;
}

button {

    width: 100%;

    height: 55px;

    border: none;

    border-radius: 28px;

    background:
        linear-gradient(
            #ffe66b,
            #efa800
        );

    color: #28132f;

    font-size: 19px;

    cursor: pointer;
}

.back {

    display: block;

    margin-top: 18px;

    text-align: center;

    color: #bda5d6;

    text-decoration: none;
}

</style>

</head>

<body>

<div class="box">

<h1>Admin Login</h1>


{% with messages = get_flashed_messages() %}

    {% for message in messages %}

        <div class="message">
            {{ message }}
        </div>

    {% endfor %}

{% endwith %}


<form method="POST"
      action="/admin/login">


<input
    type="text"
    name="admin_id"
    placeholder="Admin ID"
    required>


<input
    type="password"
    name="admin_password"
    placeholder="Admin Password"
    required>


<button type="submit">
    Admin Login
</button>


</form>


<a href="/" class="back">
    ← Back
</a>


</div>

</body>

</html>
"""


# =========================================================
# ADMIN DASHBOARD
# =========================================================

ADMIN_HTML = """
<!DOCTYPE html>
<html>

<head>

<meta name="viewport"
content="width=device-width,
initial-scale=1.0">

<title>Admin Dashboard</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    min-height: 100vh;

    padding: 15px;

    font-family: Arial;

    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );
}

.container {

    width: 100%;

    max-width: 1100px;

    margin: auto;
}

.header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 20px;
}

h1 {

    color: #ffd044;

    font-size: 25px;
}

.logout {

    padding: 9px 15px;

    border: 1px solid #d1a43e;

    border-radius: 20px;

    color: #ffd044;

    text-decoration: none;

    font-size: 14px;
}

.count {

    margin-bottom: 12px;

    color: #c9b7d5;
}

.card {

    width: 100%;

    overflow-x: auto;

    padding: 10px;

    border-radius: 18px;

    background: #2b1746;

    border: 1px solid
        rgba(190,145,230,.35);
}

table {

    width: 100%;

    min-width: 750px;

    border-collapse: collapse;
}

th {

    padding: 13px;

    text-align: left;

    color: #ffd044;

    border-bottom:
        1px solid #604475;
}

td {

    padding: 13px;

    color: #e4d9ec;

    border-bottom:
        1px solid #49335b;

    vertical-align: top;
}

.hash {

    font-family: monospace;

    font-size: 12px;

    word-break: break-all;

    color: #bda5d6;
}

.empty {

    padding: 35px;

    text-align: center;

    color: #a995b7;
}

</style>

</head>

<body>

<div class="container">


<div class="header">

<h1>
    Admin Dashboard
</h1>


<a
    href="/admin/logout"
    class="logout">

    Logout

</a>

</div>


<div class="count">

Registered Users:
<strong>{{ users|length }}</strong>

</div>


<div class="card">

{% if users %}

<table>

<thead>

<tr>

<th>ID</th>

<th>Phone Number</th>

<th>Password Hash</th>

</tr>

</thead>


<tbody>

{% for user in users %}

<tr>

<td>
    {{ user[0] }}
</td>


<td>
    +91 {{ user[1] }}
</td>


<td class="hash">
    {{ user[2] }}
</td>


</tr>

{% endfor %}

</tbody>

</table>


{% else %}

<div class="empty">

No registered users yet.

</div>

{% endif %}

</div>

</div>

</body>

</html>
"""


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        REGISTER_HTML
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["POST"]
)
def register():

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    confirm = request.form.get(
        "confirm_password",
        ""
    )


    if not phone.isdigit() or len(phone) != 10:

        flash(
            "Please enter a valid 10-digit phone number."
        )

        return redirect("/")


    if len(password) < 8 or len(password) > 15:

        flash(
            "Password must be 8-15 characters."
        )

        return redirect("/")


    if password != confirm:

        flash(
            "Passwords do not match."
        )

        return redirect("/")


    # PASSWORD HASH

    hashed_password = generate_password_hash(
        password
    )


    try:

        conn = sqlite3.connect(
            DATABASE
        )

        conn.execute(
            """
            INSERT INTO users
            (phone, password)
            VALUES (?, ?)
            """,
            (
                phone,
                hashed_password
            )
        )

        conn.commit()

        conn.close()


    except sqlite3.IntegrityError:

        flash(
            "This phone number is already registered."
        )

        return redirect("https://dhaniwin4.com/")



# =========================================================
# USER LOGIN
# =========================================================

@app.route("/login")
def login_page():

    return render_template_string(
        LOGIN_HTML
    )


@app.route(
    "/login",
    methods=["POST"]
)
def login():

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )


    conn = sqlite3.connect(
        DATABASE
    )


    user = conn.execute(
        """
        SELECT id, phone, password
        FROM users
        WHERE phone = ?
        """,
        (phone,)
    ).fetchone()


    conn.close()


    if (
        user is None
        or not check_password_hash(
            user[2],
            password
        )
    ):

        flash(
            "Phone number or password is incorrect."
        )

        return redirect("/login")


    session["user_id"] = user[0]

    session["user_phone"] = user[1]


    flash(
        "Login successful."
    )

    return redirect("/login")


# =========================================================
# ADMIN LOGIN PAGE
# =========================================================

@app.route("/admin")
def admin():

    if session.get(
        "admin_logged_in"
    ):

        return redirect(
            "/admin/dashboard"
        )


    return render_template_string(
        ADMIN_LOGIN_HTML
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["POST"]
)
def admin_login():

    admin_id = request.form.get(
        "admin_id",
        ""
    ).strip()

    admin_password = request.form.get(
        "admin_password",
        ""
    )


    # EXACT ADMIN ID AND PASSWORD

    if (
        admin_id == ADMIN_ID
        and
        admin_password == ADMIN_PASSWORD
    ):

        session["admin_logged_in"] = True

        return redirect(
            "/admin/dashboard"
        )


    flash(
        "Invalid Admin ID or Password."
    )

    return redirect("/admin")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get(
        "admin_logged_in"
    ):

        return redirect("/admin")


    conn = sqlite3.connect(
        DATABASE
    )


    # GET USER ID + PHONE + HASHED PASSWORD

    users = conn.execute(
        """
        SELECT id, phone, password
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()


    conn.close()


    return render_template_string(
        ADMIN_HTML,
        users=users
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect("/admin")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )
