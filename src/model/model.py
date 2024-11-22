from enum import StrEnum
import dotenv
import requests
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TargetData():

    class Targets(StrEnum):
        MOCKDATA = 'mock'
        REALDATA = 'real'

    BASE_URL = "https://www.tabnews.com.br/api/v1/"
    MOCK_PATH = "../mockdata"

    def __init__(self) -> None:
        self.url_complement = None
        self.mock_complement = None
        pass

    def op_remote(self) -> list:
        response = requests.get(f"{TargetData.BASE_URL}{self.url_complement}")
        json_content = response.json()
        self.write_file(json.dumps(json_content))
        return json_content

    def write_file(self, content: str):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_fullpath = f"{current_directory}/{TargetData.MOCK_PATH}/{self.mock_complement}"
            file = open(file_fullpath, "w", encoding="utf8")
            file.write(content)
        except Exception as e:
            logging.error(f"Error {e}")


    def op_mock(self) -> list:
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_fullpath = f"{current_directory}/{TargetData.MOCK_PATH}/{self.mock_complement}"
            logging.debug(f"Opening file {file_fullpath}")
            with open(file_fullpath, encoding="utf8") as file:
                json_content = json.load(file)
            if len(json_content) == 0:
                logging.debug("no data on the file")
                return []            
            return json_content
        except FileNotFoundError:
            logging.debug("File not found")
            return []


class Retrieve(TargetData):
    def __init__(self) -> None:
        super(Retrieve, self).__init__()
        self.target:TargetData.Targets = os.getenv("TARGET")

    def operation(self):
        if self.target == TargetData.Targets.MOCKDATA:
            return self.op_mock()
        elif self.target == TargetData.Targets.REALDATA:
            return self.op_remote()
        else: 
            return []


class MainPageContent(Retrieve):
    def __init__(self) -> None:
        super(MainPageContent, self).__init__()
        self.url_complement = "contents?page=1&per_page=100"
        self.mock_complement = "content.json"
   
class PostDescription(Retrieve):
    def __init__(self, user:str, slug: str) -> None:
        super(PostDescription, self).__init__()
        self.url_complement = f"contents/{user}/{slug}"
        self.mock_complement = f"content_{user}_{slug}.json"
