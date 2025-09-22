from flask import Flask, render_template

SITENOM = 'Services'

app = Flask(__name__)

@app.route('/')
def base():
    """Affiche la page d'aceuil du site"""
    return render_template('base.jinja', titre=SITENOM)



if __name__ == "__main__":
    app.run()
