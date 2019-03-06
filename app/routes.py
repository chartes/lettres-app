import werkzeug
from flask import render_template, make_response, request, redirect, url_for, current_app
from flask_login import current_user

from app import app_bp
from app.api.routes import refresh_token, pprint


@app_bp.route("/")
@app_bp.route("/documents")
@app_bp.route("/documents/<doc_id>")
def index(doc_id=None):
    user = current_user

    searched_term = request.args.get('search', '')
    if doc_id is not None and searched_term != '':
        return redirect(url_for("app_bp.index", search=searched_term, docId=None))

    resp = make_response(render_template("app/homepage.html",
                                         section="documents",
                                         docId=doc_id,
                                         search=searched_term))
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

    resp = make_response(render_template("app/homepage.html", section="documents", template=action_template))
    return refresh_token(user, resp)


@app_bp.route("/users/login")
def login():
    user = current_user
    if user.is_authenticated:
        return redirect(url_for("app_bp.index"))
    login_template = current_app.user_manager.login_view()
    resp = make_response(render_template("app/homepage.html", template=login_template))
    return refresh_token(user, resp)


@app_bp.route("/users/logout")
def logout():
    user = current_user
    if not user.is_authenticated:
        return redirect(url_for("app_bp.index"))
    current_app.user_manager.logout_view()
    return redirect(url_for('app_bp.index'))





@app_bp.route("/documentation")
def documentation():
    return render_template("docs/docs.html")


@app_bp.route("/about")
def about():
    return render_template("docs/about.html")

