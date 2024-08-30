import machine
from machine import Pin
from time import ticks_ms, sleep
from ili9341 import Display, color565
from machine import Pin, SPI
from machine import Pin, ADC
from xglcd_font import XglcdFont
from machine import Pin
from machine import Pin, PWM
from hcsr04 import HCSR04
import tm1637
import utime
import time
from neopixel import Neopixel


# Sample code from https://github.com/rdagger/micropython-ili9341/blob/master/demo_shapes.py
PLAY_PIN = 2
button_play = Pin(PLAY_PIN, Pin.IN, Pin.PULL_UP)
PLAY_PIN2 = 3
button_play2 = Pin(PLAY_PIN2, Pin.IN, Pin.PULL_UP)

spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7))

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))

numpix = 8
strip = Neopixel(numpix, 1, 0, "GRB")

display.clear()

tm.numbers(00,00)
white = (255, 255, 225)
strip.fill(white)
strip.show()
display.fill_rectangle(50, 85, 130, 150, color565(94, 90, 96))  # head


display.fill_rectangle(70, 115, 30, 30, color565(246, 17, 147))  # Left eye
display.fill_rectangle(70, 175, 30, 30, color565(246, 17, 147))  # Right eye


display.fill_rectangle(135, 125, 20, 70, color565(10, 140, 186)) #mouth

# Ears
display.fill_rectangle(80, 235, 50, 10, color565(149, 7, 250))  # Left ear
display.fill_rectangle(80, 75, 50, 10, color565(149, 7, 250))  # Right ear

sleep(5)
display.clear()
font = XglcdFont('fonts/Unispace12x24.c', 12, 24)
font2 = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
display.draw_text(100, 200, 'Welcome!', font, color565(255, 255, 255))
sleep(3)
display.clear()
display.draw_text(90, 270, 'I am your study bot,', font, color565(255, 255, 255))
display.draw_text(120, 205, 'Gregory', font, color565(255, 255, 255))
sleep(3)



sleep(1)
# y- coordinate maximum = 319
screen_mode = 0
time_options = ["10 secs", "1 min", "20 mins", "30 mins", "45 mins", "1hr","1hr 30 mins", "2hrs", "2hr 15 mins", "2hr 30 mins", "3hrs"]
selected_time = ""

def display_study_mode():
    display.clear()
    display.draw_text(20, 300, "", font, color565(255, 255, 255))
    print("1")
    if (button_play2.value() == False):
        time_mode()
        yellow = (255, 100, 0)
        strip.fill(yellow)
        strip.show()
    else:
        yellow = (225, 100, 0)
        strip.fill(yellow)
        strip.show()
        return main_func()
    

def display_instructions():
    display.clear()
    display.draw_text(20, 300, "", font, color565(255, 255, 255))
    print("2")
    if (button_play2.value() == False):
        yellow = (225, 100, 0)
        strip.fill(yellow)
        strip.show()
        display_picture_mode()
    else:
        yellow = (225, 100, 0)
        strip.fill(yellow)
        strip.show()
        return main_func()

def time_mode():
    global time_options
    global selected_time
    display.clear()
    display.draw_text(100, 220, "PICK A TIME:" , font, color565(255, 255, 255))
    sleep(1.5)
    
    current_time_index = 0  # Start with the first option
    display_time_option(current_time_index)  # Display the initial option
    
    while True:  # Stay in time mode until a condition is met to exit
        lights2()
        if button_play.value() == 0:  # If Button 1 is pressed
            red = (236, 10, 10)
            strip.fill(red)
            strip.show()
            current_time_index = (current_time_index + 1) % len(time_options)  # Cycle through options
            display_time_option(current_time_index)  # Update display with the new option
            sleep(0.3)
          
        # Check for Button 2 press for a long press to return to Study Mode
        if button_play2.value() == 0:  # Button 2 pressed
            yellow = (225, 100, 0)
            strip.fill(yellow)
            strip.show()
            press_time = ticks_ms()  # Record the time when Button 2 was pressed
            while button_play2.value() == 0:  # Wait while Button 2 is held down
                if ticks_ms() - press_time > 1000:
                    inital()
                    # Long press detected (e.g., > 1000 ms)
                    # Perform actions to return to Study Mode
                    return  # Exit time_mode function to return to previous mode
            debounce(button_play2)  # Debounce after checking for long press
            selected_time = time_options[current_time_index]
            confirm_screen()
            
        


