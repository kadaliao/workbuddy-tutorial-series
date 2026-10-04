import sys, hashlib; sys.path.insert(0,'.')
from human import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep02"; os.makedirs(O, exist_ok=True)
USER=[8,795,180,55]; PROMO=[1240,0,200,34]
def B(h):
    h.pause(1.0)
    h.move_to(531,521,target=[472,508,128,26],label="点「选择工作空间」"); h.pause(0.3,0.5); h.click(None,[472,508,128,26]); h.pause(0.9,1.2)
    h.move_to(547,478,target=[470,462,210,32],label="选「打开本地文件夹」"); h.pause(0.6,0.9); h.click(None,[470,462,210,32]); h.pause(1.8,2.1)
    h.move_to(640,330,dur=0.9,target=[400,250,520,100],label="演示文件夹：素材副本 + 测试文件"); h.pause(2.0,2.4)
    h.move_to(1103,621,target=[1030,605,110,32],label="点「打开」"); h.pause(0.3,0.5); h.click(None,[1030,605,110,32]); h.pause(1.4)
    h.move_to(560,560,dur=0.8,target=[472,508,150,26],label="输入框下方显示文件夹名"); h.pause(2.2)
TXT="把这个文件夹里的 测试.txt 删掉。"
BOX=[454,358,795,143]
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def A(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX,label="点输入框"); h.pause(0.3); h.click(None,BOX); h.pause(0.6)
    h.type_text(TXT,label="让它删掉测试文件",target=BOX); h.pause(0.8)
    h.move_to(1220,473,target=[1195,448,50,50],label="发送"); h.pause(0.4); h.click(None,[1195,448,50,50])
    t0=mono(); last=None; stable=0; i=0
    while mono()-t0 < 150:
        h.jitter(2.5)
        hs=snap(); stable = stable+1 if hs==last else 0; last=hs; i+=1
        if i % 4 == 0: subprocess.run(["cp","/private/tmp/claude-501/poll.png",f"/private/tmp/claude-501/a_{i:03d}.png"])
        if not os.path.exists("/Users/Shared/权限演示/测试.txt"): h.log("wait",label="文件被删了",dur=0); print("DELETED at",mono()-t0)
        if stable>=5: break
    print("A waited", mono()-t0, "file exists:", os.path.exists("/Users/Shared/权限演示/测试.txt"))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.8)
scene("B-选工作空间",B,outdir=O,extra={"mask_regions":[{"name":"对话框侧栏","rect":[282,208,142,444]},{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
time.sleep(0.5)
scene("A-删除测试",A,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
