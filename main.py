import os
import subprocess

class Launcher:
    def __init__(self):
        self.tmux_session = "ztOS_HUD_TUI"

    def start_tmux(self):
        subprocess.run("stty cols 64 rows 37", shell=True)
        subprocess.run(f"tmux new-session -d -s {self.tmux_session}", shell=True)

    def split_panes(self):
        subprocess.run(f"tmux split-window -v -t {self.tmux_session}", shell=True)
        subprocess.run(f"tmux split-window -v -t {self.tmux_session}:0.0", shell=True)

    def resize_panes(self):
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.0 -y 10", shell=True)  # Resize pane 0
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.1 -y 20", shell=True)  # Resize pane 1
        subprocess.run(f"tmux resize-pane -t {self.tmux_session}:0.2 -y 15", shell=True)  # Resize pane 2

    def send_commands(self):
        # Send commands to each pane

        # Pane 0: Clock (using tclock)
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.0 'tclock' C-m", shell=True)

        # Pane 1: System Monitor
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.1 'sudo python system_monitor.py' C-m", shell=True)

        # Pane 2: App Launcher
        subprocess.run(f"tmux send-keys -t {self.tmux_session}:0.2 'bash' C-m", shell=True)

    def attach_tmux(self):
        # Attach to the tmux session
        subprocess.run(f"tmux attach -t {self.tmux_session}", shell=True)

    def launch(self):
        self.start_tmux()
        self.split_panes()
        self.resize_panes()
        self.send_commands()
        self.attach_tmux()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.launch()
