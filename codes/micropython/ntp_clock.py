import time
import ntp_client
import led
import gc
import config
import bus_timer


class Clock():
    
    def __init__(self, display, buzzer = None, led_high_is_on = False):        
        self.adjusted_time_delta = 0
        self.display = display
        self.buzzer = buzzer if buzzer else led.on_board_led
        self.led_high_is_on = led_high_is_on
        ntp_client.calibrate_time_upython() 
        
        
    def show_current_time(self):
        current_time = time.localtime()
        print(current_time)        
        year, month, day, hour, minute, second, _, _ = current_time 
        
        self.display.show_time(year, month, day, hour, minute, second)
        
        self._on_hour(hour, minute, second)
        
        
    def _on_hour(self, hour, minute, second): 
        
        if minute == second == 0: 
            print("\n[Clock: now is {} o'clock]\n".format(hour))

            times_to_signal = hour % 12
            if times_to_signal == 0: times_to_signal = 12

            led.blink(self.buzzer, 
                      times = times_to_signal - 1, on_seconds = 0.1, off_seconds = 0.9, 
                      high_is_on = self.led_high_is_on)
            led.blink(self.buzzer, 
                      times = 1, on_seconds = 0.5, off_seconds = 0.5, 
                      high_is_on = self.led_high_is_on)   
            
            ntp_client.calibrate_time_upython()
        
        
    def adjust_time_delta(self, start_time, end_time, targeted_difference = 1000):
        time_delta = end_time - start_time - targeted_difference
        time_delta = time_delta if 0 < abs(time_delta) < targeted_difference else 0
        self.adjusted_time_delta += time_delta / 3

    
    def show_timer(self):
        minutes_left = bus_timer.query_minutes_left(route_id = config.route_id, 
                                                    route_direction = config.route_direction, 
                                                    bus_stop_code = config.bus_stop_code)
                                                    
        self.display.show_text('{0:4s}  {1:>2s}'.format(config.route_id, minutes_left) )
            
            
    def refresh_timer(self, on_second = 45):
        current_time = time.localtime()
        print(current_time)        
        year, month, day, hour, minute, second, _, _ = current_time  
        
        if second == on_second:
            self.show_timer()
        
        if self.display.exec_command(self.display.read_keys()[0]):
            self.show_timer()
            
        self._on_hour(hour, minute, second) 
        
        
    def run(self):
        adjusted_time_delta = 0
        self.show_timer()
        
        while True:
            start_time = time.ticks_ms()             
            
            self.refresh_timer() 
            
            gc.collect()
            print('[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc())) 
            time.sleep(1 - (self.adjusted_time_delta / 1000))
            
            end_time = time.ticks_ms()
            self.adjust_time_delta(start_time, end_time)
            print('cycle time (ms):{}\n'.format(end_time - start_time))