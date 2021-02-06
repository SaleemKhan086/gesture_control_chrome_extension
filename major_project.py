#import statements
import numpy as np
import cv2
import math
import pyautogui
import collections
import time
from flask import session
from flask import Flask, escape, request

# function for performing actions corresponding to gestures
def perform_(no_of_defects, data, frame):
    for key in data:
        if key is not 't' and int(data.get(key)) == no_of_defects :
            if key == 'scroll_up':
                print(key,data.get(key))
                pyautogui.scroll(300)   #scroll up the page
            elif key == 'scroll_down':
                print(key,data.get(key))
                pyautogui.scroll(-300)      #scroll down the page
            elif key == 'previous_tab':
                print(key,data.get(key))
                pyautogui.hotkey('ctrl', 'pgup')  #previous tab
            elif key == 'next_tab':
                print(key,data.get(key))
                pyautogui.hotkey('ctrl', 'pgdn')    #next ta
            elif key == 'zoom_in':
                print(key,data.get(key))
                pyautogui.hotkey('ctrl', '+')     #zoom in
            elif key == 'zoom_out':
                print(key,data.get(key))
                pyautogui.hotkey('ctrl', '-')   #zoom out
            break
    return frame



app = Flask(__name__)
app.secret_key = "abc"
@app.route('/',methods = ['POST'])

def major():
    time.sleep(1)
    pyautogui.hotkey('winleft', 'right')
    data = request.get_json()
    t = bool(int(data.get('t')))
    if t:
    	with open('temp_file.txt','w') as f:
            f.write("1")
    else:
    	with open('temp_file.txt','w') as f:
            f.write("")
    toggle = False
    with open('temp_file.txt','r') as f:
        toggle = bool(f.read())

    check=False
    if t:
        capture = cv2.VideoCapture(0)   # value 0 for default camera

    list = []
    while toggle and capture.isOpened():
        with open('temp_file.txt','r') as f:
            toggle = bool(f.read())
        check=True
        ret, frame = capture.read()                     # capture frames continuously
        frame = cv2.flip(frame, 1)                      # 1 - means flipping around y-axis

        start_x, start_y, end_x, end_y = 300, 20, 580, 250
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 1)   # BGR (0, 255, 0), thickness - 1
        roi = frame[start_y:end_y, start_x:end_x]                                  # roi - region of interest

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)                                 # from bgr to hsv

        lower_bound = np.array([0, 20, 70], dtype = np.uint8)
        upper_bound = np.array([20, 255, 255], dtype = np.uint8)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)                          #extracts skin colour image

        kernel = np.ones((3,3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=4)                               #morphological transformation
        mask = cv2.GaussianBlur(mask, (5,5), 100)                                   #blur the image

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        try:
            contour = max(contours, key = lambda x: cv2.contourArea(x))                 # find contour of maximum area

            # create bounding rectangle around the contour
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),0)

            #approx the contour
            epsilon = 0.0005 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            #creating convex hull
            hull = cv2.convexHull(contour)

            area_hull = cv2.contourArea(hull)
            area_contour = cv2.contourArea(contour)

            area_ratio = ((area_hull - area_contour) / area_contour ) * 100

            #finding out the defects in the hull wrt hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            no_of_defects = 0

            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])

                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                area = math.sqrt(s * (s - a) * (s - b) * (s - c))

                # distance between point and convex hull
                distance = (2 * area) / a

                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                if angle <= 90 and distance > 30:
                    no_of_defects = no_of_defects + 1
                    cv2.circle(roi, far, 3, [255,0 , 0], -1)

                cv2.line(roi, start, end, [0, 255, 0], 2)

            no_of_defects = no_of_defects + 1

            #storing no. of defects in a list
            if no_of_defects == 1:
                if area_contour < 2000:
                    list.append(-1)
                else:
                    if area_ratio < 12:
                        list.append(0)
                    else:
                        list.append(1)
            else:
                list.append(no_of_defects)

            temp = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

            if len(list)>50 and collections.Counter(temp) == collections.Counter(list[-10:]):
                result = []
                var = list.count(-1)
                if var < 0.9 * len(list):
                    result = [list.count(0),list.count(1),list.count(2),list.count(3),list.count(4),list.count(5)]
                    max_element = max(result)
                    index_of_ele = result.index(max_element)
                    frame=perform_(index_of_ele, data, frame)
                    list = []
        except:
            pass

        # show the windows
        cv2.imshow('mask', mask)
        #cv2.imshow('frame', frame)
        cv2.moveWindow('mask', 0,30)
        if cv2.waitKey(10)==ord('q'):
            break
    if not toggle and check :
        capture.release()
        cv2.destroyAllWindows()
    return "Successfully Launched"
