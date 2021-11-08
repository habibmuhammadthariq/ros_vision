#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


def callback(data):
    bridge = CvBridge()

    try:
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    cv2.imshow("Image Window", cv_img)
    cv2.waitKey(1)


def listener():
    rospy.init_node("ImageSubscriber", anonymous = True)
    rospy.Subscriber("/webcam", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    
