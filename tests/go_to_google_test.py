import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def browser_context(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page

def go_to_google_test(page: Page) -> None:
    page.goto("https://www.google.com")

    search_field = page.get_by_label("Найти")
    search_field.fill("Автотесты")
    search_button = page.get_by_label("Поиск в Google")
    search_button.first.click()

    # Проверка отображения логотипа Google
    logo = page.get_by_title("Главная страница Google")
    expect(logo).to_be_visible()

    # Проверка результатов поиска
    page.wait_for_selector(".g", timeout=5000)
    results_locator = page.locator(".g")
    assert results_locator.count() > 0, "Результаты поиска отсутствуют"

    # Проверка количества страниц
    pagination_selector = "#botstuff table tr td a"
    page.wait_for_selector(pagination_selector, timeout=5000)
    pages_count = page.locator(pagination_selector).count()
    assert pages_count > 0, "Количество страниц равно 0"

    # Проверка наличия и работы кнопки "Очистить"
    clean_button = page.get_by_role("button", name="Очистить")
    assert clean_button.is_visible(), "Кнопка Очистить не отображается"
    clean_button.click()

    # Проверка очистки поля
    page.wait_for_function(
        "document.querySelector('textarea[aria-label=\"Найти\"]').value === ''",
        timeout=5000
    )
    value = search_field.input_value()
    assert value == "", "Поле не очищено"
