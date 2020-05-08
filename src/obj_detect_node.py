#! /usr/bin/env python
import rospy
from obj_tracking.msg import point
from cv2 import cv2
import numpy as np

rospy.init_node('ball_tracking', anonymous=True)
pub = rospy.Publisher('ball_tracker', point, queue_size=20)
r = rospy.Rate(20)
msg = point()
# Instantiate a video capture object, with 0 it will use the default system camera.
cap = cv2.VideoCapture(0)
cv2.namedWindow("frame",cv2.WINDOW_NORMAL)

while True:
  ## Read rhe frame from the camera and convert to HSV
  ret,frame = cap.read()
  hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

  ## Creates a mask of the particular range in hsv colorspace
  mask = cv2.inRange(hsv_img, (29, 102, 0), (48, 255,255))

  ## Visualize the mask
  res = cv2.bitwise_and(frame,frame,mask = mask)
  cv2.imshow("result",res)
  cv2.imshow("mask",mask)

  ## erosion and dilation (not necessary)
  ## Processing to get better contours
  kernel = np.ones((3,3))
  erosion = cv2.erode(mask,kernel,iterations=1)
  dilation = cv2.dilate(erosion,kernel,iterations=1)
  mask = dilation.copy()

  ## Finding contours
  cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
  if cnts:
    # Find the maximum area contour and drawing bounding rectangle
    C_max = max(cnts,key = cv2.contourArea)
    x, y, w, h = cv2.boundingRect(C_max)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
    mid_x = int(x+(w/2))
    mid_y = int(y+(h/2))
    frame = cv2.circle(frame,(mid_x,mid_y), radius=5, color=(0, 0, 255),thickness=-1)
    msg.x = mid_x
    msg.y = mid_y
    pub.publish(msg)
    r.sleep()
    print(mid_x,mid_y)

  cv2.imshow("frame",frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()
