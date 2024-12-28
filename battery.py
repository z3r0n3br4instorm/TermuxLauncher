import subprocess
import json
try:
    result = subprocess.run(["termux-battery-status"], capture_output=True, text=True, check=True)
    battery_data = json.loads(result.stdout)
    return battery_data.get("percentage", 0)
except:
    return 0
