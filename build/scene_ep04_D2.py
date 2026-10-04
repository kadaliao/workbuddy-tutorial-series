import sys, hashlib, glob; sys.path.insert(0,'.')
from human import *
import ocr
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep04"; D="/Users/Shared/模式演示"
def C(b): return b[0]+b[2]/2, b[1]+b[3]/2
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def wait_stable(h, maxs, mins=5):
    t0=mono(); last=None; stable=0
    while mono()-t0 < maxs:
        h.jitter(2.0); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=3 and mono()-t0>mins: break
    return mono()-t0
def D2(h):
    h.pause(1.0)
    for i in range(6):
        hdr=[(s,b) for s,b in ocr.all_text() if b[1]>580 and ("/4" in s or "/3" in s or "/5" in s or "/2" in s)]
        opt=ocr.find("推荐",region=[470,630,780,60]) or ocr.find("Recommended",region=[470,630,780,60])
        if not opt: break
        h.move_to(C(opt)[0],C(opt)[1],dur=0.7,target=[476,642,756,34],label="选推荐项" if i==0 else None); h.pause(0.9); h.click(None,[476,642,756,34]); h.log("mark",text=f"answer{i}")
        h.pause(1.6)
    sub=ocr.find("提交",region=[1050,740,200,80])
    if sub: h.move_to(*C(sub),dur=0.6); h.pause(0.5); h.click(); h.log("mark",text="submit")
    w=wait_stable(h, 300, 10); h.log("mark",text="plan_ready"); print("plan ready after", round(w,1))
    subprocess.run(["cp","/private/tmp/claude-501/poll.png","/private/tmp/claude-501/plan_ready.png"])
D2.__name__="D2"
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("D2-回答问题",D2,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
