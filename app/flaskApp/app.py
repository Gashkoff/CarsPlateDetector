import os
from flask import Flask, render_template, request
from common.logger import logger
from werkzeug.utils import secure_filename
from config.configs import *
import requests as req


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = VIDEO_PATH


def allowed_file(filename: str) -> bool:
    """Checking the video extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video_with_yolo(video: str) -> (str, str):
    """Processes the requested video and sends recognized numbers and videos with objects."""
    response = ''
    try:
        response = req.post(YOLO_URL, json={"video_name": video})
        response.raise_for_status()

    except req.exceptions.RequestException as e:
        status_code = response.status_code if response.status_code else "Неизвестен"
        error_detail = response.json()['detail'] if response.json()['detail'] else "Ответ отсутствует"
        logger.error(f"Ошибка при запросе к FastAPI: {e}")
        return '', f'Bad response\n Код ошибки:{status_code}\n Детали:{error_detail}'

    except Exception as _ax:
        logger.error(f"Другая ошибка при запросе к FastAPI: {_ax}")
        return '', 'Сервер не отвечает'

    message = response.json()
    return message['symbols'], message['error_message']

def delete_folder():
    """Delete last videos."""
    try:
        for filename in os.listdir(VIDEO_PATH):
            file_path = os.path.join(VIDEO_PATH, filename)
            os.remove(file_path)

    except OSError as _ex:
        logger.error(f"Ошибка очистки директории с видео - {_ex}")
        return _ex

@app.route('/', methods=['GET', 'POST'])
def index():
    detected_numbers = ""
    processed_video = None
    err_msg = None

    if request.method == 'POST':
        logger.info("Получен запрос от пользователя")

        err = delete_folder()
        if err:
            err_msg = "С сервером беда"

        if 'video' in request.files:
            file = request.files['video']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                try:
                    file.save(filepath)
                    logger.info(f"Файл сохранён: {filepath}")
                    detected_numbers, err_msg = process_video_with_yolo(filename)

                    if not err_msg:
                        processed_video = 'processing_video.MOV'

                except Exception as e:
                    logger.error(f"Ошибка сохранения файла: {e}")

    return render_template('main.html', video_filename=processed_video,
                           numbers=detected_numbers, error_message=err_msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)