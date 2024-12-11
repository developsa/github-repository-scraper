# GitHub Login Automation Project

 This project is a Python application that automates the login process to GitHub and fetches repository information using Selenium and BeautifulSoup. The user provides their GitHub username and password, and the program attempts to log in to GitHub. Upon successful login, it retrieves the user's repositories and writes the information to a CSV file.

## Features
- Automated Login: Logs into GitHub using the username and password provided by the user.
- Repository Information Retrieval: After login, the program fetches the user's repositories, including their name, programming language, and the last updated date.
- CSV Output: Writes the repository information to a CSV file.
- Error Handling: Informs the user if the login fails and prints the corresponding error message.

## Libraries Used

- `selenium`: Used for automating the login process and navigating GitHub's web interface.
- `beautifulsoup4`: Used for scraping repository information from the HTML of the page.
- `requests`: Used to send HTTP requests and fetch the repository page's HTML.
- `csv`: Used for writing the fetched data to a CSV file.
- `dotenv`: Loads environment variables (e.g., user-agent) from a .env file to make the script more configurable.

## Installation

1. Ensure Python 3 and pip are installed.
2. Install the necessary libraries: Run the following command in the project directory to install the required Python libraries:
   ```bash
   pip install -r requirements.txt
3. Create a .env file:In the project directory, create a .env file with the following content (replace with your actual user-agent string):
   ```bash
   USER_AGENT=your_user_agent_string_here
4. Run the project:
   ```bash
   python main.py


