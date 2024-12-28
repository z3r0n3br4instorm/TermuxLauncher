import curses
import psutil
import subprocess
import time

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

def get_battery_temperature():
    try:
        data = subprocess.run("sudo", "cat", "/sys/class/power_supply/battery/temp", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return int(data.stdout)
    except:
        return 0

def get_battery_percentage():
    if True:
        try:
            data = open("battery.txt", "r")
            return int(data.read())
        except:
            return 10

def draw_bar(percentage, bar_length=30, color_pair=1):
    filled_length = int(bar_length * percentage / 100)
    bar = "[" + "/" * filled_length + "-" * (bar_length - filled_length) + "]"
    return bar, filled_length

def center_text(stdscr, text, row, color_pair=1):
    max_y, max_x = stdscr.getmaxyx()
    col = (max_x // 2) - (len(text) // 2)
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(row, col, text)
    stdscr.attroff(curses.color_pair(color_pair))

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()

    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Labels
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Bars
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)   # Warning Bars
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Alerts

    stdscr.clear()

    while True:
        stdscr.clear()

        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        gpu_percent = get_gpu_usage()
        ram_percent = psutil.virtual_memory().percent
        wifi_percent = get_cell_signal()
        battery_percent = get_battery_percentage()

        # Center header text
        center_text(stdscr, "-= HUD_SYSMON v1.0 =-", 0, 1)
        cpu_bar, cpu_filled = draw_bar(cpu_percent)
        color = 3 if cpu_percent > 80 else 2
        center_text(stdscr, f"CPU   : {cpu_bar} {cpu_percent:06.2f}%", 2, color)

        gpu_bar, gpu_filled = draw_bar(gpu_percent)
        color = 3 if gpu_percent > 80 else 2
        center_text(stdscr, f"GPU   : {gpu_bar} {gpu_percent:06.2f}%", 3, color)

        ram_bar, ram_filled = draw_bar(ram_percent)
        color = 3 if ram_percent > 80 else 2
        center_text(stdscr, f"RAM   : {ram_bar} {ram_percent:06.2f}%", 4, color)

        battery_bar, battery_filled = draw_bar(battery_percent)
        color = 3 if battery_percent < 20 else 2
        center_text(stdscr, f"BATT  : {battery_bar} {battery_percent:06.2f}%", 5, color)

        wifi_bar, wifi_filled = draw_bar(wifi_percent)
        color = 2 if wifi_percent > 50 else 3
        center_text(stdscr, f"CELL  : {wifi_bar} {wifi_percent:06.2f}%", 6, color)
        center_text(stdscr, " ztOS HUD ", 8, 4)

        stdscr.refresh()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
