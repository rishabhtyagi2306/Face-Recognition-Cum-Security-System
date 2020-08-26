import numpy as np
from tkinter import *
import cv2

root = Tk()
root.geometry('500x600')
heading = Label(root, text="Welcome! to the super secure face recognition system",
                font=('montserrat', 12, "bold"), fg="black").pack()


def on_click():
    my_label = Label(root, text="Look into the camera")
    my_label.pack()
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        if faces is ():
            mylabel = Label(root, text="Sorry could not find your face try again")
            mylabel.pack()
        else:
            for (x, y, w, h) in faces:
                print(x, y, w, h)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                img_item = "my_image.png"
                cv2.imwrite(img_item, roi_color)

    cap.release()
    # cv2.destroyAllWindows()


my_button = Button(root, text="click here to open VS Code", command=on_click)
my_button.pack()

root.mainloop()
