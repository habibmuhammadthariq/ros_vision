#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import simple_find_contours as fc

VERBOSE = False

def callback(data):
    if VERBOSE:
        print ('received image of type: "%s"' % data.format)
        
    bridge = CvBridge()
    
    # get images from camera
    try:
        np_arr = np.fromstring(data.data, np.uint8)
        cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #cv_img = bridge.compressed_imgmsg_to_cv2(data, 'passthrough')
    except CvBridgeError as e:
        print(e)
        
    # temp
    #cv2.imshow("hayoo", cv_img)
    #cv2.waitKey(1)
    
    # get contour
    detected_image, status = fc.extract(cv_img, True)
    # get direction
    if status:
        direction = fc.get_direction()
        print("Next destination : {}".format(direction))

    # show the image up
    cv2.imshow('Detected Image', detected_image)
    cv2.waitKey(1)

    # publish detected object
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"
    msg.data = np.array(cv2.imencode('.jpg', detected_img)[1]).tostring()
    try:
        img_pub.publish(msg)
    except CvBridgeError as e:
        print(e)


def drone_navigation():
    global img_pub
    rospy.init_node('drone_navigation', anonymous=True)
    rospy.Subscriber('/tello/image_raw/h264', CompressedImage, callback)
    if VERBOSE:
        print ('Subscribed to /tello/image_raw/h264')
        
    img_pub = rospy.Publisher('/detected_object', CompressedImage, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    try:
        drone_navigation()
    except rospy.ROSInterruptException:
        pass
