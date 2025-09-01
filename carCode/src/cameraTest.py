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
##########################################################
# from picamera2 import Picamera2
# import cv2

# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
# picam2.start()

# while True:
#     frame = picam2.capture_array()
#     cv2.imshow("Pi Cam (Picamera2)", frame)
#     if cv2.waitKey(1) == ord('q'): break

# cv2.destroyAllWindows()
# picam2.stop()
################################################################
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
picam2.start_preview(Preview.DRM)  # requires a display connected to HDMI
picam2.configure(picam2.create_preview_configuration())
picam2.start()
