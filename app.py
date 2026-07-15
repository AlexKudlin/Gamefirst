# Этот файл запускает простой сайт для скачивания твоей игры

from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    """Главная страница"""
    return app.send_static_file('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.static_folder, filename, as_attachment=True)

if __name__ == '__main__':
    print("Сервер запущен!")
    app.run(host='0.0.0.0', port=8000, debug=False)
