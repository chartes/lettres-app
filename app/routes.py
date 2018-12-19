from flask import render_template, current_app, flash, url_for, redirect

from app import app_bp,  db


@app_bp.route("/")
def index():
    return render_template("documents/document_index.html")


@app_bp.route("/documents/<id>")
def document(id):
    return render_template("documents/document_edit.html", id=id)


@app_bp.route("/api")
def index_api():
    return render_template("main/index.html")


@app_bp.route("/documentation")
def documentation():
    return render_template("docs/docs.html")


@app_bp.route("/recreate-database")
def recreate_database():
    if current_app.config["DEBUG"] and current_app.config["ENV"] != "production" and current_app.config["GENERATE_FAKE_DATA"]:
        print("Recreating database...")
        with current_app.app_context():
            db.drop_all()
            db.create_all()

            # === load some fake data
            from db.fixtures.create_fake_data import create_fake_documents, create_fake_users
            print("Generating fake data...", end=" ", flush=True)
            create_fake_users(db, nb_users=10)
            create_fake_documents(db, nb_docs=50, nb_correspondents=20)
            print("done !")
            flash('Database recreated with fake data !')

    return redirect(url_for('app_bp.index'))
