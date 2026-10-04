import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep07"; os.makedirs(O, exist_ok=True)
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def BC(h):
    h.pause(0.8)
    h.move_to(100,224,dur=0.8,target=[12,208,245,32],label="专家·技能·连接器"); h.pause(0.4); h.click(); h.pause(1.0)
    b=ocr.find("专家",exact=True,region=[200,150,300,200]); h.move_to(*C(b),dur=0.6,target=[b[0]-20,b[1]-8,120,b[3]+16],label="专家"); h.pause(0.5); h.click(); h.pause(2.0)
    h.move_to(700,230,dur=0.8,target=[290,150,1130,190],label="精选场景"); h.pause(2.4); h.log("mark",text="featured")
    b=ocr.find("专家团",region=[280,360,200,40]) or ocr.find("专家园",region=[280,360,200,40])
    tx=b[0]+b[2]-25 if b else 380; ty=(b[1]+b[3]/2) if b else 384
    h.move_to(tx,ty,dur=0.7,target=[tx-30,ty-14,60,28],label="专家团"); h.pause(0.4); h.click(); h.pause(2.0); h.log("mark",text="team_tab")
    h.move_to(800,600,dur=0.7,target=[290,450,1130,380],label="一组专家分工协作"); h.pause(2.6)
    h.move_to(310,384,dur=0.6); h.click(); h.pause(1.6); h.log("mark",text="expert_tab")
    b=ocr.find("全部",exact=True,region=[280,400,200,40]); h.move_to(*C(b),dur=0.7,target=[290,404,700,30],label="按行业筛选"); h.pause(2.4)
    b=ocr.find("内容创作专家",exact=True); h.move_to(*C(b),dur=0.8,target=tgt(b),label="选一个专家"); h.pause(0.6); h.click(); h.pause(1.8); h.log("mark",text="detail")
    h.move_to(700,250,dur=0.7,target=[420,130,600,160],label="擅长什么，一眼看清"); h.pause(2.6)
    b=ocr.find("召唤专家"); h.move_to(*C(b),dur=0.7,target=tgt(b),label="召唤专家"); h.pause(0.8); h.click(); h.pause(2.4); h.log("mark",text="summoned")
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/summon.png"])
h=Human(); new_task(h)
scene("BC-逛专家并召唤",BC,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34],"t":[[0,3]]}]})
