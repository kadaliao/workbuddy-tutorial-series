import sys, hashlib; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep04"; os.makedirs(O, exist_ok=True)
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]; D="/Users/Shared/模式演示"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def BC(h):
    before=sorted(os.listdir(D)); h.pause(0.8)
    h.move_to(480,472,dur=0.8,target=[466,458,28,28],label="点「+」"); h.pause(0.4); h.click(None,[466,458,28,28]); h.pause(1.0)
    h.move_to(540,322,dur=0.7,target=[476,307,182,32],label="模式"); h.pause(1.4)
    h.move_to(760,338,dur=0.7,target=[668,316,186,46],label="不开开关 = 默认模式"); h.pause(2.6)
    h.move_to(831,396,dur=0.6,target=[670,382,184,30],label="计划 Plan"); h.pause(1.6)
    h.move_to(831,430,dur=0.5,target=[670,416,184,30],label="仅问答 Ask"); h.pause(1.4)
    h.click(None,[816,420,30,20]); h.log("mark",text="ask_on"); h.pause(1.4)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/askon.png"])
    h.esc(); h.pause(0.4); h.esc(); h.pause(0.6)
    h.move_to(640,395,dur=0.7,target=BOX,label="问一句"); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text("如果我让你整理这个文件夹，你会怎么做？会删除文件吗？",target=BOX); h.pause(0.8)
    h.move_to(1220,473,target=[1195,448,50,50],label="发送"); h.pause(0.4); h.click(None,[1195,448,50,50])
    t0=mono(); last=None; stable=0
    while mono()-t0 < 180:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=4 and mono()-t0>15: break
    h.log("mark",text="answer_done"); h.pause(1.0)
    print("C waited", round(mono()-t0,1), "unchanged:", before==sorted(os.listdir(D)), sorted(os.listdir(D)))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("BC-仅问答",BC,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
