import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
import time
import math
import tkinter as tk
import asyncio
from bleak import BleakScanner, BleakClient
import sys

MAC_ADDR = "BE:58:45:00:53:FA"
MODEL_NBR_UUID = "00002a00-0000-1000-8000-00805f9b34fb"
CHAR_UUID = "0000FFF3-0000-1000-8000-00805f9b34fb"
# from PIL import ImageGrab

def unique_count_app():
  img = pyautogui.screenshot()
  a = np.array(img)
  colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
  return colors[count.argmax()]


def bincount_app():
    img = pyautogui.screenshot()
    a = np.array(img) 
    a2D = a.reshape(-1,a.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)


def take_screenshot():
  img = pyautogui.screenshot()
  open_cv_image = np.array(img) 
  im = open_cv_image# cv.cvtColor(open_cv_image, cv.COLOR_BGR2RGB)
  # r = np.average(im[:, : ,0])
  # g = np.average(im[:, : ,1])
  # b = np.average(im[:, : ,2])
  avg = np.mean(im, axis = (0,1))

  # print(avg)
  # print(flor)
  # floored = np.floor([r,g,b])
  floored = np.floor(avg)
  return floored

async def color_loop(): 
  async with BleakClient(MAC_ADDR) as client:
    await client.get_services()
    while(1):
        time.sleep(0.1)
        rgb = bincount_app()
        R=int(rgb[0])
        G=int(rgb[1])
        B=int(rgb[2])
        data = bytes.fromhex('7e070503'+f'{R:02x}{G:02x}{B:02x}'+'10ef')
        await client.write_gatt_char(CHAR_UUID, data, response=False)

def change_color():
    rgb = bincount_app()
    print(rgb)
    color_code = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    window['bg'] = color_code
    window.after(1000, change_color)
 
 

window = tk.Tk()
# window.geometry("200x200")
# change_color()
# window.mainloop()

async def main():
  if len(sys.argv) == 2 and sys.argv[1] == 'w': 
    window.geometry("200x200")
    change_color()
    window.mainloop()
  else: 
    await color_loop()

asyncio.run(main()) 
