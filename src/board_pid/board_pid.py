import time

class BoardPid:

    """ Implementation of PID
    """

    def __init__(self,
        kp=0,                   # proportional gain
        ki=0,                   # integral gain
        kd=0,                   # derivative gain
        target=0,               # target value
        derivative_window=1,    # number of previous calls to average error change rate over
        timeout=None,           # optionally sets a timeout which resets integral error if exceeded
        int_max=None,           # optionally sets a maximum integral error, to prevent wind-up
        out_max=None,            # optionally sets a maximum controller output
        in_max=None,
        halt_out=0
    ):

        """ 
        Initialization function 
        INPUTS:
            kp=0 ~ proportional gain                 
            ki=0 ~ integral gain           
            kd=0 ~ derivative gain               
            target=0 ~ target setpoint   
            derivative_window=1 ~ previous calls over which to average derivative 
            timeout=None ~ timeout to reset integral          
            int_max=None ~ maximum integral
            out_max=None ~ maximum output
            in_max=None ~ maximum input
            halt_out=0 ~ "rest" output
        OUTPUTS:
            PID object

        """

        # sets PID coefficients
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # inits controller values
        self.int = 0 
        self.target = target
        self.err_last = 0
        self.last_time = time.time()
        self.edot_hist = [0]*derivative_window
        self.timeout=timeout
        self.int_max = int_max
        self.out_max = out_max
        self.in_max = in_max
        self.halt_out = halt_out

    def get(self, val):

        """ 
        Gets PID output
        INPUTS:
            val ~ current process sensor value
        OUTPUTS:
            out ~ actuator output

        """

        # Gets new output based on current sensor 

        # Halts if position is out of range
        if not self.in_max is None:
            if val > self.in_max or val < -self.in_max:
                return self.halt_out

        # get timestep since last controller call
        cur_time = time.time()
        dt = cur_time - self.last_time
        self.last_time = cur_time

        # get new error between current sensor value and target
        err = self.target-val 

        # update integral of error assuming error changes linearly between calls
        self.int = self.int+(err*dt)/2 

        # if a maximum integral error is set, makes sure maximum integral error is not
        # exceeded to prevent windup
        if not self.int_max is None:
            self.int = min(self.int_max, max(-self.int_max, self.int))

        # if maximum timestep is set and exceeded, resets integral error to prevent
        # large integral errors
        if not self.timeout is None:
            if dt > self.timeout:
                self.int = 0

        # calculates error change rate since last controller call
        derr = (err-self.err_last)/dt

        # averages error change rate over last n controller calls to smooth velocity
        self.edot_hist.pop(-1)
        self.edot_hist.insert(0, derr)
        edot = sum(self.edot_hist)/len(self.edot_hist)

        # stores current error for comparison in next controller call
        self.err_last = err

        # calculates PID value
        out = self.kp*err + self.ki*self.int + self.kd*edot 

        # if maximum output is set, clamps output so that the maximum output is not exceeded
        if not self.out_max is None:
            out = min(self.out_max, max(-self.out_max, out))

        # returns controller values
        return out
 
    def set_target(self, target):
        """ 
        Sets PID target
        INPUTS:
            target ~ new target
        OUTPUTS:
            none
        """
        self.target = target # sets new target setpoint

    def set_gains(self, kp=None, ki=None, kd=None):
        """ 
        Sets PID gains
        INPUTS:
            kp=None ~ proportional gain
            ki=None ~ integral gain
            kd=None ~ derivative gain  
        OUTPUTS:
            none
        """
        if not kp is None:
            self.kp = kp
        if not ki is None:
            self.ki = ki
        if not kd is None:
            self.kd = kd


