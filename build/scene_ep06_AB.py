import sys, hashlib, glob; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep06"; os.makedirs(O, exist_ok=True)
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]; D="/Users/Shared/技能演示"
TXT="读取这个文件夹里的三份日报和数据表，写一份周报，分成本周完成、数据表现、问题与需求、下周计划四段，只用材料里的内容，不要编，查不到的写待确认，输出成 Word，存在当前文件夹。"
SK="记住这次任务的说明和格式要求，封装成一个技能，名字叫 周报四段式。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def wait(h, maxs, cond, mins=20):
    t0=mono(); last=None; stable=0
    while mono()-t0 < maxs:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=5 and mono()-t0>mins and cond(): break
    return round(mono()-t0,1)
def A1(h):
    h.pause(0.8)
    h.move_to(640,395,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text(TXT,label="第一次：写一大段",target=BOX); h.pause(0.8)
    if not ocr.find("三份日报"): raise RuntimeError("not typed")
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50])
    print("A1 waited", wait(h, 360, lambda: bool(glob.glob(D+"/*.docx"))))
    h.log("mark",text="done")
def B(h):
    sk0=set(os.listdir(os.path.expanduser("~/.workbuddy/skills"))); h.pause(0.8)
    box=None
    for s,b in ocr.all_text():
        if "今天帮你做些什么" in s: box=b
    x,y=(box[0]+200, box[1]+8) if box else (560,718)
    h.move_to(x,y,dur=0.7); h.pause(0.3); h.click(); h.pause(0.4)
    h.type_text(SK,label="满意了：封装成技能",target=[292,660,540,110]); h.pause(0.8)
    h.key(36); h.log("mark",text="send")
    print("B waited", wait(h, 360, lambda: set(os.listdir(os.path.expanduser("~/.workbuddy/skills")))-sk0 != set(), 40))
    h.log("mark",text="done")
    print("new skills", set(os.listdir(os.path.expanduser("~/.workbuddy/skills")))-sk0)
h=Human(); new_task(h); pick_folder(h, D)
scene("A1-第一次写需求",A1,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
time.sleep(1)
scene("B-封装技能",B,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER}]})
