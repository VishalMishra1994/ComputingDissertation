import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera na")
    exit()

ret, frame = cap.read()
if ret:
    cv2.imshow("test", frame)
    cv2.waitKey(0)
else:
    print("No frame")

cap.release()
cv2.destroyAllWindows()
