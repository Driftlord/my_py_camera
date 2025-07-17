import cv2
import datetime

# Global variable to track the last screenshot filename
last_screenshot = None

def save_screenshot(frame):
    """Captures a screenshot and saves it with a timestamped filename."""
    global last_screenshot
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    last_screenshot = f"screenshot_{timestamp}.png"
    if cv2.imwrite(last_screenshot, frame):
        print(f"Screenshot saved as {last_screenshot}")
    else:
        print("Error: Failed to save screenshot.")

def open_last_screenshot():
    """Opens the last saved screenshot."""
    if last_screenshot:
        img = cv2.imread(last_screenshot)
        if img is not None:
            cv2.imshow("Latest Screenshot", img)
            cv2.waitKey(0)  # Wait until a key is pressed
            cv2.destroyAllWindows()  # Close the image window
        else:
            print("Error: Unable to read the screenshot.")
    else:
        print("No screenshot has been saved in this session.")

def exit_program():
    """Handles the exit process."""
    print("Exiting...")
    return False

def record_video():
    """Records a video and saves it with a timestamped filename."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access webcam for recording.")
        return

    # Get the video frame width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.avi"

    # Setup the video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))

    print("Recording... Press 'd' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        out.write(frame)  # Write the frame to the video file
        cv2.imshow("Recording", frame)  # Display the frame

        # Stop recording when 'd' is pressed
        if cv2.waitKey(1) & 0xFF == ord('d'):
            print(f"Video saved as {filename}")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    """Main function to handle webcam feed and user input."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the webcam")
        return

    print("Press:")
    print("  s - Save Screenshot")
    print("  o - Open Last Screenshot")
    print("  v - Record Video")
    print("  q - Quit")

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame.")
            break

        # Show the webcam feed
        cv2.imshow('Webcam Feed', frame)

        # Handle user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            save_screenshot(frame)  # Save a screenshot
        elif key == ord('o'):
            open_last_screenshot()  # Open the last saved screenshot
        elif key == ord('v'):
            print("Switching to video recording...")
            cap.release()
            cv2.destroyAllWindows()
            record_video()  # Start video recording
            cap = cv2.VideoCapture(0)  # Reopen the webcam after recording
        elif key == ord('q'):
            running = exit_program()  # Quit the program

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
