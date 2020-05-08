#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped

midpt=PoseStamped()
def callback(msg):
  global midpt
  midpt=msg

current_pos=PoseStamped()
def callback2(msg):
     global current_pos
     current_pos=msg

def move():
  rospy.init_node('move_drone', anonymous=True)
  pub=rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=20)
  r = rospy.Rate(20)
  r.sleep()

  sub1=rospy.Subscriber('midpoint_coordinates', PoseStamped,  callback)
  sub2=rospy.Subscriber('mavros//local_position/pose', PoseStamped, callback2)
  pub_pos=PoseStamped()



  while not rospy.is_shutdown():
    xcurr=current_pos.pose.position.x
    ycurr=current_pos.pose.position.y
    zcurr=current_pos.pose.position.z


    def pub_set():
      pub_pos.pose.position.x = xcurr
      pub_pos.pose.position.z = zcurr
      print(pub_pos.pose.position.x, pub_pos.pose.position.y)
      pub.publish(pub_pos)
 
    def topright():
      pub_pos.pose.position.x= xcurr + 0.2
      pub_pos.pose.position.z= zcurr + 0.2
      pub_set()

    def bottomright():
      pub_pos.pose.position.x= xcurr + 0.2
      pub_pos.pose.position.z= zcurr - 0.2
      pub_set()

    def bottomleft():
      pub_pos.pose.position.x= xcurr - 0.2
      pub_pos.pose.position.z= zcurr - 0.2
      pub_set()

    def topleft():
      pub_pos.pose.position.x= xcurr - 0.2
      pub_pos.pose.position.z= zcurr + 0.2
      pub_set()


    def right():
      pub_pos.pose.position.x= xcurr + 0.2
      pub_set()
 
    def left():
      pub_pos.pose.position.x= xcurr - 0.2
      pub_set()

    def up():
      pub_pos.pose.position.z= zcurr + 0.2
      pub_set()

    def down():  
      pub_pos.pose.position.z= zcurr - 0.2
      pub_set()


    midx = midpt.pose.position.x 
    midy = midpt.pose.position.y  
#Webcam windw is 630x470 pixels approx. error margin of +-15 pixels is giveen from screen center   
    if midx < 300:

      if midy < 220:
        topleft()
      elif midy > 250:
        bottomleft()
      elif midy<=250 and midy>220: 
        left()


    elif midx > 330:


      if midy < 220:
        topright()
      elif midy > 250:
        bottomright()
      elif midy>=220 and midy<=250:
        right()


    elif midx<=330 and midx>=300:


      if midy < 220:
        up()
      elif midy > 250:
        down()
      elif midy>=220 and midy<=250:
        break

if __name__ == '__main__':
  try:
    move()
  except rospy.ROSInterruptException:
    pass
