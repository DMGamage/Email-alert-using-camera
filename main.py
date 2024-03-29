import glob
import os
import time
import cv2
from emailling  import send_email
import os
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list=[]
count =0

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


while True:
    status =0


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
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png",frame)
            count =count+1
            all_images =glob.glob("images/*.png")
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email,args=(image_with_object,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder())
        clean_thread.daemon =True
        email_thread.start()


    cv2.imshow("My test", frame)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()
clean_thread.start()

