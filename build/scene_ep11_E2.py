import sys, hashlib; sys.path.insert(0,'.')
from wslib import *
from scene_ep11_E import wait
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep11"
def E2(h):
    h.pause(0.8)
    h.move_to(800,718,dur=0.7,target=[462,692,766,60]); h.pause(0.3); h.click(); h.pause(0.4)
    h.type_text("确认，创建吧。",label="看过草稿，再确认",target=[462,692,766,60]); h.pause(0.8)
    h.key(36); h.log("mark",text="send")
    print("E2 waited", wait(h, 300, 20)); h.log("mark",text="created")
    subprocess.run(["cp","/private/tmp/claude-501/poll.png","/private/tmp/claude-501/created.png"])
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
scene("E2-确认创建",E2,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
