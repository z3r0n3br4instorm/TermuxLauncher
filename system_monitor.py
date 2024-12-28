import curses
import psutil
import subprocess
import time
import asyncio


async def get_gpu_usage():
    try:
        return 3
    except:
        return 0


async def get_cell_signal():
    try:
        command = ["python", "signalStrength.py"]
        try:
            result = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = await result.communicate()
            if result.returncode == 0:
                return int(float(stdout))
            else:
                print(f"Error in signalStrength.py: {stderr}")
                return 0
        except Exception as e:
            print(f"Error running signalStrength.py: {e}")
            return 0
    except Exception as e:
        print(f"Error in get_cell_signal: {e}")
    return 0


async def get_battery_percentage():
    try:
        command = ["python", "battery.py"]
        result = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = await result.communicate()
        print(f"Battery script output: {stdout}")  # Debug output
        if result.returncode == 0:
            return int(stdout.strip())
        else:
            print(f"Error in battery script: {stderr}")
            return 0
    except Exception as e:
        print(f"Error in get_battery_percentage: {e}")
        return 0


def draw_bar(percentage, bar_length=30):
    filled_length = int(bar_length * percentage / 100)
    bar = "[" + "\\" * filled_length + " " * (bar_length - filled_length) + "]"
    return bar


def center_text(stdscr, text, row):
    max_y, max_x = stdscr.getmaxyx()
    col = (max_x // 2) - (len(text) // 2)
    stdscr.addstr(row, col, text)


async def main_loop(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    while True:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        gpu_percent = await get_gpu_usage()
        ram_percent = psutil.virtual_memory().percent
        battery_percent = await get_battery_percentage()
        wifi_percent = await get_cell_signal()

        center_text(stdscr, "HUD_SYSMON", 0)

        # Display the bars and center each line
        center_text(stdscr, f"CPU          : {draw_bar(cpu_percent)} ", 1)
        center_text(stdscr, f"GPU          : {draw_bar(gpu_percent)} ", 2)
        center_text(stdscr, f"RAM          : {draw_bar(ram_percent)} ", 3)
        center_text(stdscr, f"BATT         : {draw_bar(battery_percent)} ", 4)
        center_text(stdscr, f"CELL    : {draw_bar(wifi_percent)} ", 5)

        stdscr.refresh()

        await asyncio.sleep(1)


def run_curses():
    asyncio.run(curses.wrapper(main_loop))


if __name__ == "__main__":
    run_curses()
