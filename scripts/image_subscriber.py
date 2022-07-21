#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

#temp
import time

class listener:
    def __init__(self):
        #start this node
        rospy.init_node("ImageSubscriber", anonymous=True)
        #medium to convert ros image into cv image
        self.bridge = CvBridge()
        #start subscriber
        self.img_sub = rospy.Subscriber("/webcam", Image, self.callback)
        #do any work while this node going to stop
        rospy.on_shutdown(self.end)


        #temp
        self.start = rospy.get_rostime().secs
        print ("Current time with get_rostime() :  ", self.start)

        self.counter = 0
    

    def callback(self, data):
        try:
            img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print (e)
        
        
        #displaying the image
        cv2.imshow("Subscriber Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            #stop subscribing this topic
            self.img_sub.unregister()
            #stop this ros
            rospy.signal_shutdown("")
        
        #stop this node after 30's
        self.counter += 1
        print ("this the image number : %d" % self.counter)

        self.now = rospy.get_rostime().secs
	    result = (self.now-self.start)/60.0
	    print('type  : {}. now : {}'.format(type(result), result))
        if (self.now-self.start)/60.0 == 0.05:	# 0.05 = 3 seconds # 0.5 = 30 seconds, 1 = one minutes
            rospy.signal_shutdown("")
        # if self.counter == 10:
            # print 

    def end(self):
        print ("This node would be dead, Good bye")
        cv2.destroyAllWindows() #this is just an option



if __name__ == '__main__':
    try:
        listener = listener()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
