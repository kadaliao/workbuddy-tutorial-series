import sys, hashlib; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep03"; os.makedirs(O, exist_ok=True)
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]
D="/Users/Shared/需求演示"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def A(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX,label="点输入框"); h.pause(0.3); h.click(None,BOX); h.pause(0.6)
    h.type_text("帮我写个周报。",label="只说一句",target=BOX); h.pause(0.8)
    h.move_to(1220,473,target=[1195,448,50,50],label="发送"); h.pause(0.4); h.click(None,[1195,448,50,50])
    t0=mono(); last=None; stable=0; i=0
    while mono()-t0 < 300:
        h.jitter(3.0); i+=1
        hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if i%3==0: subprocess.run(["cp","/private/tmp/claude-501/poll.png",f"/private/tmp/claude-501/v_{i:03d}.png"])
        if stable>=5 and mono()-t0>30: break
    print("A waited", round(mono()-t0,1), sorted(os.listdir(D)))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("A-模糊指令",A,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
