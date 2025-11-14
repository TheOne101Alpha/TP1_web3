"""
Connexion à la BD
"""

import types
import contextlib
import mysql.connector

@contextlib.contextmanager
def creer_connexion():
    """Pour créer une connexion à la BD"""
    conn = mysql.connector.connect(
        user="garneau",
        password="qwerty_123",
        host="127.0.0.1",
        database="services_particuliers",
        raise_on_warnings=True
    )

    # Pour ajouter la méthode getCurseur() à l'objet connexion
    conn.get_curseur = types.MethodType(get_curseur, conn)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def get_curseur(self):
    """Permet d'avoir les enregistrements sous forme de dictionnaires"""
    curseur = self.cursor(dictionary=True)
    try:
        yield curseur
    finally:
        curseur.close()


def get_compte(nom, mdp):
    """retourne l'id et le role de l'utilisateur en fonction de son nom et mot de passe"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT id_compte, role FROM compte WHERE' \
            ' nom=%(nom)s AND mdp=%(mdp)s',{'nom':nom, 'mdp':mdp})
            compte = curseur.fetchone()
            return compte
        
def add_compte(nom, mdp, role):
    """Ajoute un utilisateur à la base de données"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('INSERT IGNORE INTO compte FROM VALUES(NULL, %(nom)s,'
            '%(mdp)s,%(role)s)' ,{'nom':nom, 'mdp':mdp, 'role':role})
            conn.commit()


def get_comptes():
    """reto"""

    
def get_service(conn, id_service):
    """Retourne un service"""
    retour = []

    with conn.get_curseur() as curseur:
        curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ' \
        'ser.titre, ser.actif, ser.description, ser.cout,' \
        ' ser.localisation FROM services ser INNER JOIN' \
        ' categories cat ON cat.id_categorie = ser.id_categorie ' \
        'WHERE ser.id_service =%(id)s', {'id': id_service})
        retour = curseur.fetchone()
        
        return retour

def get_services():
    """Retourne tous les services de la bd"""
    with creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_service, (SELECT nom_categorie FROM " \
            "`categories` WHERE categories.id_categorie " \
            "= services.id_categorie), titre, localisation, " \
            "description FROM `services` ORDER BY services.date_creation")
            return curseur.fetchall()