def confirm_screen():
    display.clear()
    lights2()
    display.draw_text(80, 300, "Are you sure you want to" , font, color565(255, 255, 255))
    message = f"study for {selected_time}?"
    
    
    if selected_time in ["1hr 30 mins", "2hr 15 mins", "2hr 30 mins"]:
        display.draw_text(110, 290, message, font, color565(255, 255, 255))
    else:
        display.draw_text(110, 260, message, font, color565(255, 255, 255))
    
    
    
    while True:
        if button_play2.value() == 0:  # Button 2 pressed
            yellow = (225, 100, 0)
            strip.fill(yellow)
            strip.show()
            display.clear()
            press_time = ticks_ms()  # Record the time when Button 2 was pressed
            while button_play2.value() == 0:  # Wait while Button 2 is held down
                if ticks_ms() - press_time > 1000:  # Long press detected (e.g., > 1000 ms)
                    return time_mode()
                
            debounce(button_play2)
            display.clear()
            collect_phone()
            surroundings_check()
            lights2()
            display.draw_text(90, 250, "Timer begins in:" , font, color565(255, 255, 255))
            sleep(1)
            
            number_display_area = (130, 165, 40, 50)  
            for i in range(5, 0, -1):
                display.fill_rectangle(*number_display_area, color565(0, 0, 0)) 
                display.draw_text(number_display_area[0], number_display_area[1], str(i), font, color565(255, 255, 255))
                sleep(1)

            display.clear()
            timer(selected_time)
            break

            
def collect_phone():
    sensor = HCSR04(trigger_pin=12, echo_pin=13)
    distance = sensor.distance_cm()
    while True:
        lights2()
        display.draw_text(80, 275, "Please put your phone", font, color565(255, 255, 255))
        display.draw_text(110, 255, "in the slot below.", font, color565(255, 255, 255))
        sleep(3)
        distance = sensor.distance_cm()
        print(distance)
        if distance < 7:
            display.clear()
            sleep(2)
            display.draw_text(110, 250, "Phone Collected.", font, color565(255, 255, 255))
            sleep(3)
            display.clear()
            display.draw_text(110, 295, "Commencing Study Mode...", font, color565(255, 255, 255))
            sleep(3)
            servo_set(1000, 6000)
            display.clear()
            break


def timer(selected_time):
    display.fill_rectangle(50, 85, 130, 150, color565(94, 90, 96))  # head


    display.fill_rectangle(70, 115, 30, 30, color565(246, 17, 147))  # Left eye
    display.fill_rectangle(70, 175, 30, 30, color565(246, 17, 147))  # Right eye


    display.fill_rectangle(135, 125, 20, 70, color565(10, 140, 186)) #mouth


    display.fill_rectangle(80, 235, 50, 10, color565(149, 7, 250))  # Left ear
    display.fill_rectangle(80, 75, 50, 10, color565(149, 7, 250))  # Right ear
    
    time_options = {"10 secs": 10, "1 min": 60, "20 mins": 1200, "30 mins": 1800, "45 mins": 2700, "1hr": 3600,"1hr 30 mins": 5400, "2hrs": 7200, "2hr 15 mins": 8100, "2hr 30 mins": 9000, "3hrs": 10800}
    for x in range(time_options[selected_time], 0, -1):
        minutes = x // 60
        seconds = x % 60
        #minutes = int(x / 60) % 60
        #hours = int(x / 3600)
        print(f"{minutes:02}:{seconds:02}")
        tm.numbers(minutes, seconds)
        sleep(1)
        
        
        if magnet() == True:
            tm.show("----")
            servo_reset(6000,1000)
            display.clear()
            display.draw_text(100, 319, "Please grab your phone from", font, color565(255, 255, 255))
            display.draw_text(125, 230, "from the slot.", font, color565(255, 255, 255))
            sleep(5)
            display.clear()
            display.draw_text(110, 225, "Resetting...", font, color565(255, 255, 255))
            sleep(3)
            inital()
            
            
            

    print("TIME'S UP!")
    reset()
    
    
               
