from flask import render_template, make_response
from flask_jwt_extended import set_access_cookies, create_access_token, unset_jwt_cookies
from flask_login import current_user

from app import app_bp


@app_bp.route("/")
@app_bp.route("/documents")
def index():
    resp = make_response(render_template("documents/document_index.html"))

    user = current_user
    if not user.is_anonymous:
        access_token = create_access_token(identity=user.to_json())
        resp.headers["login"] = True
        set_access_cookies(resp, access_token)
    else:
        resp.headers["logout"] = True
        unset_jwt_cookies(resp)

    return resp, 200


@app_bp.route("/documents/<id>")
def document(id):
    return render_template("documents/document_edit.html", id=id)


@app_bp.route("/documentation")
def documentation():
    return render_template("docs/docs.html")

