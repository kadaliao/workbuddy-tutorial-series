import sys, hashlib; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep02"
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]
D="/Users/Shared/权限演示"
TXT="把这个文件夹里所有的 txt 文件都删掉。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def A2(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX,label="点输入框"); h.pause(0.3); h.click(None,BOX); h.pause(0.6)
    h.type_text(TXT,label="让它批量删除",target=BOX); h.pause(0.8)
    h.move_to(1220,473,target=[1195,448,50,50],label="发送"); h.pause(0.4); h.click(None,[1195,448,50,50])
    t0=mono(); last=None; stable=0; i=0; n0=len([f for f in os.listdir(D) if f.endswith(".txt")])
    while mono()-t0 < 180:
        h.jitter(2.5); i+=1
        hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        subprocess.run(["cp","/private/tmp/claude-501/poll.png",f"/private/tmp/claude-501/b_{i:03d}.png"])
        n=len([f for f in os.listdir(D) if f.endswith(".txt")])
        if n < n0: print("TXT COUNT", n, "at", round(mono()-t0,1)); n0=n
        if stable>=4: break
    print("A2 waited", round(mono()-t0,1), "txt left:", sorted(os.listdir(D)))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
h=Human(); h.move_to(529,333); h.click(); time.sleep(1.0); h.move_to(1210,176); h.click(); time.sleep(0.8)
scene("A2-批量删除",A2,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