def display_picture_mode():
    display.clear()
    display.draw_text(20, 300, "-Press the red button to", font, color565(255, 255, 255))
    display.draw_text(40, 300, "scroll", font, color565(255, 255, 255))
    display.draw_text(100, 300, "-Press the yellow button", font, color565(255, 255, 255))
    display.draw_text(120, 300, "to enter", font, color565(255, 255, 255))
    display.draw_text(180, 300, "-Press and hold the", font, color565(255, 255, 255))
    display.draw_text(200, 300, "yellow button to cancel", font, color565(255, 255, 255))
    lights2()
    while True:
        if button_play2.value() == 0:  # Button 2 pressed
            yellow = (225, 100, 0)
            strip.fill(yellow)
            strip.show()
            display.clear()
            press_time = ticks_ms()  # Record the time when Button 2 was pressed
            while button_play2.value() == 0:  # Wait while Button 2 is held down
                if ticks_ms() - press_time > 1000:  # Long press detected (e.g., > 1000 ms)
                    inital()
                    #return display_instructions()

        sleep(0.1)  # Small delay to reduce CPU usage
    
        
    
def display_time_option(index):
    """Display the selected time option."""
    display.clear()
    selected_time = time_options[index]  # Get the selected time option
    display.draw_text(100, 200, selected_time, font, color565(255, 255, 255))
    
def debounce(button):
    """Debounce a button press."""
    sleep(0.3)  # Wait for the bouncing to stop
    while button.value() == 0:  # Wait for the button to be released
        pass
def inital():
    tm.numbers(00,00)
    servo_reset(6000, 1000)
    white = (255, 255, 225)
    strip.fill(white)
    strip.show()
    main_func()
    
def main_func():
    global screen_mode
    time_mode_active = False  # Flag to track whether time mode is active
    display.clear()
    display.fill_rectangle(100, 180, 30, 120, color565(255, 0, 255))
    display.fill_rectangle(100, 30, 30, 120, color565(255, 0, 255))
    display.draw_text(70, 150, "Study mode", font, color565(255, 255, 255))
    display.draw_text(70, 315, "Instructions", font, color565(255, 255, 255))
    lights2()
    while True:
        lights2()
        if button_play.value() == 0:
            red = (236, 10, 10)
            strip.fill(red)
            strip.show()
            if time_mode_active:  # If currently in time mode, go back to study mode
                time_mode_active = False
                
            else:  # Toggle between study mode and instructions
                screen_mode = not screen_mode
                if screen_mode:
                    print('hello')
                    display.fill_rectangle(100, 180, 30, 120, color565(150, 0, 100))
                    display.fill_rectangle(100, 30, 30, 120, color565(255, 0, 255))
#                   display_instructions()
                   
                else:
                    print('bye')
                    display.fill_rectangle(100, 180, 30, 120, color565(255, 0, 255))
                    display.fill_rectangle(100, 30, 30, 120, color565(150, 0, 100))
