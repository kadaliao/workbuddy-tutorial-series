import sys, glob, hashlib; sys.path.insert(0,'.')
from human import *
DOCX=os.path.expanduser("~/WorkBuddy-demo/本周周报.docx")
def snap():
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/poll.png"])
    return hashlib.md5(open("/private/tmp/claude-501/poll.png","rb").read()).hexdigest()
def run(h):
    h.pause(1.0,label="需求已写好")
    h.move_to(1220,473,target=[1195,448,50,50],label="点发送"); h.pause(0.4,0.6); h.click("点发送按钮",[1195,448,50,50])
    t0=mono(); h.pause(1.0,label="开始执行")
    mark={}
    last=None; stable=0
    while mono()-t0 < 420:
        h.jitter(3.0)
        if "docx" not in mark and os.path.exists(DOCX):
            mark["docx"]=mono()-t0; h.log("wait",label="本周周报.docx 已生成到文件夹",dur=0)
        hs=snap()
        if hs==last: stable+=1
        else: stable=0
        last=hs
        if "docx" in mark and stable>=6: break
    h.log("wait",label="任务结束",dur=0)
    h.extra={"docx_at_s":mark.get("docx")}
h=scene("G-执行",run,pre_wait=1.5,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]},{"name":"注意：执行过程中若出现完整本地路径含用户名需后期遮盖(见 03-hands-on-log 检查记录)","rect":[0,0,0,0]}]})
