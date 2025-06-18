import os
import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from werkzeug.utils import secure_filename
from mongoengine import connect
from flask import abort
import config
from models import Report

# -----------------------------------------------------------------------------
# App & DB setup
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"]    = config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Connect MongoEngine
connect(host=config.MONGO_URI)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    """Show the 10 most recent reports."""
    reports = Report.objects.limit(10)
    return render_template("index.html", reports=reports)


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # 1) Gather form data
        kind        = request.form["kind"]
        name        = request.form["name"]
        description = request.form.get("description", "")
        date_str    = request.form.get("date")
        location    = request.form.get("location", "")
        contact     = request.form.get("contact", "")
        image_fn    = None

        # 2) Handle file upload
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            image_fn = filename

        # 3) Parse date
        date_obj = None
        if date_str:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", "danger")
                return redirect(url_for("submit"))

        # 4) Save to MongoDB
        report = Report(
            kind=kind,
            name=name,
            description=description,
            date=date_obj,
            location=location,
            contact=contact,
            image=image_fn,
        )
        report.save()

        flash("Your report has been submitted!", "success")
        return redirect(url_for("index"))

    return render_template("submit.html")


@app.route("/search")
def search():
    """Search by item name (case‑insensitive) and optional kind filter."""
    q    = request.args.get("q", "")
    kind = request.args.get("kind", None)

    query = {}
    if q:
        query["name__icontains"] = q
    if kind in ("lost", "found"):
        query["kind"] = kind

    results = Report.objects(**query)
    return render_template("search.html", results=results, q=q, kind=kind)

@app.route("/delete/<report_id>", methods=["POST"])
def delete(report_id):
    """Delete a specific report by ID."""
    report = Report.objects(id=report_id).first()
    if not report:
        abort(404)

    # Delete associated image
    if report.image:
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], report.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    report.delete()
    flash("Report deleted successfully.", "success")
    return redirect(url_for("index"))


@app.route("/update/<report_id>", methods=["GET", "POST"])
def update(report_id):
    """Update a specific report by ID."""
    report = Report.objects(id=report_id).first()
    if not report:
        abort(404)

    if request.method == "POST":
        # Update fields
        report.kind = request.form["kind"]
        report.name = request.form["name"]
        report.description = request.form.get("description", "")
        report.location = request.form.get("location", "")
        report.contact = request.form.get("contact", "")
        
        date_str = request.form.get("date")
        if date_str:
            try:
                report.date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", "danger")
                return redirect(url_for("update", report_id=report.id))

        # Handle new image (optional)
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            # Delete old image if exists
            if report.image:
                old_path = os.path.join(app.config["UPLOAD_FOLDER"], report.image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            report.image = filename

        report.save()
        flash("Report updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("update.html", report=report)

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