#                     display_study_mode()

            sleep(0.3)  # Debounce delay

        elif button_play2.value() == 0 and not time_mode_active:
            yellow = (255, 100, 0)
            strip.fill(yellow)
            strip.show()
            debounce(button_play2)  # Debounce delay
            if screen_mode == 1:  # Check if we are in Instructions screen
                display_picture_mode()  # Display picture menu
            elif screen_mode == 0:  # In Study Mode, transition to Time Mode
                time_mode_active = True
                time_mode()

        #sleep(0.1)

        elif button_play2.value() == 0:
            yellow = (225, 100, 0)
            strip.fill(yellow)
            strip.show()
            press_time = ticks_ms()
            sleep(0.1)  # Debounce
            while button_play2.value() == 0:  # Wait for release
                if ticks_ms() - press_time > 1000:  # Long Press Detected
                    if time_mode_active:  # If in Time Mode, return to Study Mode
                        time_mode_active = False
                        display_study_mode()
                        break
            
        
def surroundings_check():
    soundSensor = ADC(28) # Pin where sensor device (Microphone) is connected
    baseline = 25000 # You may need to change this, but your mic should be reading around here as a baseline. 
    variability = 0.1
    check = False
    check2 = False
    
    while True:
        print(soundSensor.read_u16())
    
    # If we detect a spike in the waveform greater than a 10% deviation from our baseline, someone is probably talking.
        if soundSensor.read_u16() > (baseline + baseline*variability) or soundSensor.read_u16() < (baseline - baseline*variability):
            check = True
            break
        else:
            print("break1")
            break
        sleep(0.01)
        
    ldr = machine.ADC(27)  # Initialize an ADC object for pin 27

    while True:
        ldr_value = ldr.read_u16()  # Read the LDR value and convert it to a 16-bit unsigned integer
        print("LDR Value:", ldr_value)  # Print the LDR value to the console
        if ldr_value > 500:
            check2 = True
            break
        else:
            print("break2")
            break
            
    if check and check2:
        display.draw_text(10, 300, "The noise is loud here, you should move", font2, color565(255, 255, 255))
        display.draw_text(30, 225, "to a different room", font2, color565(255, 255, 255))
        
        display.draw_text(80, 280, "The light quality is poor here, you", font2, color565(255, 255, 255))
        display.draw_text(100, 300, " should move somewhere with more light", font2, color565(255, 255, 255))
        
        display.draw_text(150, 285, "Please press enter to ", font, color565(255, 255, 255))
        display.draw_text(180, 290, "confirm you have noted", font, color565(255, 255, 255))
        display.draw_text(210, 265, "these suggestions", font, color565(255, 255, 255))
        while True:
            if button_play2.value() == 0:
                yellow = (225, 100, 0)
                strip.fill(yellow)
                strip.show()
                debounce(button_play2)
                break
            sleep(0.1)
    elif check:
        display.draw_text(40, 300, "The noise is loud here, you should move", font2, color565(255, 255, 255))
        display.draw_text(60, 225, "to a different room", font2, color565(255, 255, 255))
        
        display.draw_text(110, 285, "Please press enter to ", font, color565(255, 255, 255))
        display.draw_text(140, 290, "confirm you have noted", font, color565(255, 255, 255))
        display.draw_text(170, 265, "these suggestions", font, color565(255, 255, 255))
        while True:
            if button_play2.value() == 0:
                yellow = (225, 100, 0)
                strip.fill(yellow)
                strip.show()
                debounce(button_play2)
                break
            sleep(0.1)
    elif check2:
        display.draw_text(40, 280, "The light quality is poor here, you", font2, color565(255, 255, 255))
        display.draw_text(60, 300, " should move somewhere with more light", font2, color565(255, 255, 255))
        
        display.draw_text(110, 285, "Please press enter to ", font, color565(255, 255, 255))
        display.draw_text(140, 290, "confirm you have noted", font, color565(255, 255, 255))
        display.draw_text(170, 265, "these suggestions", font, color565(255, 255, 255))
        while True:
            if button_play2.value() == 0:
                yellow = (225, 100, 0)
                strip.fill(yellow)
                strip.show()
                debounce(button_play2)
                break
            sleep(0.1)
    else:
        print("still continue")
    display.clear()
    
    
    
