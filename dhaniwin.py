from flask import Flask, render_template_string, request, redirect, session, flash
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
# ADMIN LOGIN
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


# IMPORTANT:
# Render/Gunicorn-ലും database table ഉണ്ടാകാൻ
# ഇത് main block-ന് പുറത്താണ്.
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

<title>Dhani Win Register</title>

<style>

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

    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366 0%,
            #211036 48%,
            #170b29 100%
        );

    overflow-x: hidden;
}


/* =====================================================
   TOP
   ===================================================== */

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


.back {

    position: absolute;

    top: 18px;
    left: 18px;

    font-size: 42px;

    color: white;
}


.language {

    position: absolute;

    top: 20px;
    right: 18px;

    font-size: 15px;
}


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


/* =====================================================
   CONTAINER
   ===================================================== */

.container {

    width: calc(100% - 32px);

    max-width: 430px;

    margin: 12px auto 30px;
}


/* =====================================================
   MESSAGE
   ===================================================== */

.message {

    padding: 10px;

    margin-bottom: 10px;

    text-align: center;

    border-radius: 10px;

    background:
        rgba(255,255,255,0.08);

    color: #ffd75a;

    font-size: 14px;
}


/* =====================================================
   INPUT BOX
   ===================================================== */

.input-box {

    width: 100%;

    height: 58px;

    margin-bottom: 13px;

    display: flex;

    align-items: center;

    padding: 0 13px;

    border-radius: 14px;

    border: 1px solid
        rgba(190,145,230,0.42);

    background:
        rgba(43,24,70,0.94);
}


.icon {

    width: 34px;

    min-width: 34px;

    text-align: center;

    font-size: 19px;

    color: #bea1dd;
}


.country {

    margin-right: 9px;

    font-size: 19px;

    font-weight: 600;
}


input {

    width: 100%;

    min-width: 0;

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


/* =====================================================
   EYE
   ===================================================== */

.eye-button {

    width: 30px;

    min-width: 30px;

    height: 30px;

    position: relative;

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

    position: absolute;

    width: 5px;

    height: 5px;

    background: #bda5d6;

    border-radius: 50%;

    top: 2px;

    left: 6px;
}


/* =====================================================
   REGISTER BUTTON
   ===================================================== */

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
            #ffe66b,
            #ffc21c,
            #efa800
        );

    color: #28132f;

    font-size: 20px;

    cursor: pointer;
}


.register:active {

    transform: scale(0.985);
}


/* =====================================================
   ADMIN BUTTON
   ===================================================== */

.admin-link {

    width: 100%;

    height: 45px;

    display: flex;

    justify-content: center;

    align-items: center;

    color: #a992bd;

    text-decoration: none;

    font-size: 14px;
}


/* =====================================================
   LAPTOP
   ===================================================== */

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
    }

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
        onclick="togglePassword('password')">

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
        onclick="togglePassword('confirmPassword')">

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
    href="/admin"
    class="admin-link">

    Admin Login

</a>


</div>


<script>

function togglePassword(id) {

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
# REGISTER
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        REGISTER_HTML
    )


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


    # PHONE VALIDATION

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


    flash(
        "Registration successful."
    )

    return redirect("/")


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

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );

    color: white;
}


.box {

    width: 100%;

    max-width: 390px;

    padding: 28px 20px;

    background: #2b1746;

    border: 1px solid
        rgba(190,145,230,.35);

    border-radius: 22px;
}


h1 {

    text-align: center;

    margin-bottom: 25px;

    color: #ffd044;

    font-size: 28px;
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


.message {

    margin-bottom: 15px;

    padding: 10px;

    border-radius: 8px;

    text-align: center;

    color: #ffd75a;

    background:
        rgba(255,255,255,.08);
}


.back {

    display: block;

    margin-top: 18px;

    text-align: center;

    color: #bfa7d1;

    text-decoration: none;

}

</style>

</head>

<body>


<div class="box">

<h1>
    Admin Login
</h1>


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
    Login
</button>


</form>


<a
    href="/"
    class="back">

    ← Back

</a>


</div>


</body>

</html>

"""


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin")
def admin_login():

    if session.get("admin_logged_in"):

        return redirect("/admin/dashboard")

    return render_template_string(
        ADMIN_LOGIN_HTML
    )


@app.route("/admin/login", methods=["POST"])
def admin_login_submit():

    admin_id = request.form.get(
        "admin_id",
        ""
    ).strip()

    admin_password = request.form.get(
        "admin_password",
        ""
    )


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

ADMIN_DASHBOARD_HTML = """

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

    padding: 20px;

    font-family: Arial;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );

    color: white;
}


