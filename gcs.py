from base import *


class GCS:


    def __init__(self,hz):
        
        rospy.init_node("gcs")

        self.rate = rospy.Rate(hz)

        self.subActionDisplay = rospy.Subscriber("action_",String,self._callback_action_display)

        self.action_input = None


    def _callback_action_display(self,msg):

        self.action_input = msg.data


    def run(self):

        while not rospy.is_shutdown():

            self.rate.sleep()



if __name__ == "__main__":

    gcs = GCS(60)
    gcs.run()