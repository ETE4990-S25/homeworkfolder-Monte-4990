import os
import sys
import time
import threading
import multiprocessing
import msvcrt  # Windows-only module for keyboard input
from ball import move_ball
from shared import ball_x, ball_y, paddle1_y, paddle2_y, PADDLE_SIZE

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_keypress():
    """Windows-compatible keypress detection."""
    return msvcrt.getch().decode('utf-8').lower()

def handle_input():
    """Handles player input for moving paddles."""
    while True:
        if msvcrt.kbhit():  # Check if a key is pressed
            key = get_keypress()
            if key == 'w' and paddle1_y.value > 1:
                paddle1_y.value -= 1
            elif key == 's' and paddle1_y.value < 16:
                paddle1_y.value += 1
            elif key == 'o' and paddle2_y.value > 1:
                paddle2_y.value -= 1
            elif key == 'l' and paddle2_y.value < 16:
                paddle2_y.value += 1
            elif key == 'q':  # Quit the game
                os._exit(0)

def draw_screen(width, height):
    """Redraws the game screen at intervals."""
    while True:
        clear_screen()
        screen = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Draw borders
        for i in range(width):
            screen[0][i] = screen[-1][i] = '-'
        for i in range(height):
            screen[i][0] = screen[i][-1] = '|'
        
        # Draw paddles
        for i in range(PADDLE_SIZE):
            screen[paddle1_y.value + i][2] = '|'
            screen[paddle2_y.value + i][width - 3] = '|'
        
        # Draw ball
        screen[ball_y.value][ball_x.value] = 'O'
        
        # Print screen efficiently
        sys.stdout.write('\n'.join(''.join(row) for row in screen) + '\n')
        sys.stdout.flush()
        time.sleep(0.05)

def main():
    height, width = 20, 50
    
    # Create and start the ball movement process
    ball_process = multiprocessing.Process(target=move_ball, args=(height, width))
    ball_process.start()

    # Create and start the input handling thread
    input_thread = threading.Thread(target=handle_input, daemon=True)
    input_thread.start()
    
    try:
        draw_screen(width, height)
    except KeyboardInterrupt:
        pass
    finally:
        ball_process.terminate()
        ball_process.join()

if __name__ == "__main__":
    main()
