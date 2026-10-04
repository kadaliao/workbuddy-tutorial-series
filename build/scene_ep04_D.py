import sys, hashlib; sys.path.insert(0,'.')
from human import *
import ocr
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep04"
USER=[8,795,180,55]; PROMO=[1240,0,200,34]; BOX=[454,358,795,143]; D="/Users/Shared/模式演示"
TXT="读取三份日报和数据表，统计每天完成了几件事，算出四项指标的环比，最后生成一份 Excel 汇总表。"
def C(b): return b[0]+b[2]/2, b[1]+b[3]/2
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
class Abort(Exception): pass
def D1(h):
    h.pause(0.8)
    h.move_to(480,472,dur=0.8,target=[466,458,28,28],label="点「+」"); h.pause(0.4); h.click(None,[466,458,28,28]); h.pause(1.0)
    b=ocr.find("模式",exact=True,region=[440,150,300,330])
    if not b:
        h.click(None,[466,458,28,28]); h.pause(1.0); b=ocr.find("模式",exact=True,region=[440,150,300,330])
    if not b: raise Abort("no 模式")
    x,y=C(b); h.move_to(x+20,y,dur=0.7,target=[b[0]-30,b[1]-8,182,b[3]+16]); h.pause(1.0)
    h.move_to(720,y,dur=0.5); h.pause(0.6)          # 先水平移进子菜单，避免路过「专家」行
    p=ocr.find("计划",exact=True,region=[640,150,300,330]); q=ocr.find("仅问答",exact=True,region=[640,150,300,330])
    if not p or not q or not (20 < q[1]-p[1] < 50): raise Abort(f"mode submenu not found {p} {q}")
    tx,ty=p[0]+152,p[1]+p[3]/2
    h.move_to(tx,ty,dur=0.6,target=[p[0]-8,p[1]-8,184,p[3]+16],label="打开「计划」"); h.pause(0.8); h.click(None,[tx-15,ty-10,30,20]); h.log("mark",text="plan_on"); h.pause(1.2)
    h.esc(); h.pause(0.4); h.esc(); h.pause(0.6)
    ind=ocr.find("计划",region=[450,440,800,60])
    if not ind: raise Abort("plan indicator missing")
    if ocr.find("工程师"): raise Abort("expert chip present")
    h.move_to(640,395,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text(TXT,label="一个多步任务",target=BOX); h.pause(0.8)
    if not ocr.find("统计每天"): raise Abort("text not typed")
    h.move_to(1220,473,target=[1195,448,50,50],label="发送"); h.pause(0.4); h.click(None,[1195,448,50,50])
    t0=mono(); last=None; stable=0
    while mono()-t0 < 300:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=4 and mono()-t0>20: break
    h.log("mark",text="plan_done"); h.pause(1.0)
    print("plan waited", round(mono()-t0,1), sorted(os.listdir(D)))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
h=Human(); h.move_to(76,124); h.click(); time.sleep(1.8)
b=ocr.find("活动")
if b: h.move_to(1210,176); h.click(); time.sleep(0.6)
h.move_to(531,521); h.click(); time.sleep(1.2)
w=ocr.find("模式演示",exact=True,region=[440,100,300,420])
print("ws item", w); h.move_to(*C(w)); h.click(); time.sleep(1.0)
assert ocr.find("模式演示",region=[440,500,300,40]), "workspace not set"
scene("D1-计划",D1,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER},{"name":"右上推广按钮","rect":PROMO}]})
