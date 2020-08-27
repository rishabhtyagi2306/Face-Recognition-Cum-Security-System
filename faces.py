import numpy as np
from tkinter import *
import cv2
import faces_train as ft
import os
import keys
import smtplib
import pyttsx3
import imghdr
from email.message import EmailMessage

root = Tk()
root.geometry('500x600')
heading = Label(root, text="Welcome! to the super secure face recognition system",
                font=('montserrat', 12, "bold"), fg="black").pack()


def speak(my_entry):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(my_entry)
    engine.runAndWait()


def send_mails():
    with open('test.jpg', 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(keys.Gmail(), keys.gmail_password())
        msg = EmailMessage()
        msg['Subject'] = "Alert !!!"
        msg['From'] = keys.Gmail()
        msg['To'] = keys.Alert_Gmail()
        msg.set_content("Someone tried to use your system. If it isn't you then please make necessary actions. Image "
                        "of that person is attached with this mail.")
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
        smtp.send_message(msg)

    # server = smtplib.SMTP_SSL('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # server.login(keys.Gmail(), keys.gmail_password())
    # subject = "Alert !!!"
    # body = "Someone tried to use your system. If it isn't you then please make necessary actions."
    # msg = f'Subject: {subject}\n\n{body}'
    # server.sendmail(keys.Gmail(), keys.Alert_Gmail(), msg)
    # server.close()


def on_click():
    my_label = Label(root, text="please, Look into the camera")
    my_label.pack()
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    cap = cv2.VideoCapture(0)
    speak("please, Look into the camera for 5 seconds to open Visual Studio Code")
    if cap.isOpened():
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        if faces == ():
            mylabel = Label(root, text="Sorry could not find your face try again")
            mylabel.pack()
            speak("Sorry could not find your face try again")
        else:
            for (x, y, w, h) in faces:
                print(x, y, w, h)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                img_item = "test.jpg"
                cv2.imwrite(img_item, roi_color)
                a = ft.classify_face("test.jpg")
                print(ft.classify_face("test.jpg"))
                if a == ['Unknown']:
                    try:
                        mylabel = Label(root, text="Sorry Sir !!! you are not authenticated to enter the system")
                        mylabel.pack()
                        speak("Sorry Sir !!! you are not authenticated to enter the system")
                        send_mails()
                    except Exception as e:
                        print(e)
                        mylabel = Label(root, text="Sorry Sir !!! you are not authenticated to enter the system")
                        mylabel.pack()
                        speak("Sorry Sir !!! you are not authenticated to enter the system")

                else:
                    mylabel = Label(root, text="Welcome Sir !!!")
                    mylabel.pack()
                    s = "Welcome Sir !!!" + " opening Visual Studio Code please wait."
                    speak(s)
                    path = keys.VS_PATH()
                    os.startfile(path)

    cap.release()
    # cv2.destroyAllWindows()


my_button = Button(root, text="click here to open VS Code", command=on_click)
my_button.pack()

root.mainloop()
