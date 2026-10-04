import sys; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep03"
def C2(h):
    h.pause(0.8)
    h.move_to(480,472,dur=0.8,target=[466,458,28,28],label="点「+」"); h.pause(0.4); h.click(None,[466,458,28,28]); h.pause(1.0)
    h.move_to(540,274,dur=0.8,target=[470,260,196,30],label="添加文件"); h.pause(1.4)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/sub.png"])
    h.pause(3.0)
    h.esc(); h.pause(0.3); h.esc(); h.pause(0.8)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("C2-添加文件",C2,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
