import json
from flask import render_template, make_response, request, redirect, url_for, current_app, abort
from flask_login import current_user
from requests import Response

from app import app_bp, api_bp
from app.api.routes import refresh_token, pprint, Witness
from app.api.witness.facade import WitnessFacade
from app.models import Collection, Document


@app_bp.route("/")
@app_bp.route("/documents")
@app_bp.route("/documents/<int:doc_id>")
def index(doc_id=None):
    user = current_user

    searched_term = request.args.get('search', '')
    if doc_id is not None and searched_term != '':
        return redirect(url_for("app_bp.index", section="documents", data=json.dumps({
            'docId': None, 'searchedTerm': searched_term
        })))

    if doc_id is not None and not Document.query.filter(Document.id == doc_id).first():
        abort(status=404)

    resp = make_response(render_template("app/main.html",
                                         section="documents",
                                         data=json.dumps({
                                             'docId': doc_id, 'searchedTerm': searched_term
                                         })))
    return refresh_token(user, resp)


@app_bp.route("/collections")
@app_bp.route("/collections/<int:collection_id>")
def collections(collection_id=None):
    user = current_user

    if collection_id is not None and not Collection.query.filter(Collection.id == collection_id).first():
        abort(status=404)

    resp = make_response(render_template("app/main.html",
                                         section="collections",
                                         data=json.dumps({'collectionId': collection_id})))
    return refresh_token(user, resp)


@app_bp.route("/verrous")
def locks():
    user = current_user
    resp = make_response(render_template("app/main.html", section="locks",  data=json.dumps({})))
    return refresh_token(user, resp)


@app_bp.route("/favoris")
def bookmarks():
    user = current_user
    resp = make_response(render_template("app/main.html", section="bookmarks", data=json.dumps({})))
    return refresh_token(user, resp)


@app_bp.route("/historique")
def changelog():
    user = current_user
    resp = make_response(render_template("app/main.html", section="changelog", data=json.dumps({})))
    return refresh_token(user, resp)


@app_bp.route("/users/<action>")
def user_action(action):
    user = current_user

    if action == "login":
        return redirect(url_for("app_bp.login"))
    elif action == "logout":
        return redirect(url_for("app_bp.logout"))

    try:
        action_stub = current_app.view_functions['user.%s' % action.replace("-", '_')]
        action_template = action_stub()
    except Exception as e:
        pprint.pprint(current_app.view_functions)
        print(str(e))
        print("VIEW NOT FOUND:", action, 'user.%s' % action.replace("-", '_'))
        return redirect(url_for("app_bp.index"))

    resp = make_response(render_template("app/main.html",
                                         section="template",
                                         data=json.dumps({'template': action_template})))
    return refresh_token(user, resp)


@app_bp.route("/users/login")
def login():
    user = current_user
    if user.is_authenticated:
        return redirect(url_for("app_bp.index"))
    login_template = current_app.user_manager.login_view()
    resp = make_response(render_template("app/main.html",
                                         section="template",
                                         data=json.dumps({'template': login_template})))
    return refresh_token(user, resp)


@app_bp.route("/users/logout")
def logout():
    user = current_user
    if not user.is_authenticated:
        return redirect(url_for("app_bp.index"))
    current_app.user_manager.logout_view()
    return redirect(url_for('app_bp.index'))


@app_bp.route("/iiif/editor/witnesses/<witness_id>")
def iiif_editor(witness_id):
    user = current_user
    if not user.is_authenticated:
        return redirect(url_for("app_bp.index"))

    witness = Witness.query.filter(Witness.id == witness_id).first()
    if witness is None:
        abort(status=404)

    f_obj, errors, kwargs = WitnessFacade.get_facade('', witness)
    manifest_url = f_obj.get_iiif_manifest_url()

    return render_template("iiif-manifest-editor/editor.html", manifest_url=manifest_url)



