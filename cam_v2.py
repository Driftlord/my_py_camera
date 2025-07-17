import cv2
import datetime
import os

# Binary "data blob" file to store everything
storage_file = "collected_media.bin"
index_file = "media_index.txt"  # To keep track of what's inside the blob

# Global tracker for session
last_screenshot = None

# Function to save a screenshot and store it in both disk and binary file
def save_screenshot(frame):
    global last_screenshot
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"

    # Save temporarily to disk for preview
    if cv2.imwrite(filename, frame):
        last_screenshot = filename
        print(f"[Saved] Screenshot {filename} on disk.")
    else:
        print("[Error] Failed to save screenshot to disk.")
        return

    # Append the screenshot to binary storage
    with open(filename, "rb") as f:
        content = f.read()
        with open(storage_file, "ab") as store:
            store.write(b"--FILE_START--\n")
            store.write(f"FILENAME:{filename}\n".encode())
            store.write(f"SIZE:{len(content)}\n".encode())
            store.write(content)
            store.write(b"\n--FILE_END--\n")
    
    # Record in index file
    with open(index_file, "a") as log:
        log.write(f"[screenshot] {filename} added to {storage_file}\n")

    # Delete original file from disk after storing
    os.remove(filename)
    print(f"[Stored] Screenshot {filename} in {storage_file} and removed from disk.")

# Function to open and display the last screenshot
def open_last_screenshot():
    if last_screenshot and os.path.exists(last_screenshot):
        img = cv2.imread(last_screenshot)
        if img is not None:
            cv2.imshow("Last Screenshot", img)
            cv2.waitKey(0)  # Wait until a key is pressed
            cv2.destroyAllWindows()  # Close the image window
        else:
            print("[Error] Failed to open screenshot.")
    else:
        print("[Info] No screenshot left on disk. It’s stored in binary.")

# Function to record a video
def record_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] Cannot access webcam.")
        return

    # Get video frame width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.avi"

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))

    print("Recording... Press 'd' to stop recording.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Error] Frame capture failed.")
            break

        out.write(frame)  # Write frame to video file
        cv2.imshow("Recording (press 'd' to stop)", frame)

        # Stop recording when 'd' is pressed
        if cv2.waitKey(1) & 0xFF == ord('d'):
            print(f"Video saved as {filename}")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Append video to binary storage
    with open(filename, "rb") as f:
        content = f.read()
        with open(storage_file, "ab") as store:
            store.write(b"--FILE_START--\n")
            store.write(f"FILENAME:{filename}\n".encode())
            store.write(f"SIZE:{len(content)}\n".encode())
            store.write(content)
            store.write(b"\n--FILE_END--\n")
    
    # Record in index file
    with open(index_file, "a") as log:
        log.write(f"[video] {filename} added to {storage_file}\n")

    os.remove(filename)
    print(f"[Stored] Video {filename} in {storage_file} and removed from disk.")

# Main function to handle webcam feed and user input
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] Cannot open webcam.")
        return

    print("===== Webcam Logger (Data File Mode) =====")
    print("  s - Save screenshot")
    print("  o - Open last screenshot (if still on disk)")
    print("  v - Record video (stop with 'd')")
    print("  q - Quit")
    print("==========================================")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Error] Webcam feed failed.")
            break

        # Show the webcam feed
        cv2.imshow("Webcam Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        # Handle user input
        if key == ord('s'):
            save_screenshot(frame)  # Save a screenshot
        elif key == ord('o'):
            open_last_screenshot()  # Open the last saved screenshot
        elif key == ord('v'):
            print("Switching to video recording...")
            cap.release()  # Release the webcam
            cv2.destroyAllWindows()
            record_video()  # Start video recording
            cap = cv2.VideoCapture(0)  # Reopen the webcam after recording
        elif key == ord('q'):
            print("[Exit] Goodbye.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
