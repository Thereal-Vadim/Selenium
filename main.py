from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WikiExplorer:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://ru.wikipedia.org")

    def search_article(self, query):
        search_box = self.driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

    def get_paragraphs(self):
        paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
        return [p for p in paragraphs if p.text.strip()]

    def get_internal_links(self):
        content_div = self.driver.find_element(By.ID, "mw-content-text")
        links = content_div.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")
        return [(link.text, link.get_attribute("href")) for link in links if link.text.strip()]

    def browse_paragraphs(self):
        paragraphs = self.get_paragraphs()
        current_paragraph = 0

        while True:
            if 0 <= current_paragraph < len(paragraphs):
                print("\nТекущий параграф:")
                print(paragraphs[current_paragraph].text)

                action = input("\nДействия:\n"
                               "n - следующий параграф\n"
                               "p - предыдущий параграф\n"
                               "b - вернуться к главному меню\n"
                               "Выберите действие: ")

                if action == 'n':
                    current_paragraph += 1
                elif action == 'p':
                    current_paragraph -= 1
                elif action == 'b':
                    break
            else:
                print("Достигнут конец статьи")
                current_paragraph = len(paragraphs) - 1

    def browse_links(self):
        while True:
            links = self.get_internal_links()
            print("\nДоступные ссылки:")
            for i, (text, _) in enumerate(links[:10]):
                print(f"{i + 1}. {text}")

            choice = input("\nВыберите номер ссылки (или 'b' для возврата): ")
            if choice == 'b':
                break

            try:
                index = int(choice) - 1
                if 0 <= index < len(links):
                    self.driver.get(links[index][1])
                    self.article_menu()
                else:
                    print("Неверный номер ссылки")
            except ValueError:
                print("Пожалуйста, введите число")

    def article_menu(self):
        while True:
            choice = input("\nМеню статьи:\n"
                           "1. Читать параграфы\n"
                           "2. Перейти по ссылкам\n"
                           "3. Вернуться к поиску\n"
                           "Выберите действие: ")

            if choice == '1':
                self.browse_paragraphs()
            elif choice == '2':
                self.browse_links()
            elif choice == '3':
                break

    def run(self):
        try:
            while True:
                query = input("\nВведите поисковый запрос (или 'q' для выхода): ")
                if query.lower() == 'q':
                    break

                self.search_article(query)
                self.article_menu()

        finally:
            self.driver.quit()


if __name__ == "__main__":
    explorer = WikiExplorer()
    explorer.run()