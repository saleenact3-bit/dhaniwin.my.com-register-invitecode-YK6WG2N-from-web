from flask import Flask, render_template_string, request, redirect, flash, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "demo-secret-key-change-this"

DATABASE = "users.db"


# =========================================================
# ADMIN LOGIN DETAILS
# =========================================================

ADMIN_ID = "hadi"
ADMIN_PASSWORD = "hadi1010"


# =========================
# DATABASE
# =========================

def setup_database():

    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


setup_database()


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


/* =========================================================
   HEADER
   ========================================================= */

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


/* =========================================================
   REGISTER FORM
   ========================================================= */

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

    background:
        rgba(255,255,255,.08);
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


/* =========================================================
   PASSWORD EYE
   ========================================================= */

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


/* =========================================================
   REGISTER BUTTON
   ========================================================= */

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


/* =========================================================
USER LOGIN LINK
   ========================================================= */

.login-link {

    display: block;

    margin-top: 20px;

    text-align: center;

    color: #d7c5e5;

    text-decoration: none;

    font-size: 16px;
}


.login-link:hover {

    color: #ffd044;
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


<!-- PHONE -->

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


<!-- PASSWORD -->

<div class="input-box">

    <div class="icon">
        🔒
    </div>

    <input
        type="password"
        id="password"
        name="password"
        placeholder="Password: 8-15 letters and numbers"
        minlength="8"
        maxlength="15"
        required>

    <div
        class="eye"
        onclick="showPassword('password')">

        <div class="eye-shape"></div>

    </div>

</div>


<!-- CONFIRM PASSWORD -->

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
# USER LOGIN PAGE
# =========================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no">

<title>Login</title>

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

    cursor: pointer;
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

    margin: 25px auto;
}


.title {

    margin-bottom: 20px;

    text-align: center;

    font-size: 25px;

    color: #ffd044;
}


.message {

    padding: 10px;

    margin-bottom: 12px;

    border-radius: 10px;

    text-align: center;

    color: #ffd75a;

    background:
        rgba(255,255,255,.08);
}


.input-box {

    height: 58px;

    margin-bottom: 14px;

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

    font-size: 19px;

    text-align: center;
}


input {

    width: 100%;

    height: 100%;

    border: none;

    outline: none;

    background: transparent;

    color: white;

    font-size: 16px;
}


input::placeholder {

    color: #9d88b7;
}


.login-button {

    width: 100%;

    height: 58px;

    margin-top: 8px;

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


.register-link {

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

    <div
        class="back"
        onclick="history.back()">

        ‹

    </div>


    <div class="logo">

        <h1>Dhani</h1>

        <h2>Win</h2>

    </div>

</div>


<div class="container">


<div class="title">
    Login
</div>


{% with messages = get_flashed_messages() %}

    {% for message in messages %}

        <div class="message">
            {{ message }}
        </div>

    {% endfor %}

{% endwith %}


<form
    method="POST"
    action="/login">


<div class="input-box">

    <div class="icon">
        📱
    </div>

    <input
        type="tel"
        name="phone"
        placeholder="Phone Number"
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
        name="password"
        placeholder="Password"
        required>

</div>


<button
    type="submit"
    class="login-button">

    Login

</button>


</form>


<a
    href="/"
    class="register-link">

    Don't have an account? Register

</a>


</div>


</body>

</html>
"""


# =========================================================
# ADMIN LOGIN PAGE
# =========================================================

ADMIN_LOGIN_PAGE = """
<!DOCTYPE html>
<html>

<head>

    <title>Admin Login</title>

    <style>

        body {
            font-family: Arial;
            background: #eeeeee;
            padding: 40px;
        }

        .box {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
        }

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 12px;
            background: black;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        .error {
            color: red;
        }

    </style>

</head>


<body>

<div class="box">

    <h2>Admin Login</h2>

    <form method="POST">

        <input
            type="text"
            name="admin_id"
            placeholder="Admin ID"
            required
        >

        <input
            type="password"
            name="admin_password"
            placeholder="Admin Password"
            required
        >

        <button type="submit">
            Admin Login
        </button>

    </form>

    <p class="error">{{ message }}</p>

</div>

</body>

</html>
"""


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if session.get("admin_logged_in"):

        return redirect("/admin/users")

    message = ""

    if request.method == "POST":

        admin_id = request.form.get("admin_id", "")

        admin_password = request.form.get(
            "admin_password",
            ""
        )

        if (
            admin_id == ADMIN_ID
            and admin_password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect("/admin/users")

        else:

            message = "Invalid Admin ID or Password."

    return render_template_string(
        ADMIN_LOGIN_PAGE,
        message=message
    )

# =========================
# REGISTERED USERS PAGE
# =========================

@app.route("/admin/users")
def admin_users():

    if not session.get("admin_logged_in"):

        return redirect("/admin")

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    users = connection.execute(
        """
        SELECT id, username, phone, password
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()


    return render_template_string(
        """
<!DOCTYPE html>
<html>

<head>

    <title>Registered Users</title>

    <style>

        body {
            font-family: Arial;
            background: #eeeeee;
            padding: 30px;
        }

        h1 {
            text-align: center;
        }

        .user {
            background: white;
            padding: 20px;
            margin: 15px auto;
            max-width: 500px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .user p {
            margin: 10px 0;
        }

        .password {
            color: #d00000;
            font-weight: bold;
        }

        .logout {
            display: block;
            width: 150px;
            margin: 0 auto 20px;
            padding: 10px;
            text-align: center;
            background: black;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }

    </style>

</head>


<body>

<h1>Registered Users</h1>


<a class="logout" href="/admin/logout">
    Admin Logout
</a>


{% if users %}

    {% for user in users %}

        <div class="user">

            <p>
                <b>User ID:</b>
                {{ user["id"] }}
            </p>

            <p>
                <b>Username:</b>
                {{ user["username"] }}
            </p>

            <p>
                <b>Phone:</b>
                {{ user["phone"] }}
            </p>

            <p class="password">
                <b>Password:</b>
                {{ user["password"] }}
            </p>

        </div>

    {% endfor %}

{% else %}

    <p style="text-align:center;">
        No registered users yet.
    </p>

{% endif %}


</body>

</html>
        """,
        users=users
    )


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin")


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
