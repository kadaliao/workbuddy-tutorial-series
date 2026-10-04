import sys, hashlib; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep02"
USER=[8,795,180,55]; D="/Users/Shared/权限演示"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def A3(h):
    h.pause(1.0)
    h.move_to(850,538,dur=0.9,target=[476,522,760,34],label="它停下来问我"); h.pause(2.2)
    h.move_to(150,512,dur=0.9,target=[14,498,238,28],label="侧栏：待确认"); h.pause(1.8)
    h.move_to(760,579,dur=0.9,target=[476,562,756,156],label="给了几个选项"); h.pause(2.4)
    h.move_to(600,698,dur=0.7,target=[476,682,756,34],label="选「取消，不动任何文件」"); h.pause(0.6); h.click(None,[476,682,756,34])
    t0=mono(); last=None; stable=0
    while mono()-t0 < 60:
        h.jitter(2.0); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=3: break
    h.pause(1.0)
    print("A3 files:", sorted(os.listdir(D)))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("A3-拒绝删除",A3,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER}]})
