import sys, hashlib, glob; sys.path.insert(0,'.')
from human import *
import ocr
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep04"; D="/Users/Shared/模式演示"
def C(b): return b[0]+b[2]/2, b[1]+b[3]/2
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def D3(h):
    h.pause(1.0)
    h.move_to(850,520,dur=0.8,target=[478,474,750,98],label="它写好的计划"); h.pause(3.0)
    b=ocr.find("开始执行",region=[470,670,780,60])
    h.move_to(*C(b),dur=0.7,target=[476,682,756,34],label="确认：开始执行"); h.pause(1.0); h.click(None,[476,682,756,34]); h.log("mark",text="exec")
    t0=mono(); last=None; stable=0; i=0
    while mono()-t0 < 420:
        h.jitter(2.5); i+=1; hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if i%5==0: subprocess.run(["cp","/private/tmp/claude-501/poll.png",f"/private/tmp/claude-501/x_{i:03d}.png"])
        x=glob.glob(D+"/*.xlsx")
        if x and stable>=4: break
    h.log("mark",text="exec_done"); h.pause(1.5)
    print("exec waited", round(mono()-t0,1), sorted(os.listdir(D)))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("D3-确认执行",D3,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
