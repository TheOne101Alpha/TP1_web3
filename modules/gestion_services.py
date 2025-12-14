"""
Module pour la gestion des services
"""
import re
from datetime import datetime
from flask import Blueprint, render_template, session, abort, request, redirect, flash, current_app as app
import bd

reg_html = re.compile(r"(<(.*)>.*?|<(.*) />)")

bp_gestion_services = Blueprint('gestion_services', __name__)

@bp_gestion_services.route('/')
def index():
    """Affiche les services"""
    app.logger.info("Affichage de la liste des services")

    authentifier = False

    app.logger.debug("Vérification de l'authentification de l'utilisateur")
    if "id" in session:
        authentifier = True

    
    retour = bd.get_services()
    app.logger.debug("Récupération des services dans la base de données: %d services trouvés", len(retour))

    return render_template("gestion_services/services.jinja",
                           authentifier=authentifier, lesservices=retour)


@bp_gestion_services.route('/details/<int:id_service>')
def details(id_service):
    """Affiche un service en particulier"""
    app.logger.info(f"Affichage des détails du service {id_service}")

    proprietaire = False

    retour = bd.get_service(id_service)

    if not retour:
        app.logger.warning(f"Le service {id_service} n'existe pas, abort 404")
        abort(404)

    if retour['proprietaire'] in session:
        app.logger.debug(f"L'utilisateur {session.get('id')} est le propriétaire du service {id_service}")
        proprietaire = True

    app.logger.info(f"Affichage des détails du service {id_service}")
    return render_template('/gestion_services/details.jinja',
                           item=retour, proprietaire=proprietaire)


@bp_gestion_services.route('/changement/<int:id_change>', methods=['GET', 'POST'])
def changement(id_change):
    """affichage de changement ou ajout de services"""
    app.logger.info(f"Modification du service {id_change} demandée")

    if not id_change:
        app.logger.error("Le parametre id est manquant, abort 400")
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
            app.logger.debug("Les informations sont invalides, retour à la page de modification")
            return render_template("/gestion_services/changement.jinja", titre_page= "changement",
                                   valide_nom = v_nom, valide_localisation = v_local,
                                     valide_description = v_descr)
        
        # Sinon ajoute les données à la bd à l'aide de update
        app.logger.debug("Les informations sont valides, mise à jour du service dans la base de données")
        date = datetime.now()
        try:
            bd.update_service(id_change, nom, description, localisation, actif, cout, date)
        except Exception as e:
            app.logger.error(f"Erreur lors de la mise à jour du service {id_change}: {e}")
            return abort(500, "Erreur lors de la mise à jour du service")
        
        app.logger.debug(f"Service {id_change} mis à jour avec succès")
        flash('Changement réussi avec succès')
        return redirect("/", code=303)
    
    retour = bd.get_service(id_change)
    categorie = bd.get_categories()
    return render_template("/gestion_services/changement.jinja", service=retour, categories=categorie)

@bp_gestion_services.route("/ajout", methods=['GET', 'POST'])
def ajout():
    """ajoute un nouveau service dans la bd"""
    app.logger.info("Ajout d'un nouveau service demandé")
    categories = bd.get_categories()

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
            app.logger.debug("Les informations sont invalides, retour à la page d'ajout")
            return render_template("/gestion_services/ajout.jinja", titre_page= "ajout",
                                   valide_nom = v_nom, valide_localisation = v_local,
                                     valide_description = v_descr, titre = nom,
                                     local=localisation, description=description,cout = cout)
        # Sinon ajoute les données à la bd à l'aide de INSERT
        if bd.add_service(session['id'], nom, description, localisation, datetime.now(), categorie, actif, cout):
            flash('Ajout réussi avec succès')
            app.logger.debug("Nouveau service ajouté avec succès")
            return redirect('/', code=303)
    
        app.logger.error("Erreur lors de l'ajout du nouveau service")
        return abort(500, "Erreur lors de l'ajout du service")

    categorie = bd.get_categories()
    return render_template("/gestion_services/ajout.jinja",titre_page = "ajout service",
                                    liste_categorie = categories)

@bp_gestion_services.route('/supprimer/<int:id_service>', methods=['POSt'])
def supprimer(id_service):
    """Permet de supprimer un service"""
    app.logger.info(f"Suppression du service {id_service} demandée")
    if(bd.delete_service(id_service)):
        app.logger.debug(f"Service {id_service} supprimé avec succès")
    else:
        app.logger.error(f"Erreur lors de la suppression du service {id_service}")
        return abort(500, "Erreur lors de la suppression du service")
    flash('Suppression réussi avec succès')
    return redirect('/', code=303)

@bp_gestion_services.route('/reserver/<int:id_service>')
def reserver(id_service):
    """Permet de reserver un service particulier"""
    if bd.book_service(id_service, session['id']):
        app.logger.debug(f"Service {id_service} réservé avec succès par l'utilisateur {session.get('id')}")
    else:
        app.logger.error(f"Erreur lors de la réservation du service {id_service} par l'utilisateur {session.get('id')}")
        return abort(500, "Erreur lors de la réservation du service")
    return redirect('/', code=303)