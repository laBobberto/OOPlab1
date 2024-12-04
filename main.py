from Wikipedia import WikipediaSearch


searcher = WikipediaSearch()

while True:
    query = input("\nВведите поисковый запрос (или 'выход' для завершения): ")
    if query.lower() == 'выход':
        print("Программа завершена.")
        break

    searcher.search(query)
    searcher.displayResults()

    try:
        choice = int(input("\nВведите номер статьи для открытия (или 0 для нового поиска): ")) - 1
        if choice != 0:
            searcher.openArticle(choice)
    except ValueError:
        print("Введите корректное число.")

