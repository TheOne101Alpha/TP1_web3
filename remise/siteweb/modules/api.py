import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, Blueprint, session, url_for, flash, jsonify, current_app as app
import bd

bp_api = Blueprint('api', __name__)

@bp_api.route('/services/all', methods=['GET'])
def get_all_services():
    """Retourne tous les titres et id des services en format JSON"""
    app.logger.info("Récupération de tous les services pour l'API")
    services = bd.get_services()
    retour = []
    for item in services:
        service = dict(id=item["id_service"], titre = item['titre'])
        retour.append(service)
    app.logger.debug(f"{len(retour)} services récupérés pour l'API : \n{retour}")
    return jsonify(retour)

@bp_api.route('/services/all_details', methods=['GET'])
def get_all_services_details():
    """Retourne tous les services en format JSON"""
    app.logger.info("Récupération de tous les services détaillés pour l'API")
    services = bd.get_services()
    app.logger.debug(f"{len(services)} services détaillés récupérés pour l'API : \n{services}")
    return jsonify(services)

@bp_api.route('/Compte/all_mail', methods=['GET'])
def get_all_mail():
    """Retourne tous les mails dans la BD pour les comparer"""
    app.logger.info("Récupération de tous les noms de compte pour l'API")
    comptes = bd.get_comptes()
    retour = []
    for item in comptes:
        retour.append(item["nom"])
    app.logger.debug(f"{len(retour)} noms de compte récupérés pour l'API")
    return jsonify(retour)

@bp_api.route('/compte/all', methods=['GET'])
def get_all():
    """Retourne tous les comptes dans la BD"""
    app.logger.info("Récupération de tous les comptes pour l'API")
    comptes = bd.get_comptes()
    app.logger.debug(f"{len(comptes)} comptes récupérés pour l'API")
    return jsonify(comptes)

@bp_api.route('/compte/supprimer/<int:id_compte>', methods=['GET'])
def supp_compte(id_compte):
    """Retourne tous les mails dans la BD pour les comparer"""
    app.logger.info(f"Suppression du compte {id_compte} demandée via l'API")
    retour = bd.delete_compte(id_compte)
    if(retour):
        app.logger.debug(f"Compte {id_compte} supprimé avec succès via l'API")
    else:
        app.logger.error(f"Erreur lors de la suppression du compte {id_compte} via l'API")
    return jsonify(retour)

@bp_api.route('/reservation/check_date/<int:id_service>', methods=['GET'])
def check_date(id_service):
    """ Retourne la disponibilité d'un service"""
    app.logger.info(f"Vérification de la disponibilité du service {id_service} via l'API")
    service = bd.get_service(id_service)
    app.logger.debug(f"Service {id_service} récupéré via l'API")
    return jsonify(bool(service.get('locataire') is None))

@bp_api.route('/services/supprimer/<int:id_service>', methods=['GET'])
def supprimer_service(id_service):
    """Supprime un service"""
    app.logger.info(f"Suppression du service {id_service} demandée via l'API")
    retour = bd.delete_service(id_service)
    if(retour):
        app.logger.debug(f"Service {id_service} supprimé avec succès via l'API")
    else:
        app.logger.error(f"Erreur lors de la suppression du service {id_service} via l'API")
    return jsonify(retour)

@bp_api.route('/services/mes_services/<int:id_utilisateur>', methods=['GET'])
def mes_services(id_utilisateur):
    """Retourne les services de l'utilisateur connecté"""
    app.logger.info(f"Récupération des services de l'utilisateur {id_utilisateur} via l'API")
    services = bd.services_compte(id_utilisateur)
    app.logger.debug(f"{len(services)} services récupérés pour l'utilisateur {id_utilisateur} via l'API")
    return jsonify(services)