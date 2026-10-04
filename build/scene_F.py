import sys; sys.path.insert(0,'.')
from human import *
TXT="读取这个文件夹里的三份日报和数据表，写一份周报，分成本周完成、数据表现、问题与需求、下周计划四段，只用材料里的内容，不要编，输出成 Word，存在当前文件夹。"
BOX=[454,358,795,143]
def run(h):
    h.pause(1.0,label="工作空间已选好")
    h.move_to(640,395,target=BOX,label="点输入框"); h.pause(0.3,0.5); h.click("点输入框开始写需求",BOX); h.pause(0.7,1.0)
    h.type_text(TXT,label="输入需求：做什么+有什么材料+要什么结果",target=BOX)
    h.pause(1.0,label="写完停一下")
    h.jitter(1.0)
scene("F-写需求",run,extra={"typed_text":TXT,"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
