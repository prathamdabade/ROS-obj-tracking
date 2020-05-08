#!/usr/bin/env python
from  cv2 import cv2
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped

def publish():
   rospy.init_node('CVcode', anonymous=True)
   pub=rospy.Publisher('midpoint_coordinates',PoseStamped, queue_size=10)
   midpt=PoseStamped()
   r = rospy.Rate(20)
   r.sleep()

   while not rospy.is_shutdown():
     # Instantiate a video capture object, with 0 it will use the default system camera.
     cap = cv2.VideoCapture(0)
     cv2.namedWindow("frame",cv2.WINDOW_NORMAL)

     while True:
       ## Read rhe frame from the camera and convert to HSV
       res,frame = cap.read()
       hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
       #print(hsv_img)
       ## Creates a mask of the particular range in hsv colorspace
       #Values taken from reference values computed from 'hsv_tracker.py' 
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
       cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.   CHAIN_APPROX_SIMPLE)[-2]
       if cnts:
         # Find the maximum area contour and drawing bounding rectangle
         C_max = max(cnts,key = cv2.contourArea)
         x, y, w, h = cv2.boundingRect(C_max)
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
         midpt.pose.position.x = (2*x+w)/2
         midpt.pose.position.y = (2*y+h)/2
         print(midpt.pose.position.x, midpt.pose.position.y)
       cv2.imshow("frame",frame)

       if cv2.waitKey(1) & 0xFF == ord('q'):
         break
       pub.publish(midpt)
     cap.release()
     cv2.destroyAllWindows()
  

if __name__ == '__main__':
   try:
     publish()
   except rospy.ROSInterruptException:
     pass
