import cv2

# Loading the Haar cascade for face detection
Haar_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def bounding_box(frame, classifier, scaleF, minNeighbor, color, text):#to draw rectangle box on face
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    features = classifier.detectMultiScale(grayscale, scaleF, minNeighbor)
    cordinates = []
    for (x_axis, y_axis, width, height) in features:
        cv2.rectangle(frame, (x_axis, y_axis), (x_axis + width, y_axis + height), color, 1)
        cv2.putText(frame, text, (x_axis, y_axis - 20), cv2.FONT_ITALIC, 1, color, 1, cv2.LINE_AA)
        cordinates = [x_axis, y_axis, width, height]
    
    return cordinates, frame
        
def face_detection(frame, cascade):#applying Haar Cascade classifier to the frame
    _, frame_with_boxes = bounding_box(frame, cascade, 1.5, 3, (0, 255, 0), "Face")
    return frame_with_boxes

def main():
    video_feed = cv2.VideoCapture(0)

    if not video_feed.isOpened():
        print("Error. Cant open video capture.")
        return

    while True:
        ret, frame = video_feed.read()

        if not ret:
            print("Error: Cant grab frame.")
            break
    
        resized_frame = cv2.resize(frame, (888, 666))# changing size of the frame for better viewing
        
        detection = face_detection(resized_frame, Haar_classifier)# detecting face on the resized frame
    
        cv2.imshow("Webcam Feed", detection) # displaying the frames after detection applied to it

        if cv2.waitKey(1) & 0xFF == ord('p'):# breaking loop if 'p' is pressed while python window is in focus
            break

    video_feed.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
