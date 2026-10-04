import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep06"
def C6(h):
    h.pause(0.8)
    h.move_to(100,224,dur=0.8,target=[12,208,245,32],label="专家·技能·连接器"); h.pause(0.4); h.click(); h.pause(1.0)
    b=ocr.find("技能",exact=True,region=[200,150,300,200]); h.move_to(*C(b),dur=0.6,target=[b[0]-20,b[1]-8,120,b[3]+16],label="技能"); h.pause(0.5); h.click(); h.pause(1.8)
    b=ocr.find("我安装的"); h.move_to(*C(b),dur=0.8,target=[b[0]-8,b[1]-8,b[2]+16,b[3]+16],label="我安装的"); h.pause(0.5); h.click(); h.pause(1.8)
    b=ocr.find("周报四段式"); h.move_to(b[0]+60,b[1]+30,dur=0.8,target=[298,110,350,100],label="刚存的技能"); h.pause(3.0); h.log("mark",text="card")
    b=ocr.find("添加技能"); h.move_to(*C(b),dur=0.8,target=[b[0]-10,b[1]-8,b[2]+20,b[3]+16],label="添加技能"); h.pause(0.5); h.click(); h.pause(1.6)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/add.png"]); h.log("mark",text="addmenu"); h.pause(2.6)
    h.esc(); h.pause(0.8)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
h=Human(); new_task(h)
scene("C-看技能",C6,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34],"t":[[0,3]]}]})
