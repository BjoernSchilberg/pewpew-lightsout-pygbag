import asyncio
import src.pew as pew
import random  # Import the random library for generating random numbers

pew.init()  # Initialize the pew library

# Create an 8x8 matrix array with all values set to 0
# This represents the LED display, with each cell in the array corresponding to
# a pixel on the display
screen = pew.Pix()

# Decide how many lights you want to randomly turn on
# Generate a random integer between 0 and 63 (inclusive)
num_lights = random.randint(0, 63)

# Turn on random lights
# For each light to be turned on, generate random x and y coordinates (0-7
# inclusive), and set the pixel at those coordinates to 2 (on)
for i in range(num_lights):
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    screen.pixel(x, y, 2)

# Set initial coordinates for a moving light
x = random.randint(0,7)
y = random.randint(0,7)

# Variable to control the blinking of the moving light
blink = True

async def main():

    global x,y, blink

    # Game loop
    while True:
        # Set the current pixel to 0 (off) if its current brightness is less than 4, or to 2 (on) otherwise
        screen.pixel(x, y, 0 if screen.pixel(x, y) < 4 else 2)

        # Read the current state of the keys
        keys = pew.keys()

        # Update dx and dy based on the keys pressed
        dx = (keys & pew.K_RIGHT > 0) - (keys & pew.K_LEFT > 0)
        dy = (keys & pew.K_DOWN > 0) - (keys & pew.K_UP > 0)

        # Make sure that the new x and y are within the game field (0-7 inclusive)
        x = max(0, min(x + dx, 7))
        y = max(0, min(y + dy, 7))

        # Get the brightness of the target pixel (the pixel the moving light will
        # move to in the next frame)
        target = screen.pixel(x,y)

        # If the X key is pressed and the target pixel is off or on (but not
        # blinking or bright), turn off or on the pixels in the cross pattern
        # centered at the current pixel
        if target in {0, 2} and (keys & pew.K_X):
            screen.pixel(x, y, 0 if screen.pixel(x, y) in {2} else 2)
            screen.pixel(x + 1, y, 0 if screen.pixel(x + 1, y) in {2} else 2)
            screen.pixel(x - 1, y, 0 if screen.pixel(x - 1, y) in {2} else 2)
            screen.pixel(x, y + 1, 0 if screen.pixel(x, y + 1) in {2} else 2)
            screen.pixel(x, y - 1, 0 if screen.pixel(x, y - 1) in {2} else 2)

        # Count the number of pixels currently on (not blinking or bright)
        count = 0
        for b in range(8):
            for a in range(8):
                if screen.pixel(a, b) == 2:
                    count += 1
        # If there are no pixels on, exit the game loop
        if count == 0:
            # Create a Pix object from the text "Game over!"
            # The Pew library provides the from_text function to convert text into a Pix
            # object that can be displayed on the LED matrix
            text = pew.Pix.from_text("Game over!")

            # Loop over the range from -8 to the width of the text
            # This will scroll the text from the right side of the screen to the left
            for dx in range(-8, text.width):
                # Blit (copy) the text Pix object onto the screen Pix object at the current
                # x coordinate (dx) and y coordinate 1
                # The negative sign before dx causes the text to move from right to left
                screen.blit(text, -dx, 1)

                # Update the display to show the current state of the screen Pix object
                pew.show(screen)

                # Wait for 1/12 of a second before the next frame
                # This creates a frame rate of 12 frames per second, causing the text to
                # scroll smoothly across the screen
                pew.tick(1/12)
                await asyncio.sleep(0)  # Very important, and keep it 0

            break

        # Set the current pixel to blink (if the blink variable is True) or to be on
        # (if the blink variable is False), and to be bright (4) if it is currently
        # on or blinking
        screen.pixel(x, y, (3 if blink else 2) + (4 if screen.pixel(x, y) in {2, 7} else 0))

        # Toggle the blink variable
        blink = not blink

        # Update the display
        pew.show(screen)

        # Wait for 1/6 of a second before the next frame
        pew.tick(1 / 6)
        await asyncio.sleep(0)  # Very important, and keep it 0

# This is the program entry point:
if __name__ == '__main__':
    asyncio.run(main())

# Do not add anything from here
# asyncio.run is non-blocking on pygame-wasm