.container {

    width: 100%;

    max-width: 900px;

    margin: auto;
}


.header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 15px;

    margin-bottom: 20px;
}


h1 {

    color: #ffd044;

    font-size: 26px;
}


.logout {

    padding: 10px 17px;

    border: 1px solid #c99b37;

    border-radius: 20px;

    color: #ffd044;

    text-decoration: none;

    font-size: 14px;
}


.card {

    overflow-x: auto;

    background: #2b1746;

    border: 1px solid
        rgba(190,145,230,.35);

    border-radius: 18px;

    padding: 15px;
}


table {

    width: 100%;

    border-collapse: collapse;

    min-width: 450px;
}


th {

    color: #ffd044;

    text-align: left;

    padding: 13px;

    border-bottom: 1px solid #5d4074;
}


td {

    padding: 13px;

    border-bottom: 1px solid #49335b;

    color: #e4d9ec;
}


.empty {

    text-align: center;

    padding: 35px;

    color: #a995b7;
}


.count {

    margin-bottom: 15px;

    color: #c6b5d1;
}


.reset {

    display: inline-block;

    padding: 7px 11px;

    border-radius: 15px;

    background: #f0ae14;

    color: #24122e;

    text-decoration: none;

    font-size: 12px;
}


@media (max-width: 500px) {

    body {
        padding: 12px;
    }

    .header {
        align-items: flex-start;
    }

    h1 {
        font-size: 22px;
    }

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

    <th>Password</th>

    <th>Action</th>

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

    <td>
        ••••••••••••••••
    </td>

    <td>

        <a
            href="/admin/reset/{{ user[0] }}"
            class="reset">

            Reset

        </a>

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
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):

        return redirect("/admin")


    conn = sqlite3.connect(DATABASE)

    users = conn.execute(
        """
        SELECT id, phone
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()


    return render_template_string(
        ADMIN_DASHBOARD_HTML,
        users=users
    )


# =========================================================
# RESET PASSWORD PAGE
# =========================================================

RESET_HTML = """

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>Reset Password</title>

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

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );

    color: white;
}


.box {

    width: 100%;

    max-width: 400px;

    padding: 25px 20px;

    border-radius: 20px;

    background: #2b1746;
}


h2 {

    color: #ffd044;

    text-align: center;

    margin-bottom: 10px;
}


.phone {

    text-align: center;

    color: #c8b5d4;

    margin-bottom: 20px;
}


input {

    width: 100%;

    height: 55px;

    padding: 0 14px;

    margin-bottom: 15px;

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

    font-size: 18px;
}


a {

    display: block;

    margin-top: 17px;

    text-align: center;

    color: #bda5d6;

    text-decoration: none;
}

</style>

</head>


<body>


<div class="box">

<h2>
    Reset Password
</h2>


<div class="phone">

    +91 {{ phone }}

</div>


<form method="POST">


<input
    type="password"
    name="new_password"
    placeholder="New password"
    minlength="8"
    maxlength="15"
    required>


<input
    type="password"
    name="confirm_password"
    placeholder="Confirm new password"
    minlength="8"
    maxlength="15"
    required>


<button type="submit">

    Save New Password

</button>


</form>


<a href="/admin/dashboard">

    ← Back to Dashboard

</a>


</div>


</body>

</html>

"""


# =========================================================
# RESET PASSWORD
# =========================================================

@app.route(
    "/admin/reset/<int:user_id>",
    methods=["GET", "POST"]
)
def reset_password(user_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin")


    conn = sqlite3.connect(DATABASE)

    user = conn.execute(
        """
        SELECT phone
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    conn.close()


    if not user:

        flash("User not found.")

        return redirect(
            "/admin/dashboard"
        )


    phone = user[0]


    if request.method == "POST":

        new_password = request.form.get(
            "new_password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        if len(new_password) < 8:

            flash(
                "Password must contain at least 8 characters."
            )

            return redirect(
                f"/admin/reset/{user_id}"
            )


        if len(new_password) > 15:

            flash(
                "Password cannot exceed 15 characters."
            )

            return redirect(
                f"/admin/reset/{user_id}"
            )


        if new_password != confirm_password:

            flash(
                "Passwords do not match."
            )

            return redirect(
                f"/admin/reset/{user_id}"
            )


        hashed_password = generate_password_hash(
            new_password
        )


        conn = sqlite3.connect(DATABASE)

        conn.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (
                hashed_password,
                user_id
            )
        )

        conn.commit()

        conn.close()


        flash(
            "Password reset successfully."
        )

        return redirect(
            "/admin/dashboard"
        )


    return render_template_string(
        RESET_HTML,
        phone=phone
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
        port=5000,
        debug=True
    )


