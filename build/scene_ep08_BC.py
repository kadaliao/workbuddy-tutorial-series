import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep08"; os.makedirs(O, exist_ok=True)
BOX=[454,358,795,143]
def B8(h):
    h.pause(0.8)
    h.move_to(560,521,dur=0.8,target=[472,508,150,26],label="① 工作空间里的文件"); h.pause(2.2)
    h.move_to(482,473,dur=0.7,target=[466,458,28,28],label="② 点「+」"); h.pause(0.4); h.click(); h.pause(1.0)
    b=ocr.find("添加文件",region=[440,150,300,330]); h.move_to(*C(b),dur=0.6,target=[b[0]-30,b[1]-8,196,b[3]+16],label="添加文件"); h.pause(1.4)
    h.move_to(760,b[1]+9,dur=0.5); h.pause(0.4)
    h.move_to(760,b[1]+60,dur=0.6,target=[662,b[1]-12,200,180],label="本地、资料库、腾讯文档、ima、乐享"); h.pause(3.0); h.log("mark",text="submenu")
    h.esc(); h.pause(0.3); h.esc(); h.pause(0.6)
    h.move_to(640,395,dur=0.6,target=BOX); h.click(); h.pause(0.4)
    h.type_text("@",label="③ 打 @ 引用文件",target=BOX); h.pause(1.6)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/at.png"]); h.log("mark",text="atpanel"); h.pause(2.6)
    h.esc(); h.pause(0.3); h.key(51); h.pause(0.6)
def C8(h):
    h.pause(0.6)
    subprocess.run(["osascript","-e",'tell application "Finder" to activate']); h.pause(1.2)
    h.move_to(1210,615,dur=0.9,target=[1160,575,100,100],label="直接把文件拖进来"); h.pause(0.6); h.mouse_down(); h.pause(0.3)
    h.move_to(1150,560,dur=0.4,drag=True,overshoot=False,log=False); h.move_to(760,410,dur=1.1,drag=True,overshoot=False,log=False); h.pause(0.6); h.mouse_up(); h.log("mark",text="drop"); h.pause(1.4)
    h.move_to(560,395,dur=0.6,target=[452,364,120,28],label="变成了文件胶囊"); h.pause(2.4)
    h.move_to(640,395,dur=0.3); h.click(); h.key(0, Quartz.kCGEventFlagMaskCommand); h.pause(0.2); h.key(51); h.pause(0.2); h.key(51); h.pause(0.6)
h=Human(); new_task(h); pick_folder(h, "/Users/Shared/周报素材")
M={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]}
scene("B-进材料",B8,outdir=O,extra=M)
subprocess.run(["osascript","-e",'tell application "Finder" to set bounds of Finder window 1 to {1000, 580, 1500, 880}'])
scene("C-拖拽",C8,outdir=O,extra=M)
