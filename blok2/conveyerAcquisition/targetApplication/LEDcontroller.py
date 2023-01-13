from jetsonGPIO import setup as setupGPIO, output as outputGPIO

leds = [7, 11, 13, 15, 19, 21 , 23]
items = ['ignore','Bag', 'Bottle', 'Bottlecap', 'Fork', 'Knife', 'Pen', 'Spoon', 'Styrofoam']
ledOfItems = [6, 1, 2, 0, 3, 3, 4, 3, 5]

# set all leds as output
setupGPIO(leds, 'out')
# set all leds on and then off
outputGPIO(leds, True)
outputGPIO(leds, False)

def turnLedOnBasedOnItem(item):
  # turn all leds off
  outputGPIO(leds, False)
  # turn on led of item
  outputGPIO(leds[ledOfItems[items.index(item)]], True)