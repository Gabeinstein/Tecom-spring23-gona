#! /usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None

def callback_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[0:2]), 10),
        'front':  min(min(msg.ranges[3:5]), 10),
        'left':   min(min(msg.ranges[6:9]), 10)
    }
    take_action(regions)

def take_action(regions):
    threshold_dist = 2 #Distancia a la cual comienza a reaccionar el movil
    linear_speed = 0.7 #Velocidad estandar para el movil
    angular_speed = 1 #Cambio angular que se le da para reaccion

    msg = Twist()
    linear_x = 0
    angular_z = 0


    if regions['front'] < threshold_dist and regions['right'] < threshold_dist :
        linear_x = 0.3
        angular_z = -angular_speed
        rospy.loginfo(regions)
    elif regions['right'] > threshold_dist:
        linear_x = 0.3
        angular_z = angular_speed
        rospy.loginfo(regions)
    elif regions['front'] > threshold_dist and regions['right'] < threshold_dist :
        linear_x = linear_speed
        angular_z = 0
        rospy.loginfo(regions)
    else:
        rospy.loginfo("unknown case")

    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub
    rospy.init_node('car2')

    pub = rospy.Publisher('/car2/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/car2/laser/scan', LaserScan, callback_laser)
    rospy.spin()

if __name__ == '__main__':
    main()