import sys, time, os, json; sys.path.insert(0,'.')
from human import Recorder
out="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep10/M-电脑端.mov"
r=Recorder(out); t0=time.time(); r.start()
json.dump({"wall_start": t0}, open(out[:-4]+".wall.json","w"))
import subprocess
while not os.path.exists("/private/tmp/claude-501/stop_rec") and time.time()-t0 < 1800:
    fr=subprocess.run(["osascript","-e",'tell application "System Events" to get name of first process whose frontmost is true'],capture_output=True,text=True).stdout.strip()
    if fr!="WorkBuddy": subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate'])
    time.sleep(1.5)
r.stop(); print("stopped", round(time.time()-t0,1))
