import argparse
import logging
from enum import Enum
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_SLEEP_TIME, DEFAULT_WAIT_TIME, SONG_NAME, URL
from utils import generate_valid_email, generate_valid_password, get_random_display_name

logger = logging.getLogger(__name__)


class BrowserTypes(Enum):
    FIREFOX = "firefox"
    EDGE = "edge"
    CHROME = "chrome"


class SpotifyBot:
    SELECTORS = {
        "signup_button": "//button[normalize-space()='Sign up']",
        "login_button": "(//button[@data-testid='login-button'])[1]",
        "email_input": "username",
        "signup_email_next_button": "/html/body/div[1]/main/main/section/div/form/button/span[1]",
        "signup_password_next_button": "//span[contains(@class, 'encore-bright-accent-set')]",
        "password_input": "new-password",
        "set_gender_male": "//span[@class='Indicator-sc-hjfusp-0 jRuGOG']",
        "name_final_next_button": "//span[contains(@class, 'encore-bright-accent-set')]",
        "search_input": "//input[@placeholder='What do you want to play?'][1]",
        "add_to_playlist_button": "(//button[@aria-label='Add to Playlist'][normalize-space()='Add'])[1]",
        "close_menu_button": "//*[@id='Desktop_LeftSidebar_Id']/nav/div/div[1]/div[1]/header/div/div[1]/button",
        "logout_button": "//button[@data-testid='user-widget-dropdown-logout']",
        "home_button": "/html/body/div[4]/div/div[2]/div[1]/div[2]/div/button/span",
        "create_new_playlist_button": "(//button[@class='Button-sc-qlcn5g-0 iPAIAO encore-text-body-small-bold e-9541-button-primary e-9541-button'])[2]",
        "play_button": "(//span[@class='IconWrapper__Wrapper-sc-1hf1hjl-0 ivomLs'])[1]",

    }

    def __init__(
        self, browser: BrowserTypes = BrowserTypes.FIREFOX, wait_time: int = DEFAULT_WAIT_TIME, song: str = SONG_NAME
    ):
        """Initialize Spotify bot with specified browser and wait time.

        Args:
            browser: Browser type to use
            wait_time: Default wait time for elements in seconds
        """
        logger.info(f"Initializing Spotify bot with {browser} browser, it may take a while to download the driver ...")
        if browser == BrowserTypes.FIREFOX:
            options = webdriver.FirefoxOptions()
            options.set_preference("media.eme.enabled", True)
            options.set_preference("media.gmp-manager.updateEnabled", True)
            self.driver = webdriver.Firefox(
                options=options,
                service=webdriver.FirefoxService(
                    log_output="firefox.log",
                ),
            )
            logger.info("Firefox driver initialized")

        elif browser == BrowserTypes.EDGE:
            options = webdriver.EdgeOptions()
            self.driver = webdriver.Edge(
                options=options,
                service=webdriver.EdgeService(
                    log_output="edge.log",
                ),
            )
            logger.info("Edge driver initialized")

        elif browser == BrowserTypes.CHROME:
            options = webdriver.ChromeOptions(
                # min
            )
            options.add_argument("--enable-media-session-64-bit")
            self.driver = webdriver.Chrome(
                options=options,
                service=webdriver.ChromeService(
                    log_output="chrome.log",
                ),
            )
            logger.info("Chrome driver initialized")

        self.wait = WebDriverWait(self.driver, wait_time)
        self.driver.maximize_window()
        self.user_email = generate_valid_email()
        self.user_password = generate_valid_password()
        self.user_display_name = get_random_display_name()
        self.song = song

        logger.info(f"User email: {self.user_email}")
        logger.info(f"User password: {self.user_password}")
        logger.info(f"User display name: {self.user_display_name}")

    def wait_and_click(self, by: By, value: str, max_retries: int = 3) -> None:
        """Wait for element to be clickable and click it with retry logic.

        Args:
            by: Selenium By selector
            value: Selector value
            max_retries: Maximum number of retry attempts
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Waiting for element to be clickable: {value} (attempt {attempt + 1})")
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to click element after {max_retries} attempts: {e}")
                    raise
                sleep(DEFAULT_SLEEP_TIME)

    def wait_and_send_keys(self, by: By, value: str, keys: str, max_retries: int = 3) -> None:
        """Wait for element to be present and send keys with retry logic.

        Args:
            by: Selenium By selector
            value: Selector value
            keys: Keys to send
            max_retries: Maximum number of retry attempts
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Waiting for element to be present: {value} (attempt {attempt + 1})")
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                element.send_keys(keys)
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to send keys after {max_retries} attempts: {e}")
                    raise
                sleep(DEFAULT_SLEEP_TIME)

    def signup(self) -> None:
        logger.info("Navigating to Spotify")
        self.driver.get(URL)
        logger.info("Clicking sign up")
        self.wait_and_click(By.XPATH, self.SELECTORS["signup_button"])
        logger.info("Sending keys to email")
        sleep(3)
        self.wait_and_send_keys(By.ID, self.SELECTORS["email_input"], self.user_email)
        sleep(3)
        self.wait_and_click(By.XPATH, self.SELECTORS["signup_email_next_button"])
        logger.info("Sending keys to password")
        self.wait_and_send_keys(By.ID, self.SELECTORS["password_input"], self.user_password)
        sleep(3)
        self.wait_and_click(By.XPATH, self.SELECTORS["signup_password_next_button"])

        # Fill in profile details
        self.wait_and_send_keys(By.ID, "displayName", self.user_display_name)
        self.wait_and_send_keys(By.ID, "day", "15")
        Select(self.driver.find_element(By.ID, "month")).select_by_index(5)
        self.wait_and_send_keys(By.ID, "year", "2000")

        # Complete signup
        self.wait_and_click(By.XPATH,  self.SELECTORS["set_gender_male"])
        self.wait_and_click(By.XPATH, self.SELECTORS["name_final_next_button"])
        self.wait_and_click(By.XPATH, self.SELECTORS["name_final_next_button"])

    def logout(self) -> None:
        self.wait_and_send_keys(By.XPATH, "//div/form/div[2]/input", "a")
        sleep(3)
        self.wait_and_click(By.XPATH, "//div[2]/div/button/span")
        sleep(1)
        self.wait_and_click(By.XPATH, "//div[3]/button[2]")
        sleep(1)
        self.wait_and_click(By.XPATH, self.SELECTORS["logout_button"])

    def login(self) -> None:
        self.wait_and_click(By.XPATH, "//button[@data-testid='login-button']")
        self.wait_and_send_keys(By.ID, "login-username", self.user_email)
        self.wait_and_send_keys(By.ID, "login-password", self.user_password)
        self.wait_and_click(By.XPATH, self.SELECTORS["name_final_next_button"])

    def search_and_add_to_playlist(self) -> None:
        logger.info("Searching and adding to playlist")
        self.wait_and_send_keys(By.XPATH, self.SELECTORS["search_input"], "a")
        sleep(3)
        self.wait_and_click(By.XPATH, self.SELECTORS["home_button"])

        # Check and handle menu visibility
        menu = self.driver.find_elements(By.XPATH, self.SELECTORS["create_new_playlist_button"])
        if not menu:
            self.wait_and_click(By.XPATH, self.SELECTORS["close_menu_button"])

        self.wait_and_click(By.XPATH, self.SELECTORS["create_new_playlist_button"])
        sleep(1)
        self.wait_and_send_keys(By.XPATH, "(//input[@placeholder='Search for songs or episodes'])[1]", self.song)
        sleep(1)
        self.wait_and_click(By.XPATH, self.SELECTORS["add_to_playlist_button"])
        self.wait_and_click(By.XPATH, self.SELECTORS["play_button"])

    def close(self) -> None:
        self.driver.quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--browser",
        "-b",
        type=str,
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Browser to use",
    )
    parser.add_argument(
        "--song",
        "-s",
        type=str,
        default=SONG_NAME,
        help="Song to search and add to playlist",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    browser = BrowserTypes(args.browser)

    logger.info("Starting Spotify bot")
    bot = None
    try:
        bot = SpotifyBot(browser, song=args.song)
        bot.signup()
        bot.logout()
        bot.login()
        bot.search_and_add_to_playlist()
        sleep(2 * 60)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    finally:
        if bot:
            logger.info("Closing Spotify bot")
            bot.close()


if __name__ == "__main__":
    main()
