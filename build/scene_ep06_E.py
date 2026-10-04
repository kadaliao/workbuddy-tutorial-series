import sys, hashlib, glob; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep06"; CM=os.path.expanduser("~/.workbuddy/commands")
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]
TXT="帮我创建一个斜杠指令 /周报速写，功能是读取当前文件夹的日报和数据表，生成四段式周报，只用材料里的内容，输出 Word。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def E6(h):
    c0=set(os.listdir(CM)); h.pause(0.8)
    h.move_to(640,395,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text(TXT,label="让它创建斜杠指令",target=BOX); h.pause(0.8)
    if not ocr.find("周报速写"): raise RuntimeError("not typed")
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50]); h.log("mark",text="send")
    t0=mono(); last=None; stable=0; tnew=None
    while mono()-t0 < 480:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if tnew is None and set(os.listdir(CM))-c0: tnew=mono()-t0; h.log("mark",text="file_created")
        if stable>=5 and tnew: break
    h.log("mark",text="done"); h.pause(1.0); print("E waited", round(mono()-t0,1), "new", set(os.listdir(CM))-c0, "at", tnew)
h=Human(); new_task(h); pick_folder(h, "/Users/Shared/技能调用")
scene("E-创建指令",E6,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
