from base import *


class Planner:


    def __init__(self,hz):
        
        rospy.init_node("planner")

        self.rate = rospy.Rate(hz)

        self.subControlInput = rospy.Subscriber("console_input_",Int16,self._callback_control_input)

        self.pubActionInput = rospy.Publisher("action",String,queue_size=1)

        self.control_input = None

        self.state          = "state1"

        self.states         = {}

        self.states["state1"] = State1(self)
        self.states["state2"] = State2(self)
        # ...

    
    def _callback_control_input(self, msg):

        print(f"control input : {msg.data}")
        self.control_input = msg.data


    def run(self):

        while not rospy.is_shutdown():

            self.states[self.state].transition()

            self.rate.sleep()



class State:

    def __init__(self, planner):

        self.planner = planner

    def transition(self):
        
        ### state transition ###

        pass
    


class State1(State):

    def __init__(self, planner):
        super().__init__(planner)

    def transition(self):
        
        print("state1")
        self.planner.pubActionInput.publish("0")
        ### state transition ###

        pass



class State2(State):

    def __init__(self, planner):
        super().__init__(planner)

    def transition(self):
        
        ### state transition ###

        pass



if __name__ == "__main__":

    planner = Planner(10)
    planner.run()