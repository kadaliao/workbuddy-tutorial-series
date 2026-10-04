import sys; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep02"
USER=[8,795,180,55]
def F(h):
    h.pause(0.8)
    h.move_to(1335,28,target=[1288,12,132,32],label="添加定时任务"); h.pause(0.4); h.click(None,[1288,12,132,32]); h.pause(1.6)
    h.move_to(558,485,dur=0.9,target=[500,472,120,28],label="权限默认是红色的「允许完全访问」",); h.pause(2.6)
    h.click(None,[500,472,120,28]); h.pause(1.4)
    h.move_to(600,372,dur=0.7,target=[496,334,196,76],label="提醒：注意数据安全"); h.pause(2.4)
    h.move_to(664,441,dur=0.7,target=[640,428,48,26],label="把它关掉"); h.pause(0.5); h.click(None,[640,428,48,26]); h.pause(1.4)
    h.move_to(800,200,dur=0.6); h.click(); h.pause(1.0)
    h.move_to(540,485,dur=0.7,target=[500,472,120,28],label="改回默认权限"); h.pause(2.4)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/f_after.png"])
    h.move_to(981,657,dur=0.8,target=[948,641,68,32],label="演示用，取消"); h.pause(0.4); h.click(None,[948,641,68,32]); h.pause(1.4)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("F-定时任务权限",F,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER}]})
