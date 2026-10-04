import sys, hashlib; sys.path.insert(0,'.')
from human import *
DIR="/Users/Shared/周报素材"; DOCX=DIR+"/本周周报.docx"
USER=[8,795,180,55]; PROMO=[1240,0,200,34]
def sysev(code): subprocess.run(["osascript","-e",f'tell application "System Events" to key code {code}'])
def E(h):
    h.pause(1.0)
    h.move_to(531,521,target=[472,508,128,26],label="点这里选择工作空间"); h.pause(0.3,0.5); h.click(None,[472,508,128,26]); h.pause(0.9,1.3)
    h.move_to(547,478,target=[470,462,210,32],label="选「打开本地文件夹」"); h.pause(0.8,1.1); h.click(None,[470,462,210,32]); h.pause(1.6,2.0)
    h.move_to(640,320,dur=0.9,target=[420,265,520,95],label="只放 3 份日报 + 1 张数据表"); h.pause(2.2,2.6)
    h.move_to(1103,621,target=[1030,605,110,32],label="点「打开」"); h.pause(0.3,0.5); h.click(None,[1030,605,110,32]); h.pause(1.2)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/e_chk.png"])
    h.pause(0.6)
    h.move_to(560,560,dur=0.8,target=[472,508,150,26],label="工作空间选好了"); h.pause(2.0)
TXT="读取这个文件夹里的三份日报和数据表，写一份周报，分成本周完成、数据表现、问题与需求、下周计划四段，只用材料里的内容，不要编，输出成 Word，存在当前文件夹。"
BOX=[454,358,795,143]
def F(h):
    h.pause(1.0)
    h.move_to(640,395,target=BOX,label="点输入框"); h.pause(0.3,0.5); h.click(None,BOX); h.pause(0.7,1.0)
    h.type_text(TXT,label="写清：做什么、有什么材料、要什么结果",target=BOX)
    h.pause(1.0); h.jitter(1.0)
def snap():
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/poll.png"])
    return hashlib.md5(open("/private/tmp/claude-501/poll.png","rb").read()).hexdigest()
def G(h):
    h.pause(1.0)
    h.move_to(1220,473,target=[1195,448,50,50],label="点发送"); h.pause(0.4,0.6); h.click(None,[1195,448,50,50])
    t0=mono(); h.pause(1.0)
    mark={}; last=None; stable=0
    while mono()-t0 < 420:
        h.jitter(3.0)
        if "docx" not in mark and os.path.exists(DOCX):
            mark["docx"]=mono()-t0; h.log("wait",label="周报文件生成了",dur=0)
        hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if "docx" in mark and stable>=6: break
    h.log("wait",label="任务完成",dur=0)
    print("G marks",mark, "total", mono()-t0)
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep01"
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(1.0)
scene("E5-选工作空间",E,outdir=O,extra={"mask_regions":[{"name":"文件选择对话框左侧栏(含用户名)","rect":[288,216,134,430]},{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
time.sleep(0.5)
scene("F5-写需求",F,outdir=O,extra={"typed_text":TXT,"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
time.sleep(0.5)
scene("G5-执行",G,outdir=O,pre_wait=1.5,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
