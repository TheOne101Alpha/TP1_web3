"""
Connexion à la BD
"""
import hashlib
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
    """retourne le l'id et le role et le crédit de l'utilisateur en fonction de son nom et mot de passe"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT id_compte, role, credit FROM compte WHERE nom=%(nom)s AND mdp=%(mdp)s',{'nom':nom, 'mdp':mdp})
            compte = curseur.fetchone()
            return compte
        
def add_compte(nom, mdp, role):
    """Ajoute un utilisateur à la base de données"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('INSERT IGNORE INTO compte VALUES(NULL, %(nom)s,'
            '%(mdp)s,%(role)s, 0)' ,{'nom':nom, 'mdp':mdp, 'role':role})
            conn.commit()


def get_comptes():
    """retournes tous les comptes dans la base de données"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            unevar = 'admin@garneau.ca'
            curseur.execute('SELECT * FROM compte WHERE `nom` != %(nom)s', {'nom': unevar})
            comptes = curseur.fetchall()
            return comptes

def delete_compte(id_compte):
    """supprime un compte dans la base de données"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('DELETE FROM compte WHERE `id_compte` = %(id)s', {'id': id_compte})
            conn.commit()

def id_exist(id_compte):
    """retourne un bool si le compte existe ou non"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT * FROM compte WHERE id_compte=%(id)s',{'id':id_compte})
            compte = curseur.fetchone()
            if compte:
                return True
            return False

def services_compte(id_compte):
    """retourne tous les services du compte si il n'est pas admin"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT * FROM service WHERE id_compte=%(id)s',{'id':id_compte})
            compte = curseur.fetchone()
            if compte:
                return True
            return False

def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()

def get_service(id_service):
    """retourne un service en particulier"""
    retour = []

    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:

            curseur.execute('SELECT ser.id_service, cat.nom_categorie, ser.date_creation, ' \
            'ser.titre, ser.actif, ser.description, ser.cout, ser.proprietaire,' \
            ' ser.localisation, ser.locataire FROM services ser INNER JOIN' \
            ' categories cat ON cat.id_categorie = ser.id_categorie ' \
            'WHERE ser.id_service =%(id)s', {'id': id_service})
            retour = curseur.fetchone()

    return retour

def get_services():
    """Retourne tous les services disponibles"""

    retour = []
    with creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_service, (SELECT nom_categorie FROM " \
            "`categories` WHERE categories.id_categorie " \
            "= services.id_categorie), titre, localisation, " \
            "description FROM `services` ORDER BY services.date_creation")
            retour = curseur.fetchall()

    return retour

def add_service(nom, description, localisation, date, categorie, actif, cout):
    """Permet d'ajouter un service"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute(
                'INSERT INTO services VALUES (NULL,%(categorie_id)s,%(letitre)s,'
                '%(ladescription)s,%(lalocalisation)s,%(ladate)s,'
                '%(si_actif)s,%(lecout)s, NULL)',
                {
                    'letitre': nom,
                    'ladescription': description,
                    'lalocalisation': localisation,
                    'ladate': date,
                    'categorie_id': categorie,
                    'si_actif': actif,
                    'lecout': cout,
                }
            )
            conn.commit()
            return True

    return False

def get_categories():
    """Retourne toutes les catégories"""
    with creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_categorie, nom_categorie FROM categories")
            return curseur.fetchall()

def delete_service(id_service):
    """supprime un compte dans la base de données"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('DELETE FROM services WHERE `id_service` = %(id)s', {'id': id_service})
            conn.commit()

def update_service(id_change, nom, description, localisation, actif, cout, date):
    """Permet de modifier un service en particulier"""
    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute(
                'UPDATE services SET titre= %(letitre)s, description= %(ladescription)s, ' \
                'localisation= %(lalocalisation)s,date_creation= %(ladate)s' \
                ', actif= %(si_actif)s,cout= %(lecout)s WHERE id_service = %(ident)s',
                {
                    'letitre': nom,
                    'ladescription': description,
                    'lalocalisation': localisation,
                    'si_actif': actif,
                    'lecout': cout,
                    'ladate': date,
                    'ident': id_change
                }
            )
            conn.commit()

def book_service(id_service, id_locataire):
    """Permet de réserver un service dans la bd"""

    with creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute(
                'UPDATE services SET locataire = %(compte)s '  \
                ' WHERE id_service = %(ident)s',
                {
                    'ident': id_service,
                    'compte': id_locataire
                }
            )
            conn.commit()
