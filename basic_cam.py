import cv2

# Print OpenCV version to verify installation
print(f"OpenCV Version: {cv2.__version__}")

# Try to load and display an image (test.jpg should be in the working directory)
img = cv2.imread("test.jpg")

# Check if the image is loaded successfully
if img is None:
    print("Failed to load image. Check the filename and path.")
else:
    cv2.imshow("Image", img)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()  # Close the image window

# Load the image in different formats for testing
normal = cv2.imread("test.jpg", cv2.IMREAD_COLOR)
bnw = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
dfl = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED)
rndm = cv2.imread("test.jpg", cv2.IMREAD_ANYCOLOR)

# Check if all image formats loaded correctly
if normal is None or bnw is None or dfl is None or rndm is None:
    print("Error loading images.")
else:
    # Save a random color version as 'random_color.jpg'
    cv2.imwrite("random_color.jpg", rndm)

    # Display the images (Optional)
    # cv2.imshow("Normal Color", normal)
    # cv2.imshow("Black & White", bnw)
    # cv2.imshow("Unchanged", dfl)
    # cv2.imshow("Random Color", rndm)
    
    # Wait until a key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()  # Close all image windows

# Start video capture (Webcam)
cap = cv2.VideoCapture(0)

# Check if the camera is successfully opened
if not cap.isOpened():
    print("Error: Cannot access the webcam.")
    exit()

print("Opening webcam...")

# Start capturing video
while True:
    success, frame = cap.read()  # Capture frame-by-frame
    if not success:
        print("Error: Failed to capture frame.")
        break

    # Show the current frame from the webcam
    cv2.imshow("Live Webcam Feed", frame)

    # Exit the webcam feed when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
