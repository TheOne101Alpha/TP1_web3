"""
Module pour la gestion des services
"""
from flask import Blueprint, render_template, session, abort
import bd

bp_gestion_services = Blueprint('gestion_services', __name__)

@bp_gestion_services.route('/')
def index():
    """Affiche les services"""

    authentifier = False

    if "nom" in session:
        authentifier = True

    retour = bd.get_services()

    return render_template("/gestion_services/services.jinja",
                           authentifier=authentifier, lesservices=retour)


@bp_gestion_services.route('/details/<int:id_service>')
def service(id_service):
    """Affiche un service en particulier"""

    proprietaire = False
    offert = False
    disponible = False
    retour = bd.get_service(id_service)

    if not retour:
        abort(404)

    #if retour['proprietaire'] in session:
        #proprietaire = True

    if proprietaire is False and retour['actif'] > 1:
        disponible = True

    return render_template('/gestion_services/details.jinja',
                           item=retour, proprietaire=proprietaire, offert=offert, disponible=disponible)
