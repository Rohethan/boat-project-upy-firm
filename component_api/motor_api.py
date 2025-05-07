from machine import Pin, PWM
from libraries.counter import Counter
import utime

import config




class PIDController:
    def __init__(self, Kp, Ki, Kd, min_output=0, max_output=100):
        """
        Initializes a PID controller.

        Args:
            Kp: Proportional gain.
            Ki: Integral gain.
            Kd: Derivative gain.
            min_output: Minimum output value (e.g., -100 for -100% PWM).
            max_output: Maximum output value (e.g., 100 for 100% PWM).
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.min_output = min_output
        self.max_output = max_output
        self.integral = 0
        self.previous_error = 0


    def compute(self, setpoint, current_value, dt):
        """
        Calculates the control output based on the PID algorithm.

        Args:
            setpoint: The desired value.
            current_value: The current measured value.
            dt: The time elapsed since the last computation (in seconds).

        Returns:
            The control output.
        """
        error = setpoint - current_value

        # Proportional term
        proportional = self.Kp * error

        # Integral term
        self.integral += error * dt
        integral = self.Ki * self.integral

        # Derivative term
        derivative = self.Kd * (error - self.previous_error) / dt

        # Total output
        output = proportional + integral + derivative

        # Clamp the output to the specified range
        output = max(self.min_output, min(output, self.max_output))

        # Store the current error for the next derivative calculation
        self.previous_error = error

        return output



class PropulsionSystem:

    def __init__(self, in1, in2, ena, in3, in4, enb, hsL, hsR):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.ena = PWM(ena, freq=1000, duty=0)
        self.in3 = Pin(in3, Pin.OUT)
        self.in4 = Pin(in4, Pin.OUT)
        self.enb = PWM(enb, freq=1000, duty=0)

        self.hsL = Pin(hsL, Pin.IN)
        self.hsR = Pin(hsR, Pin.IN)

        self.left_rotation_counter = Counter(hsL)
        self.right_rotation_counter = Counter(hsR)
        rn_time = utime.ticks_ms()
        self.lrc_time = rn_time
        self.rrc_time = rn_time

        self.thrust_power = 0
        self.thrust_ratio = 0.5


        self.PIDctrl_L = PIDController(config.PID_P, config.PID_I, config.PID_D, min_output=0, max_output=65535)
        self.PIDctrl_R = PIDController(config.PID_P, config.PID_I, config.PID_D, min_output=0, max_output=65535)

        self.in1.on()
        self.in2.off()
        self.in3.on()
        self.in4.off()
        self.ena.duty_u16(0)
        self.enb.duty_u16(0)
        self.last_motor_update = utime.ticks_ms()

    def calculate_rpms(self):
        # time sensitive stuff kinda here?
        l_ctr_val = self.left_rotation_counter.count
        r_ctr_val = self.right_rotation_counter.count
        rn_time = utime.ticks_ms()
        self.left_rotation_counter.count = 0
        self.right_rotation_counter.count = 0

        # time delta and adjustments
        l_delta_t = (rn_time - self.lrc_time) /1000 # direct to second conversion here, a bit faster ops.
        r_delta_t = (rn_time - self.rrc_time) /1000
        self.lrc_time = rn_time
        self.rrc_time = rn_time

        l_rpm = (l_ctr_val / l_delta_t)*60
        r_rpm = (r_ctr_val / r_delta_t)*60
        return l_rpm, r_rpm


    def update_thrust_ratios(self, turn_ratio, power_ratio):
        """
        :param turn_ratio: 0% = full left, 100% = full right
        :param power_ratio: 100% is max rpm on both motors
        :return:
        """
        self.thrust_ratio = turn_ratio
        self.thrust_power = power_ratio


    def update_motors(self):
        rpm_l, rpm_r = self.calculate_rpms()
        print("RPMs : ", rpm_l, rpm_r)
        target_rpm_l = config.MOTOR_MAX_RPM * self.thrust_ratio * self.thrust_power
        target_rpm_r = config.MOTOR_MAX_RPM * (1 - self.thrust_ratio) * self.thrust_power

        dt = utime.ticks_ms() - self.last_motor_update
        ctrl_L = self.PIDctrl_L.compute(target_rpm_l, rpm_l, dt)
        ctrl_R = self.PIDctrl_R.compute(target_rpm_r, rpm_r, dt)
        self.last_motor_update = utime.ticks_ms()

        self.ena.duty_u16(int(ctrl_L))
        self.enb.duty_u16(int(ctrl_R))


    def motor_task(self):
        while True:
            self.update_motors()
            print("MOTORS TICK")
            utime.sleep_ms(300)


