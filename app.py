from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
import os
import json
import boto3

from analysis import analyze_csv
from ml_model import predict_performance

from pdf_generator import (
    generate_class_report,
    generate_student_report
)

from flask import send_file

app = Flask(__name__)
app.secret_key = "student-analytics-secret"

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(
    UPLOAD_FOLDER, 
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

S3_BUCKET = "student-performance-analytics-deepak"
AWS_REGION = "ap-south-1"


def upload_to_s3(file_path, filename):

    try:
        s3 = boto3.client("s3")

        s3.upload_file(
            file_path,
            S3_BUCKET,
            f"uploads/{filename}"
        )

        print(f"Uploaded {filename} to S3")

        return True

    except Exception as e:
        print("S3 Upload Error:", e)
        return False


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    if "csv_file" not in request.files:
        return render_template(
            "index.html",
            error="Please select a file"
        )

    file = request.files["csv_file"]

    if file.filename == "":
        return render_template(
            "index.html",
            error="Please select a file"
        )

    allowed_extensions = (
        ".csv",
        ".xlsx",
        ".xls"
    )

    if not file.filename.lower().endswith(
        allowed_extensions
    ):
        return render_template(
            "index.html",
            error="Only CSV, XLSX and XLS files are supported"
        )

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    try:

        analytics = analyze_csv(
            filepath
        )

        ml_results = predict_performance(
            filepath
        )

        analytics["ml"] = ml_results

        analytics["s3_uploaded"] = upload_to_s3(
            filepath,
            filename
        )

        session["results"] = json.dumps(
            analytics
        )

        return redirect(
            url_for("dashboard")
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=f"File processing failed: {str(e)}"
        )

@app.route("/dashboard")
def dashboard():

    if "results" not in session:
        return redirect(url_for("index"))

    results = json.loads(
        session["results"]
    )

    return render_template(
        "dashboard.html",
        results=results
    )


@app.route("/search", methods=["POST"])
def search():

    if "results" not in session:
        return jsonify({
            "found": False
        })

    roll_number = request.json.get(
        "roll_number",
        ""
    )

    results = json.loads(
        session["results"]
    )

    for student in results["students"]:

        if str(
            student["roll_number"]
        ) == str(
            roll_number
        ):

            return jsonify({
                "found": True,
                "student": student
            })

    return jsonify({
        "found": False
    })

@app.route("/download-class-report")
def download_class_report():

    if "results" not in session:
        return redirect(
            url_for("index")
        )

    results = json.loads(
        session["results"]
    )

    pdf_path = os.path.join(
        REPORT_FOLDER,
        "class_report.pdf"
    )

    generate_class_report(
        results,
        pdf_path
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )

@app.route(
    "/download-student-report/<roll_number>"
)
def download_student_report(
    roll_number
):

    if "results" not in session:
        return redirect(
            url_for("index")
        )

    results = json.loads(
        session["results"]
    )

    for student in results["students"]:

        if str(
            student["roll_number"]
        ) == str(
            roll_number
        ):

            filename = (
                f"{student['name']}_report.pdf"
            )

            pdf_path = os.path.join(
                REPORT_FOLDER,
                filename
            )

            generate_student_report(
                student,
                pdf_path
            )

            return send_file(
                pdf_path,
                as_attachment=True
            )

    return "Student not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)