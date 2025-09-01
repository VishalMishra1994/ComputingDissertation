# import cv2

# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("No Frame")
#         break
#     cv2.imshow("Pi Camera", frame)
#     if cv2.waitKey(1) == ord('q'): break
# cap.release()
# cv2.destroyAllWindows()
import cv2
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # hint V4L2
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    ok, f = cap.read()
    if not ok:
        print("No Frame"); break
    cv2.imshow("Pi Cam", f)
    if cv2.waitKey(1) == ord('q'): break

cap.release(); cv2.destroyAllWindows()
