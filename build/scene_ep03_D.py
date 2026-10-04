import sys, hashlib; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep03"
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def D(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX,label="先写一句大白话"); h.pause(0.3); h.click(None,BOX); h.pause(0.5)
    h.type_text("把这几个日报整理成周报",target=BOX); h.pause(1.0)
    h.move_to(1064,472,dur=0.9,target=[1050,458,28,28],label="增强提示词"); h.pause(1.6); h.click(None,[1050,458,28,28])
    t0=mono(); last=None; stable=0
    while mono()-t0 < 40:
        h.jitter(1.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=3 and mono()-t0>6: break
    print("enhance took", round(mono()-t0,1))
    h.move_to(800,330,dur=0.8); h.pause(3.0)
    subprocess.run(["cp","/private/tmp/claude-501/poll.png","/private/tmp/claude-501/en2.png"])
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
h=Human(); h.move_to(640,395); h.click(); time.sleep(0.3); h.key(0, Quartz.kCGEventFlagMaskCommand); time.sleep(0.2); h.key(51); time.sleep(0.6)
scene("D-增强提示词",D,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
