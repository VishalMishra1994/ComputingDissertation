import cv2

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No Frame")
        break
    cv2.imshow("Pi Camera", frame)
    if cv2.waitKey(1) == ord('q'): break
cap.release()
cv2.destroyAllWindows()
