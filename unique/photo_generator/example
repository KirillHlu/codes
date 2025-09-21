import json
import time
import base64
import os
from io import BytesIO
from PIL import Image

import requests


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline_id, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt  # Исправлено: убраны лишние фигурные скобки
            }
        }

        data = {
            'pipeline_id': (None, pipeline_id),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']
            elif data['status'] == 'FAIL':
                raise Exception("Generation failed")

            attempts -= 1
            time.sleep(delay)

        raise Exception("Timeout waiting for generation")

    def save_image(self, image_data, filename="generated_image.png"):
        """
        Сохраняет изображение из base64 данных в PNG файл
        """
        try:
            # Декодируем base64 строку
            if isinstance(image_data, list):
                image_data = image_data[0]  # Берем первое изображение если их несколько

            image_bytes = base64.b64decode(image_data)

            # Создаем изображение из байтов
            image = Image.open(BytesIO(image_bytes))

            # Сохраняем в PNG файл
            image.save(filename, "PNG")
            print(f"Изображение сохранено как {filename}")

            return filename

        except Exception as e:
            print(f"Ошибка при сохранении изображения: {e}")
            return None


if __name__ == '__main__':
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', '',
                         '')

    try:
        pipeline_id = api.get_pipeline()
        print(f"Pipeline ID: {pipeline_id}")

        uuid = api.generate("pig in sky шт ьщысщц", pipeline_id)
        print(f"Request UUID: {uuid}")

        files = api.check_generation(uuid)

        if files:
            # Создаем имя файла с временной меткой
            timestamp = int(time.time())
            filename = f"generated_image_{timestamp}.png"

            # Сохраняем изображение
            saved_file = api.save_image(files, filename)

            if saved_file:
                print(f"Изображение успешно сохранено в файл: {saved_file}")
            else:
                print("Не удалось сохранить изображение")
        else:
            print("Не удалось получить изображение")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
