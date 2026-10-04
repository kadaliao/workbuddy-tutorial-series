import sys; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep02"
def A4(h):
    h.pause(1.0)
    h.move_to(760,190,dur=0.9,target=[380,175,720,46],label="移进了废纸篓，可以还原"); h.pause(4.0)
    h.move_to(700,330,dur=0.9); h.pause(2.0)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
h=Human(); h.move_to(118,545); h.click(); time.sleep(1.8)
subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/a4_pre.png"])
scene("A4-单删回复",A4,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
