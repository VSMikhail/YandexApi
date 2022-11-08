import requests

download_link = 'https://cloud-api.yandex.net/v1/disk/resources/download'
upload_link = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
files_link = 'https://cloud-api.yandex.net/v1/disk/resources/files'
token = ''


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    @property
    def header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files(self):
        resp = requests.get(files_link, headers=self.header)
        return resp.json()

    def ya_upload_link(self, file_path: str):
        params = {'path': file_path, 'overwrite': 'true'}
        responce = requests.get(upload_link, headers=self.header, params=params)
        upload_url = responce.json().get('href')
        return upload_url

    def upload_list(self, files_list):
        for file in files_list:
            upload_link = self.ya_upload_link(file)
            if upload_link:
                with open(file, 'rb') as file_obj:
                    resp = requests.put(upload_link, data=file_obj, params={'overwrite': 'true'})
                    if resp.status_code == 201:
                        print('Файл загружен успешно со статус-кодом: 201')
            else:
                print('Ссылка на загрузка не существует')

inst = YaUploader(token)
file_list = []

for file_number in range(1, 6):
    file_name = 'text_' + str(file_number) + '.txt'
    file_list.append(file_name)
    with open(file_name, 'w') as f:
        f.write('File_' + str(file_number))

inst.upload_list(file_list)
