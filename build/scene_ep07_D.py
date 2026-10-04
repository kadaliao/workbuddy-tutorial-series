import sys, hashlib; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep07"; D="/Users/Shared/周报素材"
BOX=[454,358,795,143]
TXT="把这个文件夹里的周报改写成一段给领导看的简短汇报，100 字以内，只用周报里的内容。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def D7(h):
    h.pause(0.8)
    h.move_to(560,474,dur=0.8,target=[500,460,130,28],label="专家已就位"); h.pause(1.8)
    h.move_to(800,395,dur=0.7,target=[454,358,795,40],label="预填了一个示例需求"); h.pause(1.8)
    h.click(); h.pause(0.3); h.key(0, Quartz.kCGEventFlagMaskCommand); h.pause(0.2); h.key(51); h.pause(0.6)
    h.type_text(TXT,label="换成我的需求",target=BOX); h.pause(0.8)
    if not ocr.find("简短汇报"): raise RuntimeError("not typed")
    if not ocr.find("内容创作专家",region=[450,440,800,60]): raise RuntimeError("chip lost")
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50]); h.log("mark",text="send")
    t0=mono(); last=None; stable=0
    while mono()-t0 < 300:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=5 and mono()-t0>25: break
    h.log("mark",text="done"); h.pause(1.0); print("D waited", round(mono()-t0,1), os.listdir(D))
    subprocess.run(["cp","/private/tmp/claude-501/poll.png","/private/tmp/claude-501/d7end.png"])
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
h=Human()
if ocr.find("活动"): h.move_to(1210,176); h.click(); time.sleep(0.6)
pick_folder(h, D)
scene("D-专家干活",D7,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
