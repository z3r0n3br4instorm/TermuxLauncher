import subprocess
import re

def rsrp_to_percentage(rsrp):
    min_rsrp = -120
    max_rsrp = -50
    return max(0, min(100, ((rsrp - min_rsrp) / (max_rsrp - min_rsrp)) * 100))

def get_rsrp_from_adb():
    result = subprocess.run(["sudo", "dumpsys", "telephony.registry"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        # Find the rsrp value using regex
        match = re.search(r"rsrp=(-?\d+)", result.stdout)
        if match:
            return int(match.group(1))
        else:
            print("RSRP value not found.")
            return None
    else:
        print("Error running adb command:", result.stderr)
        return None

rsrp = get_rsrp_from_adb()
if rsrp is not None:
    percentage = rsrp_to_percentage(rsrp)
    print(f"{percentage}")
else:
    print("0")
