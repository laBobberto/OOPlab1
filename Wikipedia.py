import requests
import webbrowser
import urllib.parse
from typing import List

class WikipediaResult:
    """Класс для представления результата поиска."""
    def __init__(self, title: str, snippet: str, pageid: int):
        self.title = title
        self.snippet = snippet
        self.pageid = pageid

    def getUrl(self) -> str:
        """Генерирует URL для открытия статьи."""
        return f"https://ru.wikipedia.org/w/index.php?curid={self.pageid}"

    def __str__(self) -> str:
        """Возвращает текстовое представление результата."""
        return f"Заголовок: {self.title}\nСниппет: {self.snippet}\nСсылка: {self.getUrl()}"


class WikipediaSearch:
    """Класс для выполнения поиска по Википедии."""
    BASE_URL = "https://ru.wikipedia.org/w/api.php"

    def __init__(self):
        self.results: List[WikipediaResult] = []

    def search(self, query: str):
        """Выполняет поиск по запросу."""
        encoded_query = urllib.parse.quote(query)
        params = {
            "action": "query",
            "list": "search",
            "utf8": "",
            "format": "json",
            "srsearch": encoded_query
        }
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            self._parseResults(data)
        else:
            print(f"Ошибка: {response.status_code} - {response.reason}")

    def _parseResults(self, data: dict):
        """Парсит результаты поиска."""
        self.results = []
        search_results = data.get("query", {}).get("search", [])
        for item in search_results:
            title = item.get("title", "Без названия")
            snippet = item.get("snippet", "Описание отсутствует").replace('<span class="searchmatch">', '').replace('</span>', '')
            pageid = item.get("pageid", 0)
            self.results.append(WikipediaResult(title, snippet, pageid))

    def displayResults(self):
        """Выводит результаты поиска в консоль."""
        if not self.results:
            print("Ничего не найдено.")
        else:
            for i, result in enumerate(self.results, start=1):
                print(f"{i}. {result.title} ({result.getUrl()})")

    def openArticle(self, index: int):
        """Открывает выбранную статью в браузере."""
        if 0 < index < len(self.results):
            url = self.results[index].getUrl()
            webbrowser.open(url)
        else:
            print("Неверный номер статьи.")
