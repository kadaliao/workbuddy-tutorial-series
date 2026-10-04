import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep06"
BOX=[454,358,795,143]
def F6(h):
    h.pause(0.8)
    h.move_to(640,395,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text("/",label="再敲斜杠",target=BOX); h.pause(1.4)
    h.move_to(800,200,dur=0.6); h.scroll(900,dur=1.6); h.pause(1.4)
    found=ocr.find("周报速写",region=[460,0,800,360]); g=ocr.find("指令",region=[460,0,200,360])
    print("found", found, "group", g)
    if found: h.move_to(found[0]+60,found[1]+8,dur=0.7,target=[found[0]-10,found[1]-8,700,found[3]+16],label="新指令在这里"); h.pause(2.6)
    elif g: h.move_to(g[0]+30,g[1]+8,dur=0.7,target=[g[0]-8,g[1]-6,90,g[3]+12],label="指令"); h.pause(2.6)
    h.log("mark",text="menu"); h.pause(1.0)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/f6.png"])
    h.esc(); h.pause(0.3); h.key(51); h.pause(0.6)
h=Human(); new_task(h)
scene("F-斜杠菜单",F6,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
