import sys, json; sys.path.insert(0,'.')
from human import *
from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, CGImageGetDataProvider, CGDataProviderCopyData, CGImageGetWidth, CGImageGetBytesPerRow
from Foundation import NSURL
ROWS={"新建任务":125,"助理":158,"项目":191,"专家·技能·连接器":225,"定时任务":258,"资料库":290,"更多":323}
def T(n): y=ROWS[n]; return [12,y-16,240,32]
def bubble_visible():
    # sample logical point (1100,250) region-relative: bubble bg is tinted (not white)
    subprocess.run(["screencapture","-x","-R",f"{80+1100},{40+250},4,4","/private/tmp/claude-501/px.png"])
    src=CGImageSourceCreateWithURL(NSURL.fileURLWithPath_("/private/tmp/claude-501/px.png"),None)
    img=CGImageSourceCreateImageAtIndex(src,0,None)
    d=bytes(CGDataProviderCopyData(CGImageGetDataProvider(img)))
    r,g,b=d[0],d[1],d[2]   # BGRA or RGBA; just test non-white
    return not (r>245 and g>245 and b>245)
def visit(h,name,label,stay):
    h.move_to(110,ROWS[name],target=T(name)); h.pause(0.2,0.3)
    h.click(label,T(name)); h.pause(*stay)
def run(h):
    h.pause(1.8)
    visit(h,"助理","助理：手机遥控电脑",(2.5,2.6))
    visit(h,"项目","项目：团队协作",(2.5,2.6))
    # expert/skills/connectors with flyout sweep
    h.move_to(110,ROWS["专家·技能·连接器"],target=T("专家·技能·连接器")); h.pause(0.2,0.3)
    h.click("专家·技能·连接器：工具箱",T("专家·技能·连接器")); h.pause(0.6,0.8)
    h.move_to(295,233,dur=0.6,target=[241,210,158,114],label="专家、技能、连接器",overshoot=False); h.pause(0.35)
    h.move_to(294,267,dur=0.5,overshoot=False); h.pause(0.35)
    h.move_to(301,301,dur=0.5,overshoot=False); h.pause(0.9,1.1)
    visit(h,"定时任务","定时任务：让它定点干活",(2.5,2.6))
    visit(h,"资料库","资料库：放成品和资料",(2.5,2.6))
    visit(h,"更多","更多：低频入口",(2.5,2.6))
    h.move_to(110,ROWS["新建任务"],target=T("新建任务")); h.pause(0.2,0.3)
    h.click("新建任务：天天用它",T("新建任务")); h.pause(1.0,1.2)
    if bubble_visible():
        h.move_to(1210,176,dur=0.7); h.pause(0.2,0.3); h.click(None); h.pause(0.5)
    h.move_to(900,650,dur=0.9); h.pause(1.2,1.3)
h=scene("D-侧栏巡览",run,park=(900,720),pre_wait=1.0,extra={})
# post: mask intervals
p="../footage/ep01/D-侧栏巡览"
ev=json.load(open(p+".events.json")); meta=json.load(open(p+".meta.json"))
tl=lambda s:next(e["t"] for e in ev if e.get("label","").startswith(s))
t0,t1=tl("资料库"),tl("更多")
rows=[("本周周报行所有者(昵称 Kada)",214),("所有者(他人用户名)",262),("所有者(他人用户名)",310),("所有者(他人用户名)",358),("所有者(昵称 Kada)",406)]
mr=[{"name":"侧栏左下用户行(头像+昵称)","rect":[8,795,180,55],"t":[0,meta["duration"]]}]
mr+=[{"name":"资料库页-"+n,"rect":[908,y,85,20],"t":[round(t0,2),round(t1,2)]} for n,y in rows]
mr.append({"name":"右上推广按钮(关不掉)","rect":[1240,0,200,34],"t":[0,meta["duration"]],"note":"仅新建任务页出现"})
meta["mask_regions"]=mr
json.dump(meta,open(p+".meta.json","w"),ensure_ascii=False,indent=1)
print("duration",meta["duration"],"lib interval",t0,t1)
