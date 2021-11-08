#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

cap = cv2.VideoCapture(0)
print (cap.isOpened())
bridge = CvBridge()

def talker():
    pub = rospy.Publisher('/webcam', Image, queue_size = 1)
    rospy.init_node('ImagePublisher', anonymous = False)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        ret, image = cap.read()
        if not ret:
            break

        msg = bridge.cv2_to_imgmsg(image, 'bgr8')
        pub.publish(msg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
