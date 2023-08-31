from base import *


class Communicator:


    def __init__(self,hz):
        
        rospy.init_node("communicator")
        
        self.rate = rospy.Rate(hz)

        self.subConsoleInput    = rospy.Subscriber("console_input", Int16, self._callback_console_input)
        self.subAction          = rospy.Subscriber("action", String, self._callback_action)
        self.pubConsoleInput    = rospy.Publisher("console_input_", Int16, queue_size=1)
        self.pubAction          = rospy.Publisher("action_",String, queue_size=1)

        self.console_input      = None
        self.action             = None
    

    def _callback_console_input(self, msg): 
        
        print(f"console input : {msg.data}")
        self.console_input = msg.data


    def _callback_action(self, msg):        
        
        print(f"action : {msg.data}")
        self.action = msg.data


    def run(self):

        while not rospy.is_shutdown():

            try:

                self.pubConsoleInput.publish(self.console_input)
                self.pubAction.publish(self.action)

            except: pass

            self.rate.sleep()



if __name__ == "__main__":

    communicator = Communicator(60)
    communicator.run()