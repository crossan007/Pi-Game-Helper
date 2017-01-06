import math  
import random
import time
import os 
import Adafruit_SSD1306
import RPi.GPIO as GPIO  
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import atexit

def exit_handler():
    print "exiting"
    disp.clear()
    GPIO.cleanup()

def renderDie(number, dimensions):
    width,height = dimensions
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    center = .5 * width
    dieLeft = int( center - .5 * width)
    dieRight  = int (center + .5 * width)-1
    dieTop = 1
    dieBottom = height-1
    dieRect = [dieLeft,dieTop,dieRight,dieBottom]
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.rectangle(dieRect,outline=255,fill=0)
    for point in dice[number-1]:
        dotX, dotY = point
        ra = 4
        t = int(height * dotY -ra) + dieTop
        b =  int(height * dotY +ra) + dieTop
        l =  int(width * dotX -ra) + dieLeft
        r =  int(width * dotX +ra) +dieLeft
        draw.ellipse((l, t, r, b), fill=255)
    return image

def newDieRoll():
    number1 = random.randint(1, 6)
    number2 = random.randint(1, 6)
    lastRolls.append(str(number1) + "," + str(number2))
    rollsText= '-'.join(str(x) for x in lastRolls)
    if len(lastRolls) >= 5:
        lastRolls.pop(0)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,128,64), outline=0, fill=0)
    image.paste(renderDie(number1 , (48,48)),(5,16))
    image.paste(renderDie(number2 , (48,48)),(79,16))
    draw.rectangle((0,0,128,16), outline=0, fill=255)
    draw.text((3,0),rollsText,font=font1,fill=0)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def showRollingAnimation():
    draw = ImageDraw.Draw(image)
    for x in range(0,len(diceImages)):
        draw.rectangle((0,0,128,64), outline=0, fill=0)
        image.paste(diceImages[x],(39,16))
        disp.image(image)
        disp.display()
    return

def callback_function_print(input_pint): 
  if GPIO.input(input_pint):
    print "pin " + str(input_pint) + "up"
  else: 
    showRollingAnimation()
    newDieRoll()

GPIO.setmode(GPIO.BCM)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

dir_path = os.path.dirname(os.path.realpath(__file__))
dice =[[(.5,.5)],[(.25,.25),(.75,.75)],[(.25,.25),(.5,.5),(.75,.75)],[(.25,.25),(.75,.25),(.25,.75),(.75,.75)],[(.25,.25),(.75,.25),(.25,.75),(.75,.75),(.5,.5)],[(.33,.25),(.33,.50),(.33,.75),(.66,.25),(.66,.50),(.66,.75)]]
font1 = ImageFont.truetype(dir_path+'/Minecraftia.ttf', 10)

RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
lastRolls = []
diceImages = []

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

for x in range(0,11):
    diceImages.append(Image.open(dir_path+'/dice/'+str(x+1)+'.bmp'))
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_function_print,bouncetime=500)
atexit.register(exit_handler)

while True:
    time.sleep(1);


