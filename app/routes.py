from flask import render_template, current_app, flash, url_for, redirect, render_template_string
from flask_user import login_required

from app import app_bp,  db


@app_bp.route("/")
def index():
    return render_template("documents/document_index.html")


@app_bp.route("/documents/<id>")
def document(id):
    return render_template("documents/document_edit.html", id=id)


@app_bp.route("/documentation")
def documentation():
    return render_template("docs/docs.html")

