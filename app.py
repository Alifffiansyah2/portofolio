from flask import Flask, render_template, request, redirect, flash, url_for
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load variabel dari .env
load_dotenv()

EMAIL_USER = os.getenv("MAIL_USERNAME")
EMAIL_PASS = os.getenv("MAIL_PASSWORD")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# =======================
# Routes utama
# =======================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    resume_data = {
        "education": [
            {"title": "S1 Teknik Informatika", "year": "2022 - sekarang", "place": "Universitas Sangga Buana YPKP Bandung"},
            {"title": "Teknik Komputer dan Jaringan", "year": "2019 - 2022", "place": "SMKN 1 PACET"},
        ],
        "experience": [
            {"title": "Data Entryer", "year": "2024", "place": "Dago Mandala"},
            {"title": "Staff Administrasi Desa", "year": "2021", "place": "Desa Palasari Cianjur"},
        ]
    }
    return render_template("about.html", resume=resume_data)

projects_data = [
    {
        "id": 1,
        "title": "Aplikasi Short Video",
        "desc": "Aplikasi penayangan video pendek menggunakan Android Studio",
        "image": "assets/project-1.jpg",
        "tools": ["Android Studio", "CSS", "Kotlin"],
    },
    {
        "id": 2,
        "title": "Aplikasi Pengelola dan Penjualan Sampah",
        "desc": "Aplikasi Pengelola dan jual beli sampah",
        "image": "assets/project-2.jpg",
        "tools": ["Flutter", "HTML", "CSS"],
    },
    {
        "id": 3,
        "title": "Aplikasi Pengelola dan Penjualan Sampah (Web)",
        "desc": "Aplikasi pengelola dan penjualan sampah berbasis website.",
        "image": "assets/project-3.jpg",
        "tools": ["PhoneGap", "Tailwind", "JavaScript"],
    },
    {
        "id": 4,
        "title": "Website Perpustakaan",
        "desc": "Website perpustakaan dengan tampilan interaktif",
        "image": "assets/project-4.jpg",
        "tools": ["Laravel", "Tailwind", "JavaScript"],
    },
    {
        "id": 5,
        "title": "Website Sistem Pengajuan Kerja Praktik",
        "desc": "Sistem Pengajuan Kerja Praktik Berbasis Website",
        "image": "assets/project-5.jpg",
        "tools": ["Laravel", "Tailwind", "JavaScript"],
    },
]

@app.route("/projects")
def projects():
    certificates = [
        {
            "title": "Seminar Nasional - Tico 2025",
            "issuer": "Teknik Informatika Competition",
            "image": "assets/sertifTico.jpg"
        },
        {
            "title": "Java Foundation - Oracle",
            "issuer": "Oracle Academy",
            "image": "assets/sertifjava.jpeg"
        }
    ]

    tech_stack = [
    {"name": "Python", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"},
    {"name": "Flask", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg"},
    {"name": "HTML", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"},
    {"name": "CSS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"},
   {"name": "Tailwind", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg"},
    {"name": "JavaScript", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"},
    {"name": "Node.js", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg"},  # ✅ FIXED
    {"name": "Chart.js", "icon": "https://www.chartjs.org/media/logo-title.svg"},
]


    return render_template("projects.html", projects=projects_data, certificates=certificates, tech_stack=tech_stack)

@app.route("/projects/<int:id>")
def project_detail(id):
    project = next((p for p in projects_data if p["id"] == id), None)
    if not project:
        return "Project not found", 404
    return render_template("project_detail.html", project=project)

# =======================
# Contact Form
# =======================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        sender_email = request.form["email"]
        message = request.form["message"]

        try:
            # Format email
            email_content = f"Nama: {name}\nEmail: {sender_email}\n\nPesan:\n{message}"
            msg = EmailMessage()
            msg.set_content(email_content)
            msg["Subject"] = f"Pesan dari {name}"
            msg["From"] = EMAIL_USER
            msg["To"] = EMAIL_USER

            # Kirim email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)

            flash("Pesan berhasil dikirim!", "success")
        except Exception as e:
            print("Error:", e)
            flash("Terjadi kesalahan saat mengirim pesan.", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")

# =======================
# Run App
# =======================

if __name__ == "__main__":
    app.run(debug=True)
