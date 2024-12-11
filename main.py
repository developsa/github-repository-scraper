from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import csv
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


class Github:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()
        self.url = "https://github.com/"
        self.sign_in_successful = False

    def wait_for_element(self, by, value, timeout=10):
        """Helper method for WebDriverWait"""
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def sign_in(self):
        """Sign in to GitHub"""
        self.browser.get(self.url + "login")

        # Enter username and password
        self.wait_for_element(By.NAME, "login").send_keys(self.username)
        self.wait_for_element(By.NAME, "password").send_keys(self.password)

        # Click the sign-in button
        self.wait_for_element(By.NAME, "commit").click()

        # If login fails, capture and print the error message
        try:
            flash_error = self.wait_for_element(By.CLASS_NAME, "flash-error")
            error_message = flash_error.find_element(By.CLASS_NAME, "js-flash-alert").text.strip()
            print(f"Error: {error_message}")
            self.browser.quit()
        except Exception:
            print("Success: Login successful.")
            self.sign_in_successful = True
        time.sleep(2)

    def get_repository(self):
        """Fetch repository data from GitHub"""
        if not self.sign_in_successful:
            print("Repository data could not be fetched as login failed.")
            return

        # Open the user navigation menu and navigate to repositories
        self.wait_for_element(By.CSS_SELECTOR, "button[aria-label='Open user navigation menu']").click()
        time.sleep(2)
        self.wait_for_element(By.XPATH, "//span[contains(text(), 'Your repositories')]").click()
        time.sleep(5)

        # Fetch repository data
        current_url = self.browser.current_url
        response = self.fetch_page(current_url)
        soup = BeautifulSoup(response, "html.parser")

        # Parse repository data
        repositories = self.parse_repositories(soup)
        self.write_file(repositories)

        self.browser.quit()

    def fetch_page(self, url):
        """Send an HTTP request to fetch the page"""
        headers = {
            "User-Agent": os.getenv("USER_AGENT")
        }
        response = requests.get(url, headers=headers)
        return response.text

    def parse_repositories(self, soup):
        """Parse repository information"""
        repositories = []
        div_id_ul_lis = soup.find("div", {"id": "user-repositories-list"}).find("ul").find_all("li")

        for list in div_id_ul_lis:
            text = list.h3.a.get_text().strip()
            language_span = list.find(class_="f6").find('span', {'itemprop': 'programmingLanguage'})
            language = language_span.get_text() if language_span else "Other"
            updated_date = list.find(class_="f6").find("relative-time").get_text().strip()
            repositories.append([text, language, updated_date])

        return repositories

    def write_file(self, repositories):
        """Write repository data to a CSV file"""
        try:
            with open('my_repositories.csv', 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Name', 'Language', 'Updated Date'])
                csv_writer.writerows(repositories)
            print("CSV file successfully written.")
        except Exception as e:
            print(f"An error occurred: {e}")


# Prompt the user for their GitHub username and password
username = input("Enter your github username: ")
password = input("Enter your github password: ")

# Create a Github object and execute login and repository fetching
github = Github(username, password)
github.sign_in()
github.get_repository()
