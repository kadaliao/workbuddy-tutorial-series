import sys; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep03"
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]
def D2(h):
    h.pause(0.8)
    h.move_to(800,392,dur=0.8,target=[452,362,790,52],label="改写成结构清楚的版本"); h.pause(3.2)
    h.move_to(1064,472,dur=0.8,target=[1050,458,28,28],label="不满意：恢复原文"); h.pause(1.2); h.click(None,[1050,458,28,28]); h.pause(1.4)
    h.move_to(700,392,dur=0.8,target=[452,362,300,30],label="回到原话"); h.pause(2.4)
def CE(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX,label="点输入框"); h.pause(0.3); h.click(None,BOX); h.pause(0.5)
    h.type_text("整理本周周报，",label="做什么",target=[452,362,300,30]); h.pause(0.8)
    h.move_to(480,472,dur=0.8,target=[466,458,28,28],label="点「+」"); h.pause(0.4); h.click(None,[466,458,28,28]); h.pause(1.2)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/plus.png"])
    h.log("mark",text="plus_open"); h.pause(2.5)
    h.esc(); h.pause(0.8)
    h.move_to(640,395,dur=0.6); h.click(); h.key(124, Quartz.kCGEventFlagMaskCommand); h.pause(0.4)
    h.type_text("材料是这个文件夹里的三份日报和数据表，",label="有什么材料",target=[452,362,790,30]); h.pause(0.6)
    h.type_text("分四段，输出 Word。",label="要什么结果",target=[452,362,790,52]); h.pause(1.0)
    h.type_text("只用材料里的内容，不要编；查不到的写待确认。",label="两个限制",target=[452,362,790,80]); h.pause(2.5)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("D2-恢复原文",D2,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
h=Human(); h.move_to(640,395); h.click(); time.sleep(0.3); h.key(0, Quartz.kCGEventFlagMaskCommand); time.sleep(0.2); h.key(51); time.sleep(0.6)
scene("CE-写需求",CE,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
h=Human(); h.move_to(640,395); h.click(); time.sleep(0.3); h.key(0, Quartz.kCGEventFlagMaskCommand); time.sleep(0.2); h.key(51)
