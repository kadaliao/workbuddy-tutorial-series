import sys, hashlib; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep05"; os.makedirs(O, exist_ok=True)
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]; D="/Users/Shared/验收演示"
TXT="读取这个文件夹里的三份日报和数据表，写一份周报，分本周完成、数据表现、问题与需求、下周计划四段，输出成 Word，存在当前文件夹。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def A(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text(TXT,label="这次不加两个限制",target=BOX); h.pause(0.8)
    if not ocr.find("三份日报"): raise RuntimeError("not typed")
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50])
    t0=mono(); last=None; stable=0
    while mono()-t0 < 360:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=5 and mono()-t0>40 and any(f.endswith(".docx") for f in os.listdir(D)): break
    h.log("mark",text="done"); h.pause(1.0)
    print("A waited", round(mono()-t0,1), sorted(os.listdir(D)))
h=Human(); new_task(h); pick_folder(h, D)
scene("A-陷阱版周报",A,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
