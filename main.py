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
load_dotenv()

class Github:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome()
        self.url = "https://github.com/"
        self.username = username
        self.password = password
        self.sign_in_successful = False

    def signIn(self):
        self.browser.get(self.url + "login")

        # Wait for the username input field to appear and enter the username
        username_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        username_input.send_keys(self.username)

        # Wait for the password input field to appear and enter the password
        password_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(self.password)

        # Wait for the login button to become clickable and click it
        submit = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.NAME, "commit"))
        )
        submit.click()

        # If login fails, capture and print the error message
        try:
            flash_error = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flash-error"))
            )
            error_message = flash_error.find_element(By.CLASS_NAME, "js-flash-alert").text.strip()
            print(f"Error: {error_message}")
            self.browser.quit()
        except Exception:
            # If login succeeds, print a success message
            print("Success: Login successful.")
            self.sign_in_successful = True
        time.sleep(4)

    def getRepository(self):
        # If login was not successful, do not proceed
        if not self.sign_in_successful:
            print("Repository data could not be fetched as login failed.")
            return

        # Wait for the navigation menu to become clickable and open it
        navigation_menu = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Open user navigation menu']"))
        )
        navigation_menu.click()
        time.sleep(3)

        # Wait for the "Your repositories" link to become clickable and click it
        your_repositories_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Your repositories')]"))
        )
        your_repositories_link.click()
        time.sleep(5)

        # Get the current URL to fetch the repository list
        current_url = self.browser.current_url
        params = {
            # Set a user-agent header for the HTTP request
            "user-agent": os.getenv("USER_AGENT")
        }
        response = requests.get(current_url, headers=params)
        soup = BeautifulSoup(response.text, "html.parser")

        # Parse repository information
        repositories = []
        div_id_ul_lis = soup.find("div", {"id": "user-repositories-list"}).find("ul").find_all("li")
        for list in div_id_ul_lis:
            # Get repository name
            text = list.h3.a.get_text().strip()

            # Get repository language (if available)
            language_span = list.find(class_="f6").find('span', {'itemprop': 'programmingLanguage'})
            language = language_span.get_text() if language_span else "Other"

            # Get the last updated date
            updated_date = list.find(class_="f6").find("relative-time").get_text().strip()
            repositories.append([text, language, updated_date])

        # Write repository information to a CSV file
        self.write_file(repositories)
        time.sleep(5)
        self.browser.close()

    def write_file(self, repositories):
        try:
            # Open a CSV file and write the repository data
            with open('my_repositories.csv', 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Name', 'Language', 'Updated Date'])

                # Write each repository's details into the file
                csv_writer.writerows(repositories)

            print("CSV file successfully written.")
        except Exception as e:
            print(f"An error occurred: {e}")


# Prompt the user for their GitHub username and password
username = input("Enter your github username: ")
password = input("Enter your github password: ")

# Create a Github object and execute login and repository fetching
github = Github(username, password)
github.signIn()
github.getRepository()
