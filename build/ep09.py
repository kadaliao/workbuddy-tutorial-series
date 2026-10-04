#!/usr/bin/env python3
"""第 9 集：定时任务。用法：ep09.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 9, "定时任务：让它每天自己上班"
TEXT = {
 "A开场": "这条记录，不是我手动点的。是我设好时间，它自己到点干完的。今天讲定时任务。",
 "B页面": "左边，定时任务。上面两个页签：定时任务，是你设好的计划；运行记录，是它每次跑的结果。右上角还能从模版添加。提醒一句：这个每周工作周报的模版，汇总的是代码仓库的进展，不是我们办公用的周报，别选错。",
 "C新建": "点添加定时任务。名称随便起。提示词，就是你平时对它说的话，同样要说清三件事。我写的是：读取当前文件夹，列出所有文件名和修改时间，生成一份文件清单，不要修改或删除任何文件。然后选工作空间，就是它干活的文件夹。",
 "D权限": "这里一定要停一下。权限这一项，默认是红色的，允许完全访问。定时任务是你不在场的时候跑的，更不能放开。点开，把它关掉，改回默认权限。",
 "E频率": "频率，第一次先用单次，时间设在几分钟后，跑一遍看看结果。下面两个同步开关，是把结果推到微信小程序或企业微信，用不上就关着。确定，任务就排上了。",
 "F看结果": "到点了，切到运行记录。这条就是它刚才自己跑的，状态是成功。点进去，文件清单已经生成了，还写明了这是只读扫描，原来的文件一个没动。",
 "G改成定期": "结果满意，再把频率改成每天、每周或者每月。我这个是演示，直接删掉。",
 "H收尾": "今天三句话：先单次试跑，权限改回默认，满意再定期。下一集，用手机遥控电脑，通勤路上派活。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F9 = K.F

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("R", f"{F9}/F-运行记录.mov", {"anchors": [[4.6, 0], [4.6 + t, t]], "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 4.9, "kind": "move", "target": [284,94,1136,32], "label": "它自己到点跑完的", "zoom": 1.8, "focus": True, "dur": t - 1.0}]})]
    n = "B页面"; t = T(n)
    P[n] = [("R", f"{F9}/B-页面与模版.mov", {"anchors": [[2.4, 0], [4.1, at(n,"左边")+0.6], [6.6, at(n,"上面两个")+0.4], [9.2, at(n,"运行记录")], [11.5, at(n,"右上角")], [17.2, at(n,"提醒一句")-0.6], [21.3, at(n,"这个每周")], [25.5, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO([[0, 3]])],
                "patch": [{"contains": "定时任务", "set": {"zoom": 1.6}}, {"contains": "计划", "set": {"zoom": 2.0, "label": "定时任务：计划"}},
                          {"contains": "每次跑", "set": {"zoom": 2.0, "label": "运行记录：结果"}}, {"contains": "从模版", "set": {"zoom": 2.0}},
                          {"contains": "现成的模版", "set": {"zoom": 1.2}}, {"contains": "代码仓库", "set": {"zoom": 1.8, "focus": True}}]})]
    n = "C新建"; t = T(n)
    P[n] = [("R", f"{F9}/C-新建.mov", {"anchors": [[2.4, 0], [4.3, at(n,"点添加")+0.6], [6.0, at(n,"名称")], [8.9, at(n,"提示词")], [10.5, at(n,"我写的是")], [20.8, at(n,"然后选工作空间")], [25.0, at(n,"就是它干活")], [27.7, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "添加定时任务", "set": {"zoom": 2.0}}, {"contains": "名称", "set": {"zoom": 1.6}}, {"contains": "提示词", "set": {"zoom": 1.5}},
                          {"contains": "选工作空间", "set": {"zoom": 1.8}}]})]
    n = "D权限"; t = T(n)
    P[n] = [("R", f"{F9}/D-权限.mov", {"anchors": [[2.4, 0], [3.7, at(n,"权限这一项")], [7.3, at(n,"点开")], [9.2, at(n,"把它关掉")-0.2], [12.4, at(n,"改回默认")-0.3], [13.8, at(n,"改回默认")+0.3], [17.6, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "红色", "set": {"zoom": 2.0, "focus": True}}, {"contains": "关掉", "set": {"zoom": 2.4, "focus": True}},
                          {"contains": "改回默认", "set": {"zoom": 2.0, "focus": True}}]})]
    n = "E频率"; t = T(n)
    P[n] = [("R", f"{F9}/E-频率与保存.mov", {"anchors": [[1.8, 0], [2.5, at(n,"频率")], [6.5, at(n,"下面两个")], [10.4, at(n,"确定")], [14.5, t]], "events_shift": -12.6,
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "单次", "set": {"zoom": 1.8, "focus": True}}, {"contains": "推送开关", "set": {"zoom": 1.8}}, {"contains": "确定", "set": {"zoom": 2.0}},
                          {"contains": "已添加", "set": {"zoom": 1.5, "label": "排上了"}}]})]
    n = "F看结果"; t = T(n)
    P[n] = [("R", f"{F9}/F-运行记录.mov", {"anchors": [[2.4, 0], [4.6, at(n,"切到")+0.6], [6.7, at(n,"这条就是")], [10.2, at(n,"点进去")+0.3], [12.7, at(n,"文件清单")], [19.1, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "运行记录", "set": {"zoom": 2.0}}, {"contains": "成功", "set": {"zoom": 1.8, "focus": True}}],
                "events_extra": [{"t": 13.5, "kind": "move", "target": [395,400,630,90], "label": "只读扫描，文件没动", "zoom": 1.5, "focus": True, "dur": 4.5}]})]
    n = "G改成定期"; t = T(n)
    P[n] = [("R", f"{F9}/G-改频率与删除.mov", {"anchors": [[2.4, 0], [6.7, at(n,"把频率")], [12.1, at(n,"每天")], [16.0, at(n,"我这个是演示")], [22.5, at(n,"直接删掉")-0.4], [29.5, at(n,"直接删掉")+1.2], [33.0, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "点开任务", "set": {"label": None}}, {"contains": "改频率", "set": {"zoom": 2.0}}, {"contains": "每天", "set": {"zoom": 1.8, "focus": True}},
                          {"contains": "删掉", "set": {"zoom": 2.0}}, {"contains": "确认删除", "set": {"zoom": 1.6, "focus": True}}]})]
    n = "H收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "h", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 先单次试跑", "n", at(n,"先单次")), ("② 权限改回默认", "n", at(n,"权限改回")), ("③ 满意再定期", "n", at(n,"满意再"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("用手机遥控电脑", "b", at(n,"用手机")), ("通勤路上派活", "s", at(n,"通勤"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep09-v1.mp4")
