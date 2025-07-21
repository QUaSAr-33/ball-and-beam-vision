import cv2
import numpy as np
import time
import serial
import serial.tools.list_ports
ports=serial.tools.list_ports.comports()
cx_prev=320
alpha=0.400
beta=0.900
kp=0.075000
kd=0.12
ki=0.0
output=0.000
error=0.000
previous_error=0.000
prev_time=time.time()
integral=0.000
derivative=0.000
filtered_derivative=0.000
print("Available Ports: ")
for port in ports:
    print(str(port))
serialInst=serial.Serial()
portsList=[]
com=input("Enter the port name: ")
serialInst.baudrate=9600
serialInst.port=com
try:
    serialInst.open()
    time.sleep(2)
    print(f"{com} is ready for communication")
except Exception as e:
    print("Can't open the port. ", e)
video=cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if not video.isOpened():
    print("Can't open the camera")
    exit()
while True:
    ret,frame=video.read()
    if not ret:
        print("can't load the frame")
        exit()
    cv2.line(frame,(320,0),(320,480),(0,255,0),2)
    cv2.putText(frame,"Callibrating...",(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    cv2.putText(frame,"Bring the link on the green line",(20,200),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)
    cv2.imshow("Callibration Window",frame)
    if cv2.waitKey(1)&0xFF==ord('W'):
        break
video.release()
cv2.destroyAllWindows()
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ref=320
if not cap.isOpened():
    print("Can't open the camera")
    exit()
while True:
    ret,frame=cap.read()
    if not ret:
        print("can't load the frame")
        exit()
    lower_color = np.array([0, 61, 127])
    upper_color = np.array([82,255,255])
    blurr=cv2.GaussianBlur(frame,(11,11),0)
    hsv=cv2.cvtColor(blurr,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_color,upper_color)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_result = frame.copy()
    hsv_result=hsv.copy()
    mask_result=mask.copy()
    cv2.drawContours(frame_result,contours,-1,(0,255, 255),2)
    if contours:
        key=max(contours,key=cv2.contourArea)
        m=cv2.moments(key)
        if m['m00']==0: continue
        cx=int(m['m10']/m['m00'])
        cy=int(m['m01']/m['m00'])
        cx_filtered=alpha*cx_prev+(1-alpha)*cx
        x,y,w,h=cv2.boundingRect(key)
        cv2.rectangle(frame_result,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.putText(frame_result,f"KEY COLOR, x = {cx}, y = {cy}",(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.rectangle(hsv_result,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(hsv_result,f"KEY COLOR, x = {cx}, y = {cy}",(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
        cv2.rectangle(mask_result,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(mask_result,f"KEY COLOR, x = {cx}, y = {cy}"                      ,(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
        error=ref-cx_filtered
        current_time=time.time()
        dt=current_time-prev_time
        integral+=error*dt
        derivative=(error-previous_error)/dt if dt>0 else 0
        filtered_derivative=beta*filtered_derivative*+(1-beta)*derivative
        output=(kp*error+ki*integral+kd*filtered_derivative)+105
        output=int(output)
        output = max(65, min(150, output))
        serialInst.write((str(output) + "\n").encode())
        #print(output)
        
        previous_error=error
        prev_time=current_time
        cx_prev = cx_filtered

        

    cv2.imshow("control window",frame_result)
    cv2.imshow("hsv window",hsv_result)
    cv2.imshow("masked window",mask_result)
    time.sleep(0.01)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()