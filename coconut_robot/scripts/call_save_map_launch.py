#!/usr/bin/env python 

import rospy
import roslaunch
from os.path import expanduser
from std_msgs.msg import String

home = expanduser("~")

# filename = 'test'

def save_map_start():		
	filename = rospy.get_param("/map_name", 'test')
	uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
	roslaunch.configure_logging(uuid)
	cli_args = ['{}/coconut_ws/src/coconut_uvc_slam/launch/save_map.launch'.format(home), "filename:={}".format(filename)]
	roslaunch_args = cli_args[1:]
	roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]
	parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
	parent.start()


class call_launch_subscriber(object):

	def __init__(self):
		rospy.init_node('call_save_map_launch_node', anonymous=True)
		self.call_launch_command = None

	def callback(self,data):
		self.call_launch_command = data.data

	def listener(self):
		rospy.Subscriber('call_launch', String, self.callback)


if __name__=="__main__":
	launchSub_node = call_launch_subscriber()
	launchSub_node.listener()
	r = rospy.Rate(10)
	try:
		while(not rospy.is_shutdown()):
			command = launchSub_node.call_launch_command
			if command == "save_map":
				save_map_start()
				launchSub_node.call_launch_command = None
			r.sleep()
	except Exception as e:
		print(e)