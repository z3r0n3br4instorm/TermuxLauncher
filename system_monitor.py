import curses
import psutil
import subprocess
import time
import json
import threading

battery_percentage = 0  # Global variable to store battery percentage


def get_gpu_usage():
    try:
        return 3
    except:
        return 0


def get_cell_signal():
    try:
        command = ["python", "signalStrength.py"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return int(float(result.stdout))
        except:
            return 0
        return 0
    except:
        pass
    return 0


def get_battery_percentage():
    global battery_percentage
    while True:
        try:
            result = subprocess.run(["python", "battery.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            battery_percentage = int(result.stdout)  # Update global variable
        except:
            battery_percentage = 0  # Set to 0 in case of error
        time.sleep(1)  # Update every second


def draw_bar(percentage, bar_length=30):
    filled_length = int(bar_length * percentage / 100)
    bar = "[" + "\\" * filled_length + " " * (bar_length - filled_length) + "]"
    return bar


def center_text(stdscr, text, row):
    max_y, max_x = stdscr.getmaxyx()
    col = (max_x // 2) - (len(text) // 2)
    stdscr.addstr(row, col, text)


def main(stdscr):
    global battery_percentage
    curses.curs_set(0)
    stdscr.clear()

    # Start the battery percentage in a separate thread
    battery_thread = threading.Thread(target=get_battery_percentage)
    battery_thread.daemon = True  # Ensure the thread exits when the main program exits
    battery_thread.start()

    while True:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        gpu_percent = get_gpu_usage()
        ram_percent = psutil.virtual_memory().percent
        wifi_percent = get_cell_signal()

        center_text(stdscr, "HUD_SYSMON", 0)

        # Display the bars and center each line
        center_text(stdscr, f"CPU          : {draw_bar(cpu_percent)} ", 1)
        center_text(stdscr, f"GPU          : {draw_bar(gpu_percent)} ", 2)
        center_text(stdscr, f"RAM          : {draw_bar(ram_percent)} ", 3)
        center_text(stdscr, f"BATT         : {draw_bar(battery_percentage)} ", 4)
        center_text(stdscr, f"CELL    : {draw_bar(wifi_percent)} ", 5)

        stdscr.refresh()

        time.sleep(1)


if __name__ == "__main__":
    curses.wrapper(main)
