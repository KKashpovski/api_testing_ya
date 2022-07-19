"""Tests for authorization."""


import pytest
import requests

URL = 'https://cloud-api.yandex.net/v1/disk/resources'
TOKEN = 'AQAAAABi9ZHkAADLW0-rdnVKD0HejLbuC_j2tnc'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}


@pytest.mark.parametrize("new_folder_name, copy_from, copy_to, moved_from, moved_to",
                         [("new_folder", "/Файл_для_копирования.jpeg", "/new_folder/Файл_для_копирования.jpeg",
                          "/new_folder/Файл_для_копирования.jpeg", "/new_folder/my_file.jpeg")])
class TestCloudPage:
    def test_move_file(self, new_folder_name, copy_from, copy_to, moved_from, moved_to):
        """
        Steps.

            1. Try to auth user with valid data
            2. Create new folder
            3. Copy file to new folder
            4. Rename file in folder
            5. Check file name
            6. Check that status code is 200
            7. Check response body
            8. Sign out
        """
        create_folder = requests.put(f"{URL}?path={new_folder_name}", headers=headers)
        copied_file = requests.post(f"{URL}/copy?from={copy_from}&path={copy_to}", headers=headers)
        rename = requests.post(f"{URL}/move?from={moved_from}&path={moved_to}", headers=headers)
        assert create_folder.status_code == 201, "Check status code"
        assert copied_file.status_code == 201, "Check status code"
        assert rename.status_code == 201, "Check status code"
