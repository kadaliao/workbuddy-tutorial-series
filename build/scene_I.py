import sys; sys.path.insert(0,'.')
from human import *
def run(h):
    h.pause(1.0,label="新建任务页，输入框下方有“默认权限”")
    h.move_to(655,521,target=[610,509,100,24],label="点“默认权限”"); h.pause(0.3,0.5); h.click("点“默认权限”",[610,509,100,24]); h.pause(1.0,1.3)
    h.move_to(660,477,target=[612,462,180,30],label="这里是“允许完全访问”开关"); h.pause(0.6)
    h.move_to(772,477,dur=0.6,target=[742,465,60,24],label="开关是关着的，不要打开"); h.pause(3.0,3.3,label="悬停 3 秒，不点击")
    h.esc(); h.pause(1.2,label="Esc 关闭菜单")
    h.move_to(900,700,dur=0.8); h.pause(1.0)
scene("I-权限",run,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}],"note":"全程未点击开关"})
