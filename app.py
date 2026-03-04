from flask import Flask, request, jsonify, send_file
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__, static_folder=".")

# ── Static sender credentials ──────────────────────────────────────────────
# On Render: set GMAIL_USER and GMAIL_PASS as environment variables
SENDER_EMAIL = os.environ.get("GMAIL_USER", "prashisshirsat17@gmail.com")
SENDER_PASSWORD = os.environ.get("GMAIL_PASS", "cxwavbahiyfkpzgk")  # Gmail App Password

# ── Static email content ───────────────────────────────────────────────────
SUBJECT = "Why I'm the PM You Didn't Know You Needed (Yet!) 🚀"

BODY_HTML = """\
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.7; color: #222;">
<p>Hey,</p>

<p>When I came across your organization's APM/PM opening, I knew I had to shoot my shot—
think of this email as my <strong>Steph Curry moment in the fourth quarter</strong>. 🏀</p>

<p>Here's why bringing me on board would be a game-winning move:</p>

<p>🔵 <strong>User-Obsessed &amp; Data-Driven</strong> – I don't just analyze data; I <em>live</em> in it.
At <strong>BharatPe</strong>, I managed the RTO (Return-to-Origin) project, reducing failed deliveries
by 25% and cutting operational costs by 20%. At <strong>Freshworks</strong>, I optimized predictive
analytics models, boosting efficiency by 20% and increasing adoption by 15%.</p>

<p>🔵 <strong>Master of the Cross-Functional Hustle</strong> – I know great products aren't built
in silos. Whether it's rallying engineers, designers, or business teams, I bring everyone to
the table (and, yes, I'll probably bring snacks too). At <strong>IndusInd Bank</strong>, my
pre-approved base strategies drove a 21% portfolio surge and a 33% conversion rate.</p>

<p>🔵 <strong>Creative Problem-Solver Extraordinaire</strong> – Give me a whiteboard and a marker,
and I'm ready to break down any user pain point. At <strong>MakeMyTrip</strong>, I designed a
multi-modal travel booking experience that made switching between transport modes seamless—because
no one likes travel headaches.</p>

<p>But beyond the metrics, I love building products that users actually <em>love</em>. I thrive in
fast-paced environments, obsess over customer feedback, and believe that every challenge is just
an opportunity in disguise.</p>

<p>So, what do you say? Let's chat—I'd love to discuss how I can help your organization level up.</p>

<p>
📄 <strong>Resume:</strong>
<a href="https://drive.google.com/file/d/1hG_vFCKwX0Cn0dsayjOmrYc3LahbaGk1/view?usp=sharing">
View My Resume
</a>
</p>

<p>
Best,<br>
<strong>Prashis Shirsat</strong><br>
📧 prashisshirsat17@gmail.com<br>
🔗 <a href="https://www.linkedin.com/in/prashis-shirsat-522ab2173/">LinkedIn Profile</a>
</p>
</body>
</html>
"""

@app.route("/")
def index():
    # Fix for "Not Found" error on Render: use absolute path based on this file's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_file(os.path.join(base_dir, "index.html"))

@app.route("/send", methods=["POST"])
def send_email():
    data = request.get_json()
    to_email = data.get("to_email", "").strip()

    if not to_email:
        return jsonify({"success": False, "message": "Recipient email is required."}), 400

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT
        msg["From"]    = f"Prashis Shirsat <{SENDER_EMAIL}>"
        msg["To"]      = to_email

        msg.attach(MIMEText(BODY_HTML, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        return jsonify({"success": True, "message": f"Email sent to {to_email} ✅"})

    except smtplib.SMTPAuthenticationError:
        return jsonify({
            "success": False,
            "message": "Authentication failed. Make sure you're using a Gmail App Password."
        }), 401
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
