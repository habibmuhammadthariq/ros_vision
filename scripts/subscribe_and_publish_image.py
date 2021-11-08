#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
   
def callback(data):
    try:
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
   
    cv2.imshow("Image window", cv_img)
    cv2.waitKey(1)
   
    try:
        image_pub.publish(bridge.cv2_to_imgmsg(cv_img, "bgr8"))
    except CvBridgeError as e:
        print(e)
   
def pub_sub():
    global bridge
    global image_pub
    rospy.init_node('publish_and_subscribe_image', anonymous=True)
    rospy.Subscriber("/webcam", Image, callback)
    image_pub = rospy.Publisher("/publish_webcam_image", Image, queue_size=1)
    bridge = CvBridge()
    rospy.spin()
   
if __name__ == '__main__':
    try:
        pub_sub()
    except rospy.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
