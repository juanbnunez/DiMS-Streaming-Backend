from flask import Flask, jsonify
from flask_cors import CORS
from Content import Content

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas

content_manager = Content()

@app.route('/get-media', methods=['GET'])
def get_media():
    """
    Endpoint para obtener los archivos agrupados de S3.
    Retorna un JSON con el nombre, la URL de la imagen y la URL de audio o video.
    """
    try:
        # Obtener los archivos agrupados por nombre base
        grouped_files = content_manager.group_s3_objects_by_name()

        # Convertir los datos a un formato más adecuado para el frontend
        media_data = []
        for name, files in grouped_files.items():
            media_data.append({
                'name': name,
                'image_url': files.get('image'),
                'audio_url': files.get('audio')
            })
        return jsonify(media_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Manejo de errores

# El punto de entrada de Flask es ahora la función app

