from base import *


class Console:


    def __init__(self,hz):
        
        rospy.init_node("console")

        self.rate = rospy.Rate(hz)

        self.pubConsoleInput = rospy.Publisher("console_input", Joy, queue_size=1)

    
    def _keyboardInputEvent(self, key):

        msg = Joy()
        msg.buttons = [0,0,0,0,0,0,0,0,0,0,0,0]

        try:

            if key == kb.Key.up:

                msg.buttons[4] = 1
                self.pubConsoleInput.publish(msg)

            elif key == kb.Key.down:

                msg.buttons[0] = 1
                self.pubConsoleInput.publish(msg)
            
            elif key == kb.Key.right:

                msg.buttons[1] = 1
                self.pubConsoleInput.publish(msg)

            elif key == kb.Key.left:

                msg.buttons[3] = 1
                self.pubConsoleInput.publish(msg)

            elif key == kb.Key.esc:
        
                msg.buttons[7] = 1
                self.pubConsoleInput.publish(msg)

        except AttributeError:  pass


    def run(self):

        keyIOhandler = kb.Listener(on_press=self._keyboardInputEvent)
        keyIOhandler.start()

        while not rospy.is_shutdown():

            self.rate.sleep()



if __name__ == "__main__":

    console = Console(10)

    console.run()