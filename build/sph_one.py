import sys, json; sys.path.insert(0,'.')
from sph import *
i=int(sys.argv[1]); P=json.load(open(V+"/publish/sph_posts.json"))[i-1]
hh,mm=22,40+(i-1)
log=lambda *a: print(f"[ep{i}]",*a, flush=True)
subprocess.run(["osascript","-e",'tell application "WeChat" to activate']); time.sleep(0.5)
# 1 打开发表页
b=find("发表视频")
if not b:
    H.move_to(1500,500,dur=0.3)
    for k in range(8): post(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 2, 0, -100)); time.sleep(0.05)
    time.sleep(0.8); b=find("发表视频",tries=3)
H.move_to(*C(b),dur=0.4); H.click(); time.sleep(2.5)
H.move_to(1500,500,dur=0.3)
for k in range(8): post(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 2, 0, 100)); time.sleep(0.05)
time.sleep(0.5)
up=find("上传时长",tries=4); assert up, "no upload box"
H.move_to(up[0]+70, up[1]-40, dur=0.4); H.click(); choose_file(V+"/"+P["file"])
# 2 等上传完成（出现封面预览）
for k in range(90):
    if find("封面预览") and not find("取消上传"): break
    time.sleep(2)
log("uploaded")
# 3 描述 + 短标题
b=find("添加描述",tries=3); H.move_to(*C(b),dur=0.4); H.click(); time.sleep(0.5)
paste(P["desc"]+"\n"+" ".join("#"+t for t in P["tags"])+" "); time.sleep(1.0)
b=find("填写短标题",tries=3); H.move_to(*C(b),dur=0.4); H.click(); time.sleep(0.4)
paste(P["short"]); time.sleep(0.6)
# 4 封面
e=[bb for s,bb in ocr.all_text() if s.strip()=="编辑" and bb[0]>1550 and bb[1]<450]
e.sort()
pe=e[0] if e else (1630,345,10,10)
H.move_to(pe[0]+10,pe[1]-5,dur=0.4); H.click(); time.sleep(2.0)
b=find("上传封面",tries=3); H.move_to(b[0]+b[2]/2, b[1]-40, dur=0.4); H.click(); choose_file(f"{V}/publish/covers/ep{i:02d}-3x4.png")
b=find("确认",exact=True,region=[1600,800,250,100],tries=3); H.move_to(*C(b),dur=0.4); H.click(); time.sleep(2.0)
d=find("直接编辑")
if not d:
    e=[bb for s,bb in ocr.all_text() if s.strip()=="编辑" and bb[0]>1650 and bb[1]<450]
    se=e[-1] if e else (1757,345,10,10); H.move_to(se[0]+10,se[1]-5,dur=0.4); H.click(); time.sleep(2.0); d=find("直接编辑")
if d: H.move_to(*C(d),dur=0.4); H.click(); time.sleep(2.0)
b=find("上传封面",tries=3); H.move_to(b[0]+b[2]/2, b[1]-40, dur=0.4); H.click(); choose_file(f"{V}/publish/covers/ep{i:02d}-4x3.png")
b=find("确认",exact=True,region=[1600,800,250,100],tries=3); H.move_to(*C(b),dur=0.4); H.click(); time.sleep(1.5)
log("covers")
# 5 合集、活动、定时
scroll_down(12)
if not find("Buddy零基础实战"):
    b=find("选择合集",tries=2); H.move_to(*C(b),dur=0.3); H.click(); time.sleep(1.5)
    c=find("Buddy零基础实战",tries=3); H.move_to(*C(c),dur=0.3); H.click(); time.sleep(1.0)
b=find("不参与活动")
if b:
    H.move_to(*C(b),dur=0.4); H.click(); time.sleep(1.0)
    s=find("搜索活动",tries=2); H.move_to(*C(s),dur=0.3); H.click(); time.sleep(0.3)
    paste("WorkBuddy"); time.sleep(2.5)
    a=find("有事Buddy",tries=3) or find("腾讯WorkBuddy",tries=2)
    H.move_to(*C(a),dur=0.4); H.click(); time.sleep(1.0)
b=find("定时",exact=True,region=[1650,450,150,100]) or find("◎ 定时")
t=find("定时发表"); H.move_to(t[0]+175,t[1]+9,dur=0.4); H.click(); time.sleep(1.0)
scroll_down(20)
ft=find("发表时间",tries=2); H.move_to(ft[0]+190,ft[1]+10,dur=0.4); H.click(); time.sleep(1.2)
ten=find("10",exact=True,region=[1810,650,40,200],tries=2)
H.move_to(1645,ten[1]+8,dur=0.3); H.click(); time.sleep(0.8)
tf=find("时间",exact=True,region=[1600,880,100,80]); H.move_to(tf[0]+130,tf[1]+8,dur=0.3); H.click(); time.sleep(0.5)
H.key(0, Quartz.kCGEventFlagMaskCommand); time.sleep(0.2); paste(f"{hh}:{mm:02d}"); time.sleep(0.5)
subprocess.run(["osascript","-e",'tell application "System Events" to key code 36']); time.sleep(0.6)
H.move_to(1300,600,dur=0.3); H.click(); time.sleep(1.0)
txt=" | ".join(s for s,bb in ocr.all_text() if bb[0]>1450)
ok = f"2026-10-04 {hh}:{mm:02d}" in txt and "Buddy零基础实战" in txt and "有事Buddy" in txt
log("check", ok, f"{hh}:{mm:02d}")
shot(f"ep{i:02d}_form")
if not ok: log("ABORT before publish"); sys.exit(2)
b=find("发表",exact=True,region=[1830,700,90,150]); H.move_to(*C(b),dur=0.4); H.click(); time.sleep(5)
ok2 = find(f"{hh}:{mm:02d}发表",tries=3) or find(f"{mm:02d}发表",tries=2)
log("published", bool(ok2))
