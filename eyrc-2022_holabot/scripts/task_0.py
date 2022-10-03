#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_0.py
# Functions:
# 					[ Comma separated list of functions in this file ]
# Nodes:		    Add your publishing and subscribing node


####################### IMPORT MODULES #######################
import sys
import traceback
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import sqrt,pi,atan2
##############################################################


################# ADD GLOBAL VARIABLES HERE #################

linear_vel = 1.0
angular_vel = 1.0

##############################################################

class TurtleBot:

    #global variables
    motion = ""
    bool_linear = False

    def __init__(self):

        rospy.init_node('turtlesim_node', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.callback)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    #callback function
    def callback(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        global bool_linear
        self.pose = data
        self.pose.x = round(self.pose.x,4)
        self.pose.y = round(self.pose.y,4)
        print(f"My turleBot is: {motion} \n{self.pose.theta:.2f}")
        if data.theta < -pi/2:
            bool_linear = True

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        goal_pose.x = self.pose.x
        goal_pose.y = self.pose.y - 2

        distance_tolerance = 0.001

        global motion       
        motion = "Moving straight!!!"

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:

            # Linear velocity in the x-axis.
            vel_msg.linear.x = 1
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
    
    def semi_circle(self):
        global bool_linear,motion
        motion = "Moving in a circle!!"

        goal_pose = Pose()
        goal_pose.x = self.pose.x
        goal_pose.y = self.pose.y
        goal_pose.theta = self.pose.theta
        vel_msg = Twist()
        vel_msg.linear.x = linear_vel
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = angular_vel
        while not bool_linear:
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

    def setDesiredOrientation(self, desired_angle_radians):
        global motion
        motion = "Rotating!"
        tolerence = 0.000001
        vel_msg = Twist()
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        if desired_angle_radians-self.pose.theta < 0:
            vel_msg.angular.z = -abs(angular_vel)
        else:
            vel_msg.angular.z = abs(angular_vel)
        while not (desired_angle_radians-self.pose.theta < tolerence):
            self.velocity_publisher.publish(vel_msg)

        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        

#main function
def main():
    input()
    turtle = TurtleBot()
    turtle.semi_circle()
    turtle.setDesiredOrientation(-pi/2)
    turtle.move2goal()
    rospy.signal_shutdown("Done!!")
    print("Done!!")

        









######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")

