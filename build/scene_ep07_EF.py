import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep07"
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def EF(h):
    h.pause(0.8)
    b=ocr.find("内容创作专家团",exact=True); h.move_to(*C(b),dur=0.8,target=tgt(b),label="打开一个专家团"); h.pause(0.5); h.click(); h.pause(2.0)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/team.png"]); h.log("mark",text="team")
    h.move_to(720,420,dur=0.8); h.pause(4.0)
    h.esc(); h.pause(0.8)
    if ocr.find("召唤专家团") or ocr.find("召唤"): h.move_to(1300,600); h.click(); h.pause(0.8)
    b=ocr.find("我的专家"); h.move_to(*C(b),dur=0.8,target=tgt(b),label="我的专家"); h.pause(0.5); h.click(); h.pause(2.0)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/mine.png"]); h.log("mark",text="mine")
    h.move_to(800,300,dur=0.8); h.pause(3.0)
h=Human(); new_task(h)
h.move_to(100,224); h.click(); time.sleep(1.0)
b=ocr.find("专家",exact=True,region=[200,150,300,200]); h.move_to(*C(b)); h.click(); time.sleep(2.0)
scene("EF-专家团与我的专家",EF,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
