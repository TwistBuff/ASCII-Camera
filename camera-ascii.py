import cv2 as cv
import numpy as np
import curses


#! CONSTANT
DENSITY = ' _.,-=+:;cba!?0123456789$W#@Ñ'
SCALE = 0.3
CAM_PORT = 0
INTERVALL = 1 

frame_counter = 0

cam = cv.VideoCapture(CAM_PORT, cv.CAP_DSHOW)

screen = curses.initscr()
screen.clear()


if not cam.isOpened():
    raise IOError("Cannot open camera")

while True:
    result, image = cam.read()
    
    image = cv.resize(image, None, fx=SCALE, fy=SCALE, interpolation=cv.INTER_AREA)

    screen.clear()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            #* Get the RGB values of the pixels 
            #* of each frame in a numpy array
            rgb = image[y, x]

            #* Get the gray value
            gray = (np.sum(rgb)/3)

            #* use scaling to get the right ascii character 
            charIndex = gray // len(DENSITY)
            ascii_image = DENSITY[int(charIndex)]

            #* Print the character into the terminal screen    
            try:
                screen.addch(y, x, ascii_image)
            except curses.error:
                pass
    
    frame_counter += 1
    if frame_counter % INTERVALL == 0:
        screen.refresh()

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

curses.endwin()
cam.release()
cv.destroyAllWindows()