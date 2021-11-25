#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

cap = cv2.VideoCapture(0)
print (cap.isOpened())
bridge = CvBridge()

cap.set(cv2.CAP_PROP_FPS, 5)
fps = cap.get(5)
print("Frames per second : {}".format(fps))

def talker():
    pub = rospy.Publisher('/webcam', Image, queue_size = 1)
    rospy.init_node('ImagePublisher', anonymous = False)
    # rate = rospy.Rate(2.5)   #2.5 Hz, that means we serve 5 frame per seconds

    while not rospy.is_shutdown():
        ret, image = cap.read()
        if not ret:
            break

        msg = bridge.cv2_to_imgmsg(image, 'bgr8')
        pub.publish(msg)

        # rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
