import os
import time
import subprocess
import threading

class Launcher:
    def __init__(self):
        self.tmux_session = "ztOS_HUD_TUI"

    def start_tmux(self):
        subprocess.run(f"tmux new-session -d -s {self.tmux_session}", shell=True)

    def batteryThread(self):
        while True:
            os.system("python battery.py > battery.txt")
            time.sleep(10)

    def split_panes(self):
        # Create vertical splits
        subprocess.run(f"tmux split-window -v -t {self.tmux_session}", shell=True)  # Pane 1
        subprocess.run(f"tmux split-window -v -t {self.tmux_session}:0.0", shell=True)  # Pane 0

        # Create a horizontal split for the app launcher pane
        subprocess.run(f"tmux split-window -h -t {self.tmux_session}:0.2", shell=True)  # Pane 3

    def resize_panes(self):
        # Resize the vertical panes
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.0 -y 10", shell=True)  # Pane 0
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.1 -y 20", shell=True)  # Pane 1
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.2 -y 15", shell=True)  # Pane 2 (app launcher)

        # Resize the horizontal split
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.3 -x 50", shell=True)  # Pane 3 (logcat)

    def send_commands(self):
        # Send commands to each pane

        # Pane 0: Clock (using tclock)
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.0 'tclock' C-m", shell=True)

        # Pane 1: System Monitor
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.1 'sudo python system_monitor.py' C-m", shell=True)

        # Pane 2: App Launcher
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.2 'python launchApp.py' C-m", shell=True)

        # Pane 3: Logcat
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.3 'sudo logcat' C-m", shell=True)

    def attach_tmux(self):
        # Attach to the tmux session
        subprocess.run(f"tmux attach -t {self.tmux_session}", shell=True)

    def launch(self):
        self.start_tmux()
        self.split_panes()
        self.resize_panes()
        self.send_commands()
        self.attach_tmux()
        batterThread = threading.Thread(target=self.batteryThread)
        batterThread.start()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.launch()
