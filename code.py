import board
from digitalio import DigitalInOut, Direction, Pull
import time

import displayio
display = board.DISPLAY
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

board.DISPLAY.brightness=1

font = bitmap_font.load_font("/Junction-regular-24.bdf")

label.anchor_point = (0.5, 0.5)
# Create the text label

text = label.Label(font, text="", color=0xFFFFFF)
text.scale=2
# Set the location
#text_area.x = display.width // 2
#text_area.y = display.height // 2
text.x=10
text.y=30

morsecode = label.Label(font, text="", color=0xE9FF7B)
morsecode.scale=2
# Set the location
#text_area.x = display.width // 2
#text_area.y = display.height // 2
morsecode.x=10
morsecode.y=110

# Show it
main_group = displayio.Group()
main_group.append(text)
main_group.append(morsecode)

display.root_group = main_group

btn = DigitalInOut(board.BUTTON1)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

btn2 = DigitalInOut(board.BUTTON0)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP

prev_state = btn.value
prev_state2 = btn2.value

pressed_time=0
released_time=0

code_dict={
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z"
}

while True:
    pressed_time+=1
    if released_time > 0:
        released_time+=1
    if released_time>30000:
        text.text=text.text+code_dict.get(morsecode.text,"")
        morsecode.text=""
        released_time=0
    
    cur_state = btn.value
    if cur_state != prev_state:
        if not cur_state:
            # BTN DOWN
            pressed_time = 0
        else:
            # BTN UP
            #print(pressed_time)
            if pressed_time<10000:
                morsecode.text = morsecode.text+"."
            else:
                morsecode.text = morsecode.text+"-"
            morsecode.x = display.width - len(morsecode.text)*20
            pressed_time=0
            released_time=1
    prev_state = cur_state
    
    cur_state2 = btn2.value
    if cur_state2 != prev_state2:
        if not cur_state2:
            # BTN2 DOWN
            text.text=""
        else:
            # BTN2 UP
            pass
    prev_state2 = cur_state2
