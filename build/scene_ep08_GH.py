import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep08"
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def G8(h):
    h.pause(0.8)
    h.move_to(69,290,dur=0.8,target=[12,274,245,32],label="资料库"); h.pause(0.4); h.click(); h.pause(2.0)
    h.move_to(380,190,dur=0.8,target=[280,160,260,90],label="我的资料"); h.pause(2.2)
    h.move_to(380,290,dur=0.6,target=[280,262,260,58],label="团队空间"); h.pause(2.0)
    b=ocr.find("我分享的"); 
    if b: h.move_to(b[0]+28,b[1]+8,dur=0.7,target=[b[0]-8,b[1]-8,72,b[3]+16],label="我分享的"); h.pause(0.5); h.click(); h.pause(1.8); h.log("mark",text="shared")
    h.move_to(800,215,dur=0.7); h.pause(2.4)
    b=ocr.find("已使用"); 
    if b: h.move_to(b[0]+60,b[1]+6,dur=0.7,target=tgt(b),label="容量"); h.pause(2.0)
def H8(h):
    h.pause(0.6)
    h.key(43, Quartz.kCGEventFlagMaskCommand); h.pause(2.0)
    b=ocr.find("数据管理"); h.move_to(*C(b),dur=0.8,target=tgt(b),label="设置 › 数据管理"); h.pause(0.4); h.click(); h.pause(1.8)
    b=ocr.find("分享的文件"); h.move_to(*C(b),dur=0.6,target=tgt(b),label="分享的文件"); h.pause(1.6)
    b=ocr.find("本周周报"); h.move_to(b[0]+200,b[1]+12,dur=0.7,target=[b[0]-10,b[1]-10,640,48],label="在这里管理或取消分享"); h.pause(1.6)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/dm8.png"]); h.log("mark",text="row"); h.pause(1.8)
    h.move_to(450,76,dur=0.8); h.click(); h.pause(1.0)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
M={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"所有者列","rect":[900,195,110,240],"style":"fillmed"}]}
scene("G-资料库",G8,outdir=O,extra=M)
scene("H-数据管理",H8,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
