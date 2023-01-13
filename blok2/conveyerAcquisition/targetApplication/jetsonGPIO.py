import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

def setup(pin, direction):
  if direction == 'out':
    direction = GPIO.OUT
  else:
    direction = GPIO.IN
    

  # if pin array
  if isinstance(pin, list):
    for p in pin:
      GPIO.setup(p, direction)
  else:
    GPIO.setup(pin, direction)

def output(pin, value):
  if value == True:
    value = GPIO.HIGH
  else:
    value = GPIO.LOW

  # if pin array
  if isinstance(pin, list):
    for p in pin:
      GPIO.output(p, value)
  else:
    GPIO.output(pin, value)

def input(pin):
  return GPIO.input(pin)

def cleanup():
  GPIO.cleanup()