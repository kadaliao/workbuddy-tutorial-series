import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep05"
def F(h):
    h.pause(0.8)
    h.move_to(560,100,dur=0.8,target=[300,52,516,208],label="点名的几处，都改了"); h.pause(3.0); h.log("mark",text="changes")
    h.move_to(560,490,dur=0.8,target=[300,428,516,130],label="没点名的，它照留"); h.pause(3.2); h.log("mark",text="kept")
    h.move_to(980,548,dur=0.8,target=[944,536,60,26],label="还留了个空行"); h.pause(2.6); h.log("mark",text="empty")
    h.pause(0.6)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("F-再看一遍",F,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
