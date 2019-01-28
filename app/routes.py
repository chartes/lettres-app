from flask import render_template, make_response, request
from flask_jwt_extended import set_access_cookies, create_access_token, unset_jwt_cookies
from flask_login import current_user

from app import app_bp
from app.api.routes import refresh_token


@app_bp.route("/")
@app_bp.route("/documents")
def index():
    user = current_user
    resp = make_response(render_template("documents/document_index.html"))
    return refresh_token(user, resp)


@app_bp.route("/documents/<id>")
def document(id):
    return render_template("documents/document_edit.html", id=id, base_url=request.host_url[0:-1])


@app_bp.route("/documentation")
def documentation():
    return render_template("docs/docs.html")

