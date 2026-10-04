import sys, hashlib, glob; sys.path.insert(0,'.')
from wslib import *
import human
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep06"; D="/Users/Shared/技能调用"
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def D6(h):
    h.pause(0.8)
    h.move_to(640,395,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text("/",label="敲一个斜杠",target=BOX); h.pause(1.4)
    a=ocr.find("技能（") or ocr.find("技能(")
    b=ocr.find("周报四段式",region=[460,0,800,340])
    if not b: raise RuntimeError("skill not in menu")
    h.move_to(a[0]+30,a[1]+8,dur=0.6,target=[a[0]-8,a[1]-6,90,a[3]+12],label="技能") if a else None; h.pause(1.2)
    h.move_to(b[0]+60,b[1]+8,dur=0.7,target=[b[0]-10,b[1]-8,740,b[3]+16],label="选我的技能"); h.pause(1.0); h.click(); h.pause(1.2)
    h.log("mark",text="picked")
    h.type_text("用这周的材料写周报。",target=BOX); h.pause(1.0)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/d6typed.png"])
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50]); h.log("mark",text="send")
    t0=mono(); last=None; stable=0
    while mono()-t0 < 360:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=5 and mono()-t0>30 and glob.glob(D+"/*.docx"): break
    h.log("mark",text="done"); h.pause(1.0); print("D waited", round(mono()-t0,1), os.listdir(D))
h=Human(); new_task(h); pick_folder(h, D)
scene("D-调用技能",D6,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
