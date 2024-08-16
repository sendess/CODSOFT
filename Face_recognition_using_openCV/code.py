import cv2

# Loading the Haar cascade for face detection
Haar_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def bounding_box(frame, classifier, scaleF, minNeighbor, color, text):
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    features = classifier.detectMultiScale(grayscale, scaleF, minNeighbor)
    cordinates = []
    for (x_axis, y_axis, width, height) in features:
        cv2.rectangle(frame, (x_axis, y_axis), (x_axis + width, y_axis + height), color, 1)
        cv2.putText(frame, text, (x_axis, y_axis - 20), cv2.FONT_ITALIC, 1, color, 1, cv2.LINE_AA)
        cordinates = [x_axis, y_axis, width, height]    
    return cordinates, frame
        
def face_detection(frame, cascade):
    _, frame_with_boxes = bounding_box(frame, cascade, 1.2, 9, (0, 255, 0), "Face")
    return frame_with_boxes

def main():
    while True:
        print("Which will be the video input for your program? \n\t\t1. Default Camera\n\t\t2. Screen Video")
        choice = int(input("Enter your choice 1 or 2 \t"))
        if choice == 1:
            source = 0
            width, height = 640, 480
            break
        elif choice == 2:
            source = 1
            width, height = 1366, 768
            break
        else:
            print("Invalid choice! Please enter 1 or 2.\n")

    video_feed = cv2.VideoCapture(source)

    if not video_feed.isOpened():
        print("Error: Can't open video capture.")
        return

    while True:
        ret, frame = video_feed.read()

        if not ret:
            print("Error: Can't grab frame.")
            break
    
        resized_frame = cv2.resize(frame, (width, height))  # Changing size of the frame for better viewing
        
        detection = face_detection(resized_frame, Haar_classifier)  # Detecting face on the resized frame
    
        cv2.imshow("Webcam Feed", detection)  # Displaying the frames after detection is applied to it

        if cv2.waitKey(1) & 0xFF == ord('p'):  # Breaking loop if 'p' is pressed while the window is in focus
            break

    video_feed.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
