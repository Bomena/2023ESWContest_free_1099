from base import *

ESC_ASCII_VALUE = 0x1b
FORWARD = 0x77
BACKWARD = 0x78
LEFT = 0x61
RIGHT = 0x64
STOPS = 0x73
NONE = 0x70


class Controller:


    def __init__(self, hz):
        
        rospy.init_node("controller")

        self.rate = rospy.Rate(hz)

        self.subActionInput     = rospy.Subscriber("action",String,self._callback_action_input)
        self.subConsoleInput    = rospy.Subscriber("console_input", Joy, self._callback_joy)
        # self.subConsoleInput    = rospy.Subscriber("joy", Joy, self._callback_joy)
        self.pubCommandVel      = rospy.Publisher('/dynamixel_workbench/cmd_vel', Twist, queue_size=10)


        self.action_input = None

        self.shared = {'cmd':FORWARD}
        
        self.data_received = False


    def _callback_action_input(self,msg):

        self.action_input = msg.data


    def _callback_joy(self,msg):

        forward = 0
        backward = 0
        left = 0
        right = 0
        stop = 0
        self.shared['cmd'] = None

        forward = msg.buttons[4]
        backward = msg.buttons[0]
        left = msg.buttons[3]
        right = msg.buttons[1]
        stop = msg.buttons[7]
        
        if forward == 1:
            self.shared['cmd'] = FORWARD
            self.data_received = True
        elif backward == 1:
            self.shared['cmd'] = BACKWARD
            self.data_received = True
        elif left == 1:
            self.shared['cmd'] = LEFT
            self.data_received = True
        elif right == 1:
            self.shared['cmd'] = RIGHT
            self.data_received = True
        elif stop == 1:
            self.shared['cmd'] = STOPS
            self.data_received = True
        #else:
        #    self.shared['cmd'] = NONE
        #print(f"forward: {forward} backward: {backward}\n\
        #        left: {left} right: {right}")
        
        print(f"cmd: {self.shared['cmd']}")


    def getch(self):

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    def kbhit(self):
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
        
            tty.setcbreak(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        
        finally:
        
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if ch != '':
        
            return True
        
        else:
        
            return False


    def run(self):

        lin_vel_step = 0.01
        ang_vel_step = 0.1
        prev_c = STOPS

        rospy.loginfo("You can set '-lin_vel_step' and  '-ang_vel_step' arguments (default is 0.01 and 0.1)")

        if len(sys.argv) > 1:
            lin_vel_step = float(sys.argv[1])
            ang_vel_step = float(sys.argv[2])

        twist_msg = Twist()
        i = 0
        msg = "\n\
        Control Your Mobile Robot! \n\
        --------------------------- \n\
        Moving around:\n\
                w\n\
            a    s    d\n\
                x\n\
        \n\
        w/x : increase/decrease linear velocity\n\
        a/d : increase/decrease angular velocity\n\
        \n\
        s : force stop\n\
        \n\
        CTRL-C to quit\n\
        "

        rospy.loginfo(msg)

        rate = rospy.Rate(30)

        while not rospy.is_shutdown():
            
            if self.data_received == True:
                c = self.shared['cmd']
            # c != '':
                #c = getch()
                #c = self.shared['cmd']
            # print(f"c: {c}")
                if c == FORWARD:
                    
                    print(f"in forward")
                    
                    if prev_c != FORWARD:
                    
                        twist_msg.linear.x = 0.0
                        twist_msg.angular.z = 0.0
                    
                    else:
                    
                        twist_msg.linear.x += lin_vel_step
                
                elif c == BACKWARD:
                
                    if prev_c != BACKWARD:
                
                        twist_msg.linear.x = 0.0
                        twist_msg.angular.z = 0.0
                
                    else:
                
                        twist_msg.linear.x -= lin_vel_step
                
                elif c == LEFT:
                
                    twist_msg.linear.x = 0.0
                
                    if prev_c != LEFT:
                
                        twist_msg.angular.z = 0.0
                
                    else:
                
                        twist_msg.angular.z += ang_vel_step
                
                elif c == RIGHT:
                
                    twist_msg.linear.x = 0.0
                
                    if prev_c != RIGHT:
                
                        twist_msg.angular.z = 0.0
                
                    else:
                
                        twist_msg.angular.z -= ang_vel_step
                
                elif c == STOPS:
                
                    twist_msg.linear.x = 0.0
                    twist_msg.angular.z = 0.0
            
            # elif c == NONE:
            
            #     twist_msg.linear.x = twist_msg.linear.x
            #     twist_msg.angular.z = twist_msg.angular.z
            
            # c = self.shared['cmd'] = NONE
            # twist_msg.linear.x = twist_msg.linear.x
            # twist_msg.angular.z = twist_msg.angular.z   
                
                prev_c = c
            
                self.data_received = False
            
            i += 1
            print("i :", i)
            print(twist_msg)
            
            self.pubCommandVel.publish(twist_msg)

            rate.sleep()
            


if __name__ == "__main__":

    controller = Controller(60)

    Activate_Signal_Interrupt_Handler()
    
    try:
        controller.run()
    
    except rospy.ROSInterruptException:
        pass