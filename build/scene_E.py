import sys; sys.path.insert(0,'.')
from human import *
def run(h):
    h.pause(1.0,label="新建任务页")
    h.move_to(531,521,target=[472,508,128,26],label="点这里选择工作空间"); h.pause(0.3,0.5); h.click("点“选择工作空间”",[472,508,128,26]); h.pause(0.9,1.3)
    h.move_to(547,478,target=[470,462,210,32],label="选“打开本地文件夹”"); h.pause(0.8,1.1,label="看下拉选项"); h.click("点“打开本地文件夹”",[470,462,210,32]); h.pause(1.6,2.0,label="系统选择文件夹对话框")
    h.move_to(700,238+0,dur=0.8,target=[675,222,225,24],label="确认是 WorkBuddy-demo 文件夹"); h.pause(1.4,1.8)
    h.move_to(1103,621,target=[1030,605,110,32],label="点“打开”确认"); h.pause(0.3,0.5); h.click("点“打开”",[1030,605,110,32]); h.pause(1.5,1.8,label="对话框关闭")
    h.move_to(560,560,dur=0.8,target=[472,508,200,26],label="输入框下方已显示 WorkBuddy-demo"); h.pause(2.0,label="工作空间已选中")
scene("E-选工作空间",run,extra={"mask_regions":[{"name":"文件选择对话框左侧栏(含用户名、私人收藏)，整块遮盖","rect":[288,216,134,430],"visible_during_s":"对话框出现期间"},{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
