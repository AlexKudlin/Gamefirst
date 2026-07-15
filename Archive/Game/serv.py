from flask import Flask, send_from_directory

# Создаем приложение
app = Flask(__name__)

@app.route('/')
def home():
    """Главная страница"""
    return app.send_static_file('index.html')

# Эта функция позволяет скачать архив с игрой
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.static_folder, filename, as_attachment=True)

if __name__ == '__main__':
    print("Сервер запущен!")
    app.run(debug=False)  # Отключаю дебаг, чтобы не было лишних сообщений