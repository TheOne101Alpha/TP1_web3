import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, Blueprint, session, url_for, flash, jsonify
import bd

bp_api = Blueprint('api', __name__)

@bp_api.route('/services/all', methods=['GET'])
def get_all_services():
    """Retourne tous les services en format JSON"""
    services = bd.get_services()
    retour = []
    for item in services:
        service = dict(id=item["id_service"], titre = item['titre'])
        retour.append(service)
    print(retour)
    return jsonify(retour)

@bp_api.route('/services/all_details', methods=['GET'])
def get_all_services_details():
    """Retourne tous les services en format JSON"""
    services = bd.get_services()
    return jsonify(services)

@bp_api.route('/Compte/all_mail', methods=['GET'])
def get_all_mail():
    """Retourne tous les mails dans la BD pour les comparer"""
    comptes = bd.get_comptes()
    retour = []
    for item in comptes:
        retour.append(item["nom"])
    print(retour)
    return jsonify(retour)

@bp_api.route('/compte/all', methods=['GET'])
def get_all():
    """Retourne tous les mails dans la BD pour les comparer"""
    comptes = bd.get_comptes()
    return jsonify(comptes)

@bp_api.route('/compte/supprimer/<int:id_compte>', methods=['GET'])
def supp_compte(id_compte):
    """Retourne tous les mails dans la BD pour les comparer"""
    retour = bd.delete_compte(id_compte)
    return jsonify(retour)

@bp_api.route('/reservation/check_date/<int:id_service>', methods=['GET'])
def check_date(id_service):
    """ Retourne la disponibilité d'un service"""
    service = bd.get_service(id_service)
    print(bool(service.get('locataire') is None))
    return jsonify(bool(service.get('locataire') is None))