import time

import cv2
video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None

while True:

    check,frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_blur = cv2.GaussianBlur(gray_frame,(21,21),0)


    if first_frame is None:
        first_frame = gray_frame_blur

    delta_frame = cv2.absdiff(first_frame,gray_frame_blur)
    thresh_frame = cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]
    dilate_frame = cv2.dilate(thresh_frame,None,iterations=2)

    contours, hierarchy = cv2.findContours(dilate_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 5000:
            continue

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0))

        cv2.imshow("My test", frame)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()

