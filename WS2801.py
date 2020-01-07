# Source: https://forum.micropython.org/viewtopic.php?t=1351&p=40880&hilit=spi#p40879
# Works with MicroPython esp8266-20191220-v1.12
# Wiring: 
# CK -> D5
# SI -> D7
# 5V -> UV
# GND -> G

from machine import Pin, SPI
import time

N_LED = const(160)
DEFAULT_COLOR = {'r': 0xff, 'g': 0xA0, 'b': 0xA0}

class WS2801:

  def __init__(self, num_led, spi):
    self.NUM_LED = num_led
    self._databuffer = bytearray(3*num_led)
    self._spi = spi
    # Check if baud frequency adequate.

  def set_led(self, num, r=0x00, g=0x00, b=0x00):
    if num < self.NUM_LED:
      self._databuffer[num*3] = r
      self._databuffer[num*3+1] = b
      self._databuffer[num*3+2] = g
    else:
      print("Command ignored. LED out of index!")

  def write(self, clear=False):
    self._spi.write(self._databuffer)
    if clear:
      self.clear()

  def clear(self, default=0x00):
    for i in range(len(self._databuffer)):
      self._databuffer[i] = default
  def set_all(self, r=0xff, g=0xff, b=0xff):
    for i in range(self.NUM_LED):
      self.set_led(num=i, r=r, g=g, b=b)

hspi = SPI(1, baudrate=int(250e3))
print("Initialize WS2801 handler")
ws_handler = WS2801(spi=hspi, num_led=N_LED)

print("Test LEDs")
ws_handler.clear()
ws_handler.write()
while True:
    for i in range(N_LED):
      ws_handler.clear()
      ws_handler.set_led(num=i, **DEFAULT_COLOR)
      ws_handler.write()
      time.sleep_ms(1)
ws_handler.clear()
ws_handler.write()
