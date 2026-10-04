import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep08"
def D8(h):
    h.pause(0.8)
    h.move_to(560,520,dur=0.8,target=[304,486,508,92],label="成品默认就在工作空间"); h.pause(2.2)
    h.move_to(1303,79,dur=0.8,target=[1289,65,28,28],label="保存"); h.pause(1.4)
    h.move_to(1339,79,dur=0.5,target=[1325,65,28,28],label="上传到云端"); h.pause(1.0)
    h.move_to(1375,79,dur=0.5,target=[1361,65,28,28],label="分享（先别点）"); h.pause(1.6)
    h.move_to(1406,79,dur=0.5,target=[1392,65,28,28],label="更多"); h.pause(1.0)
    h.click(); h.pause(1.2)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/more8.png"]); h.log("mark",text="more"); h.pause(2.4)
    h.esc(); h.pause(0.8)
    h.move_to(1339,79,dur=0.6); h.pause(0.3); h.click(); h.pause(1.2)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/up8.png"]); h.log("mark",text="upload"); h.pause(2.6)
    h.esc(); h.pause(0.8)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
scene("D-成品在哪",D8,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
