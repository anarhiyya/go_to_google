from playwright.sync_api import sync_playwright, expect

def test_google_search() -> None:
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        search_button = page.get_by_label("Поиск в Google")

        # Переход в браузер, ввод ключевого слова и клик по кнопке поиска:
        page.goto("https://www.google.com")
        page.get_by_label("Найти").fill("Автотесты")
        search_button.first.click()

        # Поиск элемента по его тайтлу и ожидание отображения логотипа
        logo = page.get_by_title('Главная страница Google')
        expect(logo).to_be_visible(), "Логотип Google не отображается"

        # Проверка, что количество результатов поиска на странице не равно 0
        page.wait_for_selector(".g", timeout=1000)
        results_locator = page.locator(".g")
        assert results_locator.count() > 0, "Результатов поиска нет на первой странице"

        # Проверка, что количество страниц не равно 0
        pagination_selector = "#botstuff table tr td a"
        page.wait_for_selector(pagination_selector, timeout=1000)
        pages_count = page.locator(pagination_selector).count()
        assert pages_count > 0, "Количество страниц равно 0"

        # Проверка наличия кнопки "Очистить" + нажатие по ней
        clean_button = page.get_by_role("button", name="Очистить")
        assert clean_button.is_visible(), "Кнопка Очистить не отображается"
        clean_button.click()

        # Проверка, что поле действительно очищено
        page.wait_for_function(
            "document.querySelector('textarea[aria-label=\"Найти\"]').value === ''",
            timeout=5000
        )
        value = page.get_by_label("Найти").input_value()
        assert value == "", f"Поле не очищено, текущее значение: {value}"

        browser.close()
