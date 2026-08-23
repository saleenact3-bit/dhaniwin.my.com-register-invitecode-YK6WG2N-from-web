from flask import Flask, render_template_string, request, redirect, flash
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "my-secret-key"

DATABASE = "users.db"


# ================= DATABASE =================

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


# ================= HTML =================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Dhani Win Register</title>


<style>

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    min-height: 100vh;

    font-family: Arial, sans-serif;

    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d 70%
        );
}


/* ================= TOP ================= */

.top {

    height: 350px;

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            rgba(25, 5, 50, .40),
            rgba(25, 5, 50, .90)
        ),
        url("https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1200&auto=format&fit=crop");

    background-size: cover;

    background-position: center;
}


.back {

    position: absolute;

    left: 25px;

    top: 22px;

    font-size: 55px;

    font-weight: 200;
}


.language {

    position: absolute;

    right: 25px;

    top: 30px;

    font-size: 21px;
}


.logo {

    position: absolute;

    width: 100%;

    top: 120px;

    text-align: center;
}


.logo h1 {

    margin: 0;

    font-size: 58px;

    font-style: italic;

    color: #b85cff;
}


.logo h2 {

    margin: -5px 0 0;

    font-size: 48px;

    color: #ff9d16;
}


/* ================= FORM ================= */

.container {

    width: 92%;

    max-width: 780px;

    margin: 15px auto 40px;
}


/* INPUT BOX */

.input-box {

    height: 75px;

    margin: 18px 0;

    display: flex;

    align-items: center;

    padding: 0 18px;

    border-radius: 18px;

    border: 1px solid
        rgba(190, 145, 230, .45);

    background:
        rgba(43, 24, 70, .95);

    box-shadow:
        inset 0 0 15px
        rgba(0, 0, 0, .12);
}


.icon {

    width: 50px;

    font-size: 25px;

    text-align: center;

    color: #c9a8ff;
}


.country {

    font-size: 24px;

    font-weight: bold;

    margin-right: 12px;
}


input {

    width: 100%;

    height: 100%;

    border: none;

    outline: none;

    background: transparent;

    color: white;

    font-size: 21px;
}


input::placeholder {

    color: #a38abf;
}


.eye {

    margin-left: 10px;

    cursor: pointer;

    font-size: 23px;

    color: #c1a7d8;
}


/* ================= REGISTER ================= */

.register {

    width: 90%;

    height: 75px;

    display: block;

    margin: 35px auto 25px;

    border: none;

    border-radius: 45px;

    background:
        linear-gradient(
            #ffe56c,
            #f0a800
        );

    color: #28132f;

    font-size: 28px;

    cursor: pointer;

    box-shadow:
        0 8px 20px
        rgba(0, 0, 0, .30);
}


.register:active {

    transform: scale(.98);
}


/* ================= LOGIN ================= */

.login {

    width: 90%;

    height: 75px;

    margin: auto;

    display: flex;

    justify-content: center;

    align-items: center;

    border: 2px solid #d5a632;

    border-radius: 45px;

    color: #e8b83f;

    text-decoration: none;

    font-size: 25px;
}


/* ================= MESSAGE ================= */

.message {

    padding: 13px;

    margin: 10px;

    text-align: center;

    border-radius: 10px;

    background:
        rgba(255, 255, 255, .08);

    color: #ffd75a;

    font-size: 17px;
}

</style>

</head>


<body>


<!-- ================= TOP ================= -->

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



<!-- ================= FORM ================= -->

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
      action="/register">


<!-- PHONE NUMBER -->

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

        👁

    </div>

</div>



<!-- CONFIRM PASSWORD -->

<div class="input-box">

    <div class="icon">
        🔒
    </div>


    <input
        type="password"
        id="confirm_password"
        name="confirm_password"
        placeholder="Enter the password again"
        minlength="8"
        maxlength="15"
        required>


    <div
        class="eye"
        onclick="showPassword('confirm_password')">

        👁

    </div>

</div>



<!-- REGISTER BUTTON -->

<button
    type="submit"
    class="register">

    Register

</button>


</form>



<!-- PASSWORD LOGIN -->

<a
    href="#"
    class="login">

    Password Login

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


# ================= HOME =================

@app.route("/")
def home():

    return render_template_string(HTML)


# ================= REGISTER =================

@app.route("/register", methods=["POST"])
def register():

    phone = request.form.get(
        "phone", ""
    ).strip()

    password = request.form.get(
        "password", ""
    )

    confirm_password = request.form.get(
        "confirm_password", ""
    )


    # PHONE CHECK

    if not phone.isdigit() or len(phone) != 10:

        flash(
            "Please enter a valid 10-digit phone number."
        )

        return redirect("/")


    # PASSWORD CHECK

    if len(password) < 8 or len(password) > 15:

        flash(
            "Password must be 8-15 characters."
        )

        return redirect("/")


    # PASSWORD MATCH

    if password != confirm_password:

        flash(
            "Passwords do not match."
        )

        return redirect("/")


    # HASH PASSWORD

    hashed_password = generate_password_hash(
        password
    )


    # SAVE USER

    try:

        conn = sqlite3.connect(DATABASE)


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

        return redirect("/")


    # SUCCESS

    return redirect("/success")


# ================= SUCCESS PAGE =================

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

    margin: 0;

    min-height: 100vh;

    display: flex;

    justify-content: center;

    align-items: center;

    background: #180b2d;

    color: white;

    font-family: Arial;
}


.box {

    width: 80%;

    max-width: 500px;

    padding: 40px;

    text-align: center;

    background: #2b1746;

    border-radius: 25px;
}


h1 {

    color: #ffd044;
}


a {

    display: inline-block;

    margin-top: 20px;

    padding: 15px 35px;

    background: #f4b400;

    border-radius: 30px;

    color: #24122e;

    text-decoration: none;

    font-size: 18px;
}

</style>

</head>


<body>

<div class="box">

    <h1>
        ✓ Registration Successful
    </h1>

    <p>
        Your account has been registered successfully.
    </p>

    <a href="/">
        Back
    </a>

</div>

</body>

</html>
"""


# ================= START =================

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
