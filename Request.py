from flask import Flask, jsonify
from flask_cors import CORS
from Content import Content
import time

class Request:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # Permitir CORS para todas las rutas
        self.content_manager = Content()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/get-media', methods=['GET'])
        def get_media():
            """
            Endpoint para obtener los archivos agrupados de S3.
            Retorna un JSON con el nombre, la URL de la imagen y la URL de audio o video.
            """
            try:
                start_time = time.time()
                # Obtener los archivos agrupados por nombre base
                grouped_files = self.content_manager.group_s3_objects_by_name()

                # Convertir los datos a un formato más adecuado para el frontend
                media_data = []
                for name, files in grouped_files.items():
                    media_data.append({
                        'name': name,
                        'image_url': files.get('image'),
                        'audio_url': files.get('audio')
                    })
                
                end_time = time.time()  # Detiene el temporizador
                duration = end_time - start_time
                print(f"Tiempo de carga en el backend: {duration:.4f} segundos")  # Muestra el informe en consola

                return jsonify(media_data), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500  # Manejo de errores

    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=5000)  # Iniciar el servidor

if __name__ == '__main__':
    app = Request()
    app.run()
