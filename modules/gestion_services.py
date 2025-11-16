"""
Module pour la gestion des services
"""
import re
from datetime import datetime
from flask import Blueprint, render_template, session, abort, request, redirect, flash
import bd

reg_html = re.compile(r"(<(.*)>.*?|<(.*) />)")

bp_gestion_services = Blueprint('gestion_services', __name__)

@bp_gestion_services.route('/')
def index():
    """Affiche les services"""

    authentifier = False

    if "id" in session:
        authentifier = True

    retour = bd.get_services()

    return render_template("gestion_services/services.jinja",
                           authentifier=authentifier, lesservices=retour)


@bp_gestion_services.route('/details/<int:id_service>')
def details(id_service):
    """Affiche un service en particulier"""

    proprietaire = False
    offert = False
    disponible = False
    retour = bd.get_service(id_service)
    if not retour:
        abort(404)

    if retour['proprietaire'] in session:
        proprietaire = True

    if proprietaire is False and retour['actif'] > 1:
        disponible = True

    return render_template('/gestion_services/details.jinja',
                           item=retour, proprietaire=proprietaire,
                             offert=offert, disponible=disponible)


@bp_gestion_services.route('/changement/<int:id_change>', methods=['GET', 'POST'])
def changement(id_change):
    """affichage de changement ou ajout de services"""
    if not id_change:
        abort(400, "le parametre id est manquant")

    v_nom = ""
    v_local=""
    v_descr=""

    nom = request.form.get("nom_service","")
    localisation = request.form.get("localisation_service","")
    description = request.form.get("description_service","")
    actif = request.form.get("actif_service", 0, type=int)
    cout = request.form.get('cout', 0, type=float)
    if request.method == 'POST':
        if reg_html.fullmatch(nom) or len(nom) < 1 or len(nom) > 50:
            v_nom = "is-invalid"
        if reg_html.fullmatch(localisation) or len(localisation) < 5 or len(localisation) > 50:
            v_local = "is-invalid"
        if reg_html.fullmatch(description) or len(description) < 5 or len(description) > 2000:
            v_descr = "is-invalid"

        if v_nom or v_local or v_descr:
            # si un des champs est faux
            # retourne sur la même page
            return render_template("changement.jinja", titre_page= "changement",
                                   valide_nom = v_nom, valide_localisation = v_local,
                                     valide_description = v_descr)
        # Sinon ajoute les données à la bd à l'aide de update
        date = datetime.now()
        bd.update_service(id_change, nom, description, localisation, actif, cout, date)
        flash('Changement réussi avec succès')
        return redirect("/merci_modif", code=303)

    retour = bd.get_service(id_change)
    categorie = bd.get_categories()
    return render_template("changement.jinja", service=retour, categorie=categorie)

@bp_gestion_services.route("/ajout", methods=['GET', 'POST'])
def ajout():
    """ajoute un nouveau service dans la bd"""
    categories = []

    v_nom = ""
    v_local=""
    v_descr=""

    nom = request.form.get("nom_service", default= "")
    localisation = request.form.get("localisation_service", default= "")
    description = request.form.get("description_service", default= "")
    categorie = request.form.get("choix_categorie", default=None, type=int)
    actif = request.form.get("actif_service", default= 0, type=int)
    cout = request.form.get('cout', default=0, type=int)
    if request.method == 'POST':
        if reg_html.fullmatch(nom) or len(nom) < 1 or len(nom) > 50:
            v_nom = "is-invalid"
        if reg_html.fullmatch(localisation) or len(localisation) < 5 or len(localisation) > 50:
            v_local = "is-invalid"
        if reg_html.fullmatch(description) or len(description) < 5 or len(description) > 2000:
            v_descr = "is-invalid"

        if v_nom or v_local or v_descr:
            # si un des champs est faux
            # retourne sur la même page
            return render_template("/gestion_services/ajout.jinja", titre_page= "ajout",
                                   valide_nom = v_nom, valide_localisation = v_local,
                                     valide_description = v_descr, titre = nom,
                                     local=localisation, description=description,cout = cout)
        # Sinon ajoute les données à la bd à l'aide de INSERT
        if bd.add_service(nom, description, localisation, datetime.now, categorie, actif, cout):
            flash('Ajout réussi avec succès')
            return redirect("/", code=303)

    categorie = bd.get_categories()
    return render_template("/gestion_services/ajout.jinja",titre_page = "ajout service",
                                    liste_categorie = categories)

@bp_gestion_services.route('/supprimer/<int:id_service>', methods=['POSt'])
def supprimer(id_service):
    """Permet de supprimer un service"""

    bd.delete_service(id_service)
    flash('Suppression réussi avec succès')
    redirect('/', code=303)

@bp_gestion_services.route('/reserver/<int:id_service>')
def reserver(id_service):
    """Permet de reserver un service particulier"""
    bd.book_service(id_service, session['id'])
    redirect('/', code=303)