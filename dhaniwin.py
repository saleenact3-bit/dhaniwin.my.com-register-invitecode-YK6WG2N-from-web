from flask import Flask, render_template_string, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DATABASE = "users.db"


# ---------------- DATABASE ----------------

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


def get_db():
    return sqlite3.connect(DATABASE)


# ---------------- VERIFICATION CODE ----------------

def generate_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(7))


verification_code = generate_code()


# ---------------- HTML ----------------

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Dhani Win - Register Demo</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    min-height: 100vh;
    font-family: Arial, sans-serif;
    background:
        radial-gradient(circle at top, #38205d, #160b2d 65%);
    color: white;
}

/* TOP */

.top {
    height: 330px;
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            rgba(25, 8, 55, 0.35),
            rgba(25, 8, 55, 0.85)
        ),
        url("https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1200&auto=format&fit=crop");

    background-size: cover;
    background-position: center;
}

.back {
    position: absolute;
    top: 30px;
    left: 25px;
    font-size: 50px;
    font-weight: 200;
}

.language {
    position: absolute;
    top: 30px;
    right: 25px;
    font-size: 22px;
}

.logo {
    position: absolute;
    width: 100%;
    text-align: center;
    top: 135px;
}

.logo h1 {
    font-size: 58px;
    font-style: italic;
    color: #b55cff;
    font-weight: bold;
}

.logo h2 {
    font-size: 48px;
    color: #ff9d16;
    margin-top: -10px;
}


/* FORM AREA */

.container {
    width: 92%;
    max-width: 780px;
    margin: -5px auto 40px;
    position: relative;
}

.input-box {
    height: 75px;
    margin: 18px 0;

    display: flex;
    align-items: center;

    background: rgba(43, 24, 70, 0.92);

    border: 1px solid rgba(190, 145, 230, 0.4);

    border-radius: 18px;

    padding: 0 20px;

    box-shadow:
        inset 0 0 15px rgba(0,0,0,0.15);
}

.icon {
    width: 55px;
    font-size: 25px;
    color: #c9a8ff;
    text-align: center;
}

.country {
    font-size: 25px;
    font-weight: bold;
    margin-right: 15px;
}

input {
    width: 100%;
    height: 100%;

    background: transparent;

    border: none;
    outline: none;

    color: white;

    font-size: 22px;
}

input::placeholder {
    color: #a18bbd;
}

.eye {
    cursor: pointer;
    font-size: 23px;
    color: #bca3d8;
}


/* CAPTCHA */

.code-box {
    color: white;
    font-size: 25px;
    font-weight: bold;
    letter-spacing: 3px;
}

.refresh {
    margin-left: auto;
    color: #ffbf25;
    cursor: pointer;
    font-size: 25px;
}


/* BUTTON */

.register {
    width: 90%;
    margin: 35px auto 25px;

    display: block;

    height: 75px;

    border: none;
    border-radius: 45px;

    background:
        linear-gradient(
            #ffe56c,
            #f2a900
        );

    color: #24112e;

    font-size: 28px;

    cursor: pointer;

    box-shadow:
        0 8px 18px rgba(0,0,0,0.3);
}

.register:active {
    transform: scale(0.98);
}


/* LOGIN */

.login {
    width: 90%;
    height: 75px;

    margin: auto;

    display: flex;

    align-items: center;
    justify-content: center;

    border: 2px solid #d6a735;

    border-radius: 45px;

    color: #e9b83f;

    font-size: 25px;

    text-decoration: none;
}


/* MESSAGE */

.message {
    text-align: center;
    margin: 15px;
    padding: 12px;

    border-radius: 10px;

    background: rgba(255, 255, 255, 0.08);

    color: #ffd76a;

    font-size: 18px;
}


/* DESKTOP */

@media (min-width: 800px) {

    .top {
        height: 420px;
    }

    .container {
        margin-top: -10px;
    }

}

</style>

</head>

<body>


<!-- TOP -->

<div class="top">

    <div class="back">‹</div>

    <div class="language">
        🎧 &nbsp; 🇬🇧 EN
    </div>

    <div class="logo">
        <h1>Dhani</h1>
        <h2>Win</h2>
    </div>

</div>


<!-- FORM -->

<div class="container">

    {% with messages = get_flashed_messages() %}

        {% if messages %}

            {% for message in messages %}

                <div class="message">
                    {{ message }}
                </div>

            {% endfor %}

        {% endif %}

    {% endwith %}


