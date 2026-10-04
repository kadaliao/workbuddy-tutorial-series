import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep09"
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def F9(h):
    h.pause(0.8)
    b=ocr.find("运行记录"); h.move_to(*C(b),dur=0.7,target=tgt(b),label="运行记录"); h.pause(0.4); h.click(); h.pause(1.6)
    b=ocr.find("素材检查演示"); h.move_to(b[0]+60,b[1]+8,dur=0.7,target=[284,94,1136,32],label="到点自己跑完了：成功"); h.pause(2.6)
    h.click(); h.pause(2.4); h.log("mark",text="opened")
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/f9.png"])
    h.move_to(800,400,dur=0.8); h.pause(4.0)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
h=Human(); b=ocr.find("定时任务",region=[280,0,200,40]); h.move_to(*C(b)); h.click(); time.sleep(1.2)
scene("F-运行记录",F9,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
