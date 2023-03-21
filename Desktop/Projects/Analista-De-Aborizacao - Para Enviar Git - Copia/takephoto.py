import pyautogui as autogui
from time import sleep

initial_year= 1984
last_year = 2020

autogui.FAILSAFE = False

sleep(10)
for i in range(last_year - initial_year + 1):
    autogui.screenshot(f"desmatamento_{initial_year+i}.png")
    autogui.press('right')