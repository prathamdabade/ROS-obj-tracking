#! /usr/bin/env python
import rospy
from obj_tracking.msg import point
from geometry_msgs.msg import TwistStamped
rospy.init_node('obj_listener', anonymous=True)

data = point()
pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=20)
vel_msg = TwistStamped()
r = rospy.Rate(20)

def callback(msg):
  global data
  data = msg
  #rospy.loginfo(data)
  x = data.x
  y = data.y
  y = (240-y)/300
  x = (x-320)/300
  print(x,y)
  publish(x,y)




def main():
  global data
  rospy.Subscriber('ball_tracker', point, callback)
  rospy.spin()

  
def publish(vx,vz):
  vel_msg.twist.linear.x = vx
  vel_msg.twist.linear.y = 0
  vel_msg.twist.linear.z = vz
  vel_msg.twist.angular.x = 0
  vel_msg.twist.angular.y = 0
  vel_msg.twist.angular.z = 0
  pub.publish(vel_msg)


if __name__ == "__main__":
  try:
    main()
  except rospy.ROSInterruptException():
    pass