<form method="POST"
      action="{{ url_for('register') }}">


    <!-- PHONE -->

    <div class="input-box">

        <div class="icon">📱</div>

        <div class="country">
            +91
        </div>

        <input
            type="tel"
            name="phone"
            placeholder="Enter your phone number"
            maxlength="10"
            required
        >

    </div>


    <!-- PASSWORD -->

    <div class="input-box">

        <div class="icon">🔒</div>

        <input
            type="password"
            id="password"
            name="password"
            placeholder="Password: 8-15 letters and numbers"
            minlength="8"
            maxlength="15"
            required
        >

        <div
            class="eye"
            onclick="showPassword('password')">
            👁
        </div>

    </div>


    <!-- CONFIRM PASSWORD -->

    <div class="input-box">

        <div class="icon">🔒</div>

        <input
            type="password"
            id="confirm_password"
            name="confirm_password"
            placeholder="Enter the password again"
            minlength="8"
            maxlength="15"
            required
        >

        <div
            class="eye"
            onclick="showPassword('confirm_password')">
            👁
        </div>

    </div>


    <!-- VERIFICATION CODE DISPLAY -->

    <div class="input-box">

        <div class="icon">🛡️</div>

        <div class="code-box">
            {{ verification_code }}
        </div>

        <div
            class="refresh"
            onclick="location.reload()">
            ↻
        </div>

    </div>


    <!-- VERIFICATION INPUT -->

    <div class="input-box">

        <div class="icon">🛡️</div>

        <input
            type="text"
            name="verification"
            placeholder="Please enter the verification code"
            maxlength="7"
            required
        >

        <button
            type="button"
            onclick="alert('Demo verification code: {{ verification_code }}')"
            style="
                border:none;
                border-radius:25px;
                padding:12px 25px;
                background:#f5b719;
                color:#27132f;
                font-size:18px;
                cursor:pointer;
            ">
            Send
        </button>

    </div>


    <!-- REGISTER -->

    <button
        class="register"
        type="submit">

        Register

    </button>


</form>


<!-- LOGIN -->

<a
    href="#"
    class="login">

    Password Login

</a>


</div>


<script>

function showPassword(id) {

    const input = document.getElementById(id);

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


# ---------------- REGISTER ----------------

@app.route("/", methods=["GET"])
def home():

    global verification_code

    # പുതിയ code
    verification_code = generate_code()

    return render_template_string(
        HTML,
        verification_code=verification_code
    )


@app.route("/register", methods=["POST"])
def register():

    global verification_code

    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    user_code = request.form.get("verification", "").strip().upper()


    # PHONE VALIDATION

    if not phone.isdigit() or len(phone) != 10:

        flash("Please enter a valid 10-digit phone number.")

        return redirect(url_for("home"))


    # PASSWORD VALIDATION

    if len(password) < 8 or len(password) > 15:

        flash("Password must contain 8-15 characters.")

        return redirect(url_for("home"))


    # PASSWORD MATCH

    if password != confirm_password:

        flash("Passwords do not match.")

        return redirect(url_for("home"))


    # VERIFICATION

    if user_code != verification_code:

        flash("Incorrect verification code.")

        return redirect(url_for("home"))


    # HASH PASSWORD

    hashed_password = generate_password_hash(password)


    # SAVE USER

    try:

        conn = get_db()

        conn.execute(
            """
            INSERT INTO users (phone, password)
            VALUES (?, ?)
            """,
            (phone, hashed_password)
        )

        conn.commit()
        conn.close()

    except sqlite3.IntegrityError:

        flash("This phone number is already registered.")

        return redirect(url_for("home"))


    # SUCCESS

    flash("Registration successful!")

    # New verification code
    verification_code = generate_code()

    return redirect(url_for("success"))


# ---------------- SUCCESS PAGE ----------------

@app.route("/success")
def success():

    return """
    <!DOCTYPE html>
    <html>
    <head>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Registration Successful</title>

    <style>

    body {
        margin:0;
        min-height:100vh;

        display:flex;
        justify-content:center;
        align-items:center;

        background:#180b2d;

        font-family:Arial;
        color:white;
    }

    .box {
        width:85%;
        max-width:500px;

        padding:40px;

        text-align:center;

        border-radius:25px;

        background:#2b1746;

        box-shadow:0 10px 40px #000;
    }

    h1 {
        color:#ffd044;
    }

    a {
        display:inline-block;

        margin-top:25px;

        padding:15px 35px;

        border-radius:30px;

        background:#f4b400;

        color:#24122e;

        text-decoration:none;

        font-size:20px;
    }

    </style>

    </head>

    <body>

        <div class="box">

            <h1>✓ Registration Successful</h1>

            <p>Your account has been registered successfully.</p>

            <a href="/">
                Back to Register
            </a>

        </div>

    </body>
    </html>
    """


# ---------------- START SERVER ----------------

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    ) 
