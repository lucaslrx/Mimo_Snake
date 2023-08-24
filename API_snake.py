from flask import Flask, jsonify, request

app = Flask(__name__)


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "Fichier introuvable"
    except Exception as e:
        return str(e)


def write_to_file(file_path, new_content):
    try:
        with open(file_path, 'w') as file:
            file.write(new_content)
        return "Contenu du fichier mis à jour"
    except Exception as e:
        return str(e)


@app.route('/api/get_content', methods=['GET'])
def get_content():
    return jsonify(content=read_file("highscore.txt"))


@app.route('/api/update_content', methods=['POST'])
def update_content():
    data = request.get_json()
    new_content = data.get('new_content')
    result = write_to_file("highscore.txt", new_content)
    return jsonify(message=result)


app.run()
