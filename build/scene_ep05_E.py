import sys, hashlib; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep05"; D="/Users/Shared/验收演示"
BOX=[292,676,540,90]
TXT="三处改一下：第一段的“均在当周完成响应”“恢复线上线索正常收集”，第三段的“已完成多家比价”，第四段后两条计划，材料里都没有，请删掉，只按日报原话写。投诉数保持“未填报”。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def E(h):
    m0=os.path.getmtime(D+"/工作周报.docx"); h.pause(0.8)
    h.move_to(560,718,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4)
    h.type_text(TXT,label="指出具体位置",target=[292,676,540,90]); h.pause(0.8)
    if not ocr.find("多家比价",region=[280,600,560,200]): raise RuntimeError("not typed")
    h.key(36); h.log("mark",text="send")
    t0=mono(); last=None; stable=0
    while mono()-t0 < 360:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=5 and mono()-t0>30 and os.path.getmtime(D+"/工作周报.docx")!=m0: break
    h.log("mark",text="done"); h.pause(1.0)
    print("E waited", round(mono()-t0,1))
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("E-指出问题",E,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
