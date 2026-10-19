debug = False

from time import sleep
import pynput
import threading
import random as rng
import os

max_x, max_y = 16, 16

locations = []
cur_location = [round(max_x / 2)-1, round(max_y / 2)]
apple = [[rng.randint(1, max_x-2), rng.randint(1, max_y-2)]]
direction = "r"

lenght = 1
max_lenght = (max_x - 2) * (max_y - 2)
state = "alive"

def on_press(key):
    global direction, lenght

    if hasattr(key, "char") and key.char is not None:
        pressed = key.char.lower()
        if pressed == "w" and direction != "d":
            direction = "u"
        elif pressed == "a" and direction != "r":
            direction = "l"
        elif pressed == "s" and direction != "u":
            direction = "d"
        elif pressed == "d" and direction != "l":
            direction = "r"
        elif pressed == "q" and debug:
            lenght += 1
        else:
            pass
    elif key == pynput.keyboard.Key.up and direction != "d":
        direction = "u"
    elif key == pynput.keyboard.Key.left and direction != "r":
        direction = "l"
    elif key == pynput.keyboard.Key.down and direction != "u":
        direction = "d"
    elif key == pynput.keyboard.Key.right and direction != "l":
        direction = "r"
    elif key == pynput.keyboard.Key.esc:
        exit()
    else:
        pass

def printGame():
    global state
    text = f"-- SNAKE --\nScore: {lenght-1}\n\n"
    
    if cur_location[0] == 0 or cur_location[0] == max_x-1 or cur_location[1] == 0 or cur_location[1] == max_y-1:
        state = "Out of bounds!"
    else: 
        for prvek in locations: 
            if locations.count(prvek) >= 2:
                state = "Snake crashed into himself!"

    for y in range(max_y):
        for x in range(max_x):
            #snake head
            if [x, y] == cur_location:
                text += "@ "

            #snake
            elif [x, y] in locations:
                text += "# "

            #apple
            elif [x, y] in apple:
                text += "O "

            #border
            elif x == 0 or y == 0 or x == max_x - 1 or y == max_y - 1:
                text += "+ "

            #nic
            else:
                text += "  "
        text += "\n"

    if debug: text += f"\nMap = {max_x}x{max_y}\nLenght = {lenght}/{max_lenght}\nLocations = C{cur_location} | L{locations} | A{apple}\nCrashed: {state is not "alive"} - {state}"
    print("\033c", end="")
    print(text)

def main():
    global lenght

    if direction == "r":
        cur_location[0] += 1
    elif direction == "l":
        cur_location[0] -= 1
    elif direction == "d":
        cur_location[1] += 1
    elif direction == "u":
        cur_location[1] -= 1
    locations.append(cur_location.copy())

    if cur_location in apple:
        lenght += 1
        apple[0] = [rng.randint(1, max_x - 2), rng.randint(1, max_y - 2)]
    
    if len(locations) > lenght:
        locations.pop(0)

    printGame()
    sleep(0.75)

    if state == "alive":
        if max_lenght == lenght:
            os.system("color A")
            print(f"Game won!\nScore: {lenght-1} (max!)")
            input("Press enter to exit..")
            listener.stop()
            exit()
        main()
    else:
        os.system("color 4")
        print(f"\nGame over!\nScore: {lenght-1}\nDeath cause: {state}")
        input("Press enter to exit..")
        listener.stop()
        exit()

thread = threading.Thread(target=main, daemon=True)
thread.start()

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()