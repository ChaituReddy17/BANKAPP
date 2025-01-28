import pywhatkit as kit
import pyautogui
import time
import os


def send_whatsapp_message_with_image(number, message, image_path):
    try:
        print(f"Opening WhatsApp chat for {number}...")
        kit.sendwhatmsg_instantly(number, message)
        time.sleep(10)
        if os.path.exists(image_path):
            print("Locating Attach button and selecting image...")

            pyautogui.click(x=916, y=1071)  # Coordinates for the "Attach" button
            time.sleep(6)

            pyautogui.click(x=1080, y=708)  # Coordinates for "Photos & Videos"
            time.sleep(6)

            pyautogui.write(image_path)  # Write the image path
            time.sleep(6)
            
            # Press Enter to confirm the file selection
            pyautogui.press("enter")
            time.sleep(6)
        else:
            print("Image file not found. Sending text only.")
        
        print("Pasting the message in the message box...")
        pyautogui.write(message)  # Paste the text message into the input box
        time.sleep(2)
        
        # Click the send button
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
