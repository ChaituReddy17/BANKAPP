import pywhatkit as kit
import pyautogui
import time
import os


def send_whatsapp_message_with_image(number, message, image_path):
    """
    Sends a WhatsApp message with an image to a given number.
    
    Args:
        number (str): The phone number in international format (e.g., "+919876543210").
        message (str): The message to send.
        image_path (str): The path to the image file.
    """
    try:
        # Open WhatsApp chat using pywhatkit
        print(f"Opening WhatsApp chat for {number}...")
        kit.sendwhatmsg_instantly(number, message)
        
        # Wait for WhatsApp Web to load
        time.sleep(10)

        # Check if the image path exists
        if os.path.exists(image_path):
            print("Locating Attach button and selecting image...")

            # Click the 'Attach' button (Adjust coordinates as needed)
            pyautogui.click(x=916, y=1071)  # Coordinates for the "Attach" button
            time.sleep(2)

            pyautogui.click(x=1080, y=708)  # Coordinates for "Photos & Videos"
            time.sleep(2)

            # Wait for the file explorer to open (add delay to ensure it opens)
            print("Waiting for file explorer to open...")
            time.sleep(3)

            # Type the image file path into the input field
            pyautogui.write(image_path)  # Enter the file path of the image
            time.sleep(2)

            # Press Enter to confirm the file selection
            pyautogui.press("enter")
            time.sleep(2)
        else:
            print("Image file not found. Sending text only.")
        
        # After image is selected, paste the message in the message box
        print("Pasting the message in the message box...")
        pyautogui.write(message)  # Paste the text message into the input box
        time.sleep(2)

        # Press Enter to send the message with the image
        pyautogui.press("enter")
        print(f"Message with image sent to {number}.")

    except Exception as e:
        print(f"Error: {e}")


def main():
    # Example data
    BASE_DIR = r"C:\projects\bank3\bank_project"
    MESSAGE_FILE = os.path.join(BASE_DIR, "message.txt")
    NUMBERS_FILE = os.path.join(BASE_DIR, "numbers.txt")
    IMAGE_FILE = os.path.join(BASE_DIR, "image.jpg")
    
    # Validate files
    if not os.path.exists(MESSAGE_FILE):
        print(f"Error: {MESSAGE_FILE} not found.")
        return
    if not os.path.exists(NUMBERS_FILE):
        print(f"Error: {NUMBERS_FILE} not found.")
        return
    
    # Load message
    with open(MESSAGE_FILE, "r") as f:
        message = f.read().strip()
    if not message:
        print("Error: Message file is empty.")
        return

    # Load numbers
    with open(NUMBERS_FILE, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]
    if not numbers:
        print("Error: Numbers file is empty.")
        return

    print(f"Found {len(numbers)} numbers to send messages.")
    
    # Send messages
    for number in numbers:
        print(f"Sending message to {number}...")
        send_whatsapp_message_with_image(number, message, IMAGE_FILE)
        time.sleep(5)  # Pause between messages
    
    print("All messages sent.")


if __name__ == "__main__":
    main()