def servo_set(start, end):
    pwm = PWM(Pin(9))
    pwm.freq(50)
    
    for position in range(start, end, 15):
        pwm.duty_u16(position)
        sleep(0.01)
    return (None, None)

def servo_reset(end, start):
    pwm = PWM(Pin(9))
    pwm.freq(50)
    
    for position in range(end, start, -15):
        pwm.duty_u16(position)
        sleep(0.01)
    return (None, None)
    
def reset():
   
    tm.numbers(00, 00)
    display.clear()
    display.draw_text(100, 265, "You are finished!!", font, color565(255, 255, 255))
    servo_reset(6000,1000)
    display.clear()
    display.draw_text(100, 280, "You can retrieve your", font, color565(255, 255, 255))
    display.draw_text(120, 205, "phone now", font, color565(255, 255, 255))
    sleep(5)
    display.clear()
    display.draw_text(75, 308, "Use the switch to turn off", font, color565(255, 255, 255))
    display.draw_text(100, 170, "OR", font, color565(255, 255, 255))
    display.draw_text(125, 285, "Press enter to restart", font, color565(255, 255, 255))
    lights()
    while True:
        if button_play2.value() == 0:# Button 2 pressed
            yellow = (255, 100, 0)
            strip.fill(yellow)
            strip.show()
            display.clear()
            display.draw_text(110, 230, "Restarting...", font, color565(255, 255, 255))
            sleep(5)
            inital()

            
def magnet():
    switch = Pin(1, Pin.IN)
    led = Pin('LED', Pin.OUT)

    if switch.value() == 1:  # Check if the button is pressed
        led.value(1)# Turn on the LED
        return True
        
    else:
        led.value(0)  # Turn off the LED
        return False
       
    
    print(switch.value())
    time.sleep(1)  # Short delay to reduce CPU usage

            
def lights():

    red = (255, 0, 0)
    orange = (255, 50, 0)
    yellow = (255, 100, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    indigo = (100, 0, 90)
    violet = (200, 0, 100)
    colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

    # same colors as normaln rgb, just 0 added at the end
    colors_rgbw = [color+tuple([0]) for color in colors_rgb]
    colors_rgbw.append((0, 0, 0, 255))

    # uncomment colors_rgbw if you have RGBW strip
    colors = colors_rgb
    colors = colors_rgbw


    step = round(numpix / len(colors))
    current_pixel = 0
    strip.brightness(20)

    for color1, color2 in zip(colors, colors[1:]):
       strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
       current_pixel += step

    strip.set_pixel_line_gradient(current_pixel, numpix - 1, violet, red)
    
  
    while True:
        strip.rotate_left(1)
        time.sleep(0.1)
        strip.show()
        if button_play2.value() == 0:# Button 2 pressed
            button_play2.value() == 0
            break
        
def lights2():
    # Your initial setup for colors
    red = (255, 0, 0)
    orange = (255, 50, 0)
    yellow = (255, 100, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    indigo = (100, 0, 90)
    violet = (200, 0, 100)
    colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

    # Adjust for RGBW if needed
    colors_rgbw = [color + (0,) for color in colors_rgb]
    colors_rgbw.append((0, 0, 0, 255))
    # Uncomment the following line if you have an RGBW strip
    # colors = colors_rgbw

    # Assuming you're using an RGB strip
    colors = colors_rgb

    step = round(numpix / len(colors))  # Calculate step size
    current_pixel = 0
    strip.brightness(20)  # Set brightness

    # Set gradient colors on the strip
    for color1, color2 in zip(colors, colors[1:]):
        strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
        current_pixel += step

    # Set the last gradient segment manually to loop back to the start color
    strip.set_pixel_line_gradient(current_pixel, numpix - 1, colors[-1], colors[0])

    # Remove the rotation loop to prevent motion
    # Display the setup without changing it
    strip.show()
            
    
    
      
    #if lights == ""     

if __name__ == "__main__":
    inital()
        
    
