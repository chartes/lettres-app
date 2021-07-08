from flask import render_template, redirect, url_for, abort
from flask_login import current_user

from app import app_bp
from app.api.routes import  Witness
from app.api.witness.facade import WitnessFacade


#@app_bp.route("/iiif/editor/witnesses/<witness_id>")
#def iiif_editor(witness_id):
#    user = current_user
#    if not user.is_authenticated:
#        return redirect(url_for("app_bp.index"))
#
#    witness = Witness.query.filter(Witness.id == witness_id).first()
#    if witness is None:
#        abort(status=404)
#
#    f_obj, errors, kwargs = WitnessFacade.get_facade('', witness)
#    manifest_url = f_obj.get_iiif_manifest_url()
#
#    return render_template("iiif-manifest-editor/editor.html", manifest_url=manifest_url)



