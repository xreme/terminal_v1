import machine
import input_drivers
import connection
import time


class RealTimeClock:
    
    def __init__(self, display, leds,beeper, inputs):
        self.rtc = machine.RTC()
        self.display = display
        self.leds = leds
        self.inputs = inputs
        self.beeper = beeper
        self.content = ''
    
    def get_date_time(self):
        return self.rtc.datetime()
    
    def get_nice_date_string(self, numerical_format):
        date_list = self.rtc.datetime()[:3]
        date_list = [int(num) for num in date_list]
        
        year,month,day = date_list
    
        if numerical_format:
            return str(f'{year:02d}'+'/'+f'{month:02d}'+'/'+f'{day:02d}')
        else:
            if month == 1:
                month_string = "Jan."
            elif month == 2:
                month_string = "Feb."
            elif month == 3:
                month_string = "Mar."
            elif month == 4:
                month_string = "Apr."
            elif month == 5:
                month_string = "May"
            elif month == 6:
                month_string = "June"
            elif month == 7:
                month_string = "July"
            elif month == 8:
                month_string = "Aug."
            elif month == 9:
                month_string = "Sept."
            elif month == 10:
                month_string = "Oct."
            elif month == 11:
                month_string = "Nov."
            else:
                month_string = "Dec."
        
            return str(month_string + f'{day:02d}' + ", " + f'{year:02d}')
    
    def get_time_string_nice(self,military):
        time_list = self.rtc.datetime()[4:7]
        
        time_list = [int(num) for num in time_list]
        
        hours, minutes, seconds = time_list
    
        if military:
            return str(f"{hours:02d}" + ':'+f"{minutes:02d}" +':'+ f"{seconds:02d}" )
        else:
            if hours > 12:
                hours = int(hours) - 12
                period = 'PM'
            elif hours == 12:
                period = 'PM'
            else:
                period = 'AM'
            return str(f"{hours:02d}" + ':'+f"{minutes:02d}" +':'+ f"{seconds:02d} "+ period)
    
    def get_date_array(self):
        date_list = self.rtc.datetime()[:3]
        date_list = [int(num) for num in date_list]
        return date_list
    def get_time_array(self):
        time_list = self.rtc.datetime()[4:7]
        time_list = [int(num) for num in time_list]

        return time_list

    def set_display(self,content):
        if (content != self.content):
            self.content = content
            self.display.clear()
            self.display.putstr(content)
        
    
    def run(self):
        self.set_display(self.get_nice_date_string(False) + '\n' + self.get_time_string_nice(False))