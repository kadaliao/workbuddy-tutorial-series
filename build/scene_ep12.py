import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep12"; os.makedirs(O, exist_ok=True)
CI="回答先给结论；数字保留一位小数；不确定的写待确认。"
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
class Abort(Exception): pass
def BC(h):
    h.pause(0.8)
    h.move_to(36,826,dur=0.8,target=[14,808,160,36],label="左下角头像"); h.pause(0.5); h.click(); h.pause(1.0)
    h.move_to(70,551,dur=0.8,target=[22,536,296,32],label="设置"); h.pause(0.6); h.click(hold=0.12); h.pause(1.8)
    n=subprocess.run(["osascript","-e",'tell application "System Events" to tell process "WorkBuddy" to count windows'],capture_output=True,text=True).stdout.strip()
    if n!="2": h.esc(); h.pause(0.3); h.key(43, Quartz.kCGEventFlagMaskCommand); h.pause(1.6)
    h.move_to(487,350,dur=0.8,target=[442,334,200,34],label="个性化"); h.pause(0.4); h.click(); h.pause(1.6)
    h.move_to(900,350,dur=0.8,target=[664,312,650,60],label="自定义指令：每次都生效"); h.pause(2.2)
    h.move_to(900,400,dur=0.6); h.click(); h.pause(0.5)
    h.type_text(CI,label="写下每次都要遵守的规则",target=[664,370,650,160]); h.pause(1.0)
    if not ocr.find("一位小数"): raise Abort("ci not typed")
    b=ocr.find("/1500"); 
    if b: h.move_to(*C(b),dur=0.6,target=tgt(b),label="最多 1500 字"); h.pause(2.0)
    h.log("mark",text="typed")
    h.move_to(900,620,dur=0.7,target=[664,580,650,150],label="称呼与身份"); h.pause(2.2)
    # 恢复：清空自定义指令
    h.move_to(900,400,dur=0.5); h.click(); h.pause(0.3); h.key(0, Quartz.kCGEventFlagMaskCommand); h.pause(0.2); h.key(51); h.pause(0.6)
    h.move_to(900,200,dur=0.4); h.click(); h.pause(0.8)
    h.log("mark",text="restored")
    if not ocr.find("0/1500"): print("WARN ci not empty")
def D(h):
    h.pause(0.6)
    h.move_to(510,386,dur=0.8,target=[442,370,200,34],label="记忆与进化"); h.pause(0.4); h.click(); h.pause(1.6)
    h.move_to(900,180,dur=0.8,target=[664,150,650,80],label="生成对话记忆：开关"); h.pause(2.4)
    h.move_to(800,106,dur=0.6,target=[664,86,650,44],label="仅你本人可见"); h.pause(2.2)
    h.move_to(800,292,dur=0.6,target=[664,270,650,44],label="每晚整理，可查看、编辑"); h.pause(2.4)
    h.move_to(450,76,dur=0.8); h.click(); h.pause(1.0)
def E(h):
    h.pause(0.6)
    h.move_to(1118,472,dur=0.8,target=[1090,458,64,28],label="模型在这里"); h.pause(0.4); h.click(); h.pause(1.4)
    h.move_to(960,175,dur=0.7,target=[826,124,310,100],label="快速 / 均衡 / 极致"); h.pause(2.6)
    h.move_to(1100,175,dur=0.6,target=[1074,124,62,100],label="消耗倍率"); h.pause(2.2)
    h.move_to(960,300,dur=0.7,target=[826,226,310,150],label="也能直接选模型"); h.pause(2.2)
    h.move_to(900,108,dur=0.6,target=[826,90,310,34],label="Max 模式：耗积分快"); h.pause(2.4)
    h.esc(); h.pause(0.8)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
h=Human(); new_task(h)
M={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]},
    {"name":"菜单昵称","rect":[22,240,130,38],"t":[[4,8]]},{"name":"菜单积分","rect":[222,350,100,30],"t":[[4,8]]}]}
scene("BC-个性化",BC,outdir=O,extra=M)
scene("D-记忆",D,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
new_task(h)
scene("E-模型",E,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
