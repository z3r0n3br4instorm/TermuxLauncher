import curses
import psutil
import subprocess
import time


def get_gpu_usage():
    try:
        # Under Development
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


def draw_bar(percentage, bar_length=30):
    filled_length = int(bar_length * percentage / 100)
    bar = "[" + "\\" * filled_length + " " * (bar_length - filled_length) + "]"
    return bar


def center_text(stdscr, text, row):
    max_y, max_x = stdscr.getmaxyx()
    col = (max_x // 2) - (len(text) // 2)
    stdscr.addstr(row, col, text)


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    while True:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        gpu_percent = get_gpu_usage()
        ram_percent = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else 0
        wifi_percent = get_cell_signal()

        # Center the HUD title
        center_text(stdscr, "HUD_SYSMON", 0)

        # Display the bars and center each line
        center_text(stdscr, f"CPU          : {draw_bar(cpu_percent)} ", 1)
        center_text(stdscr, f"GPU          : {draw_bar(gpu_percent)} ", 2)
        center_text(stdscr, f"RAM          : {draw_bar(ram_percent)} ", 3)
        center_text(stdscr, f"BATT         : {draw_bar(battery_percent)} ", 4)
        center_text(stdscr, f"CELL/WIFI    : {draw_bar(wifi_percent)} ", 5)

        stdscr.refresh()

        time.sleep(1)


if __name__ == "__main__":
    curses.wrapper(main)
