# Importation des classes nécessaires depuis le module Flask
from flask import Flask, jsonify, request

# Création d'une instance de l'application Flask
app = Flask(__name__)

# Fonction pour lire le contenu d'un fichier
def read_file(file_path):
    try:
        # Tentative d'ouverture du fichier en mode lecture ('r')
        with open(file_path, 'r') as file:
            # Lecture du contenu du fichier
            content = file.read()
            return content
    except FileNotFoundError:
        # Gestion de l'erreur si le fichier n'est pas trouvé
        return "Fichier introuvable"
    except Exception as e:
        # Gestion d'autres erreurs et renvoi de la description de l'erreur
        return str(e)

# Fonction pour écrire dans un fichier
def write_to_file(file_path, new_content):
    try:
        # Tentative d'ouverture du fichier en mode écriture ('w')
        with open(file_path, 'w') as file:
            # Écriture du nouveau contenu dans le fichier
            file.write(new_content)
        return "Contenu du fichier mis à jour"
    except Exception as e:
        # Gestion d'erreurs et renvoi de la description de l'erreur
        return str(e)

# Route API pour obtenir le contenu du fichier
@app.route('/api/get_content', methods=['GET'])
def get_content():
    # Appel de la fonction read_file pour obtenir le contenu du fichier
    return jsonify(content=read_file("highscore.txt"))

# Route API pour mettre à jour le contenu du fichier
@app.route('/api/update_content', methods=['POST'])
def update_content():
    # Récupération des données JSON de la requête
    data = request.get_json()
    # Récupération du nouveau contenu à partir des données
    new_content = data.get('new_content')
    # Appel de la fonction write_to_file pour mettre à jour le contenu du fichier
    result = write_to_file("highscore.txt", new_content)
    # Renvoi d'une réponse JSON avec le résultat de la mise à jour
    return jsonify(message=result)

# Démarrage de l'application Flask et mise en attente de requêtes
app.run()
