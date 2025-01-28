import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from urllib.parse import quote
import os

class Style:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

print(Style.BLUE)
print("***** THANK YOU FOR USING TEAMFIVE BOT *****")
print("***** BULK WHATSAPP MESSENGER TOOL *****")
print("*******************************************")
print(Style.RESET)

# File paths
BASE_DIR = r"C:\projects\bank3\bank_project"
MESSAGE_FILE = os.path.join(BASE_DIR, "message.txt")
NUMBERS_FILE = os.path.join(BASE_DIR, "numbers.txt")
SESSION_FILE = os.path.join(BASE_DIR, "session.txt")
IMAGE_FILE = os.path.join(BASE_DIR, "image.jpg")

def save_cookies(driver):
    """Save session cookies to a file."""
    cookies = driver.get_cookies()
    with open(SESSION_FILE, 'w') as f:
        for cookie in cookies:
            f.write(f"{cookie['name']}={cookie['value']}\n")

def load_cookies(driver):
    """Load session cookies from a file."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            cookies = f.readlines()
        for cookie in cookies:
            name, value = cookie.strip().split('=')
            driver.add_cookie({'name': name, 'value': value})
        return True
    return False

def wait_for_element(driver, by, value, timeout=30, condition="clickable"):
    """Wait for an element to appear and return it."""
    try:
        if condition == "clickable":
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        elif condition == "presence":
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
    except TimeoutException:
        return None

def is_logged_in(driver):
    """Check if the user is logged in to WhatsApp Web."""
    try:
        chat_list = wait_for_element(
            driver,
            By.XPATH,
            "//div[contains(@class, 'two') or contains(@class, 'chat')]",
            timeout=5,
            condition="presence"
        )
        return chat_list is not None
    except:
        return False

def send_message_with_image(driver, number, message, image_path, retry_count=3):
    """Send a message with an image to a WhatsApp contact."""
    for attempt in range(retry_count):
        try:
            # Format the number and URL
            number = number.replace('+', '')
            url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
            driver.get(url)

            sleep(10)  # Wait for the chat to load

            # Find and click the attachment button
            attach_button = wait_for_element(driver, By.XPATH, "//button[@title='Attach']", timeout=10)
            if not attach_button:
                raise Exception("Attachment button not found")
            attach_button.click()

            # Upload the image
            file_input = wait_for_element(driver, By.XPATH, "//input[@type='file']", timeout=10)
            if not file_input:
                raise Exception("File input field not found")
            file_input.send_keys(image_path)

            # Click the send button
            send_button = wait_for_element(driver, By.XPATH, "//span[@data-icon='send']", timeout=10)
            if not send_button:
                raise Exception("Send button in image preview not found")
            send_button.click()

            sleep(5)  # Wait for the image and message to be sent
            return True

        except Exception as e:
            print(Style.YELLOW + f"Attempt {attempt + 1} failed: {str(e)}" + Style.RESET)
            if attempt == retry_count - 1:
                return False
            sleep(5)

def validate_files():
    """Ensure necessary files exist before starting."""
    if not os.path.exists(MESSAGE_FILE):
        print(Style.RED + f"Error: {MESSAGE_FILE} not found." + Style.RESET)
        return False
    if not os.path.exists(NUMBERS_FILE):
        print(Style.RED + f"Error: {NUMBERS_FILE} not found." + Style.RESET)
        return False
    if not os.path.exists(IMAGE_FILE):
        print(Style.RED + f"Error: {IMAGE_FILE} not found." + Style.RESET)
        return False
    return True

def main():
    # Validate files
    if not validate_files():
        return

    # Load message
    with open(MESSAGE_FILE, "r") as f:
        message = f.read().strip()
    if not message:
        print(Style.RED + "Error: Message file is empty." + Style.RESET)
        return
    message = quote(message)

    # Load numbers
    with open(NUMBERS_FILE, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]
    if not numbers:
        print(Style.RED + "Error: Numbers file is empty." + Style.RESET)
        return

    print(Style.GREEN + f"Found {len(numbers)} numbers to send messages." + Style.RESET)

    # Initialize browser
    try:
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = uc.Chrome(options=options)

        driver.get("https://web.whatsapp.com")
        input("Scan QR Code and press Enter to continue...")

        for number in numbers:
            print(Style.YELLOW + f"Sending message to {number}..." + Style.RESET)
            success = send_message_with_image(driver, number, message, image_path=IMAGE_FILE)
            if success:
                print(Style.GREEN + f"Message sent to {number}" + Style.RESET)
            else:
                print(Style.RED + f"Failed to send message to {number}" + Style.RESET)
            sleep(5)  # Pause between messages

        print(Style.GREEN + "All messages sent." + Style.RESET)

    except Exception as e:
        print(Style.RED + f"Error initializing browser: {e}" + Style.RESET)

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
