from flask import render_template, make_response, request, redirect, url_for
from flask_login import current_user

from app import app_bp
from app.api.routes import refresh_token


@app_bp.route("/")
@app_bp.route("/documents")
@app_bp.route("/documents/<doc_id>")
def index(doc_id=None):
    user = current_user

    searched_term = request.args.get('search', '')
    if doc_id is not None and searched_term != '':
        return redirect(url_for("app_bp.index", search=searched_term, docId=None))

    resp = make_response(render_template("documents/document_index.html", docId=doc_id, search=searched_term))
    return refresh_token(user, resp)


#@app_bp.route("/documents/<id>")
#def document(id):
#    return render_template("documents/document_edit.html", id=id, base_url=request.host_url[0:-1])


@app_bp.route("/documentation")
def documentation():
    return render_template("docs/docs.html")


@app_bp.route("/about")
def about():
    return render_template("docs/about.html")

