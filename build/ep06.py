#!/usr/bin/env python3
"""第 6 集：把做过的活存成技能和斜杠指令。用法：ep06.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 6, "把做过的活存成技能和斜杠指令"
TEXT = {
 "A开场": "第一次写周报，我写了一大段需求。第二次，我只敲一个斜杠，选一个技能，再补一句话。差别在哪？我把第一次做顺的流程，存成了技能。",
 "B封装": "怎么存？第一次结果满意之后，接着对它说：记住这次任务的说明和格式要求，封装成一个技能，名字叫周报四段式。它会自己写好技能的说明和模板，一分多钟就存好了。",
 "C看技能": "存好之后去哪里看？左边，专家、技能、连接器，选技能，点我安装的。用户自定义下面，就是刚存的这个。右上角添加技能，还能查找技能、上传技能，或者直接创建技能。",
 "D调用": "下次怎么用？新建任务，在输入框里敲一个斜杠。下拉菜单分两组：技能和指令。选中周报四段式，再补一句：用这周的材料写周报。它就按上次定好的四段结构来写，不用重新交代。",
 "E自动": "还有一点：技能存好之后，你不点名，它也可能自己用上。有一次我只说了一句帮我写个周报，它就自己加载了之前存的周报技能。所以技能的说明要写准，别让它用错地方。",
 "F指令": "更省事的是斜杠指令。你对它说：帮我创建一个斜杠指令，周报速写，功能是读取当前文件夹的日报和数据表，生成四段式周报，输出 Word。它会在本机生成一个指令文件，两分钟左右就好了。",
 "G菜单": "新开一个任务，敲斜杠，往下翻到指令这一组，周报速写已经在里面了。以后选它回车就行。如果你那边没看到新指令，重新开个任务，或者重启一下再看。",
 "H收尾": "今天三句话：做顺了就存成技能，常用的做成斜杠指令，技能的说明要写准。下一集，认识专家和专家团。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F6 = K.F

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n); a2 = at(n, "第二次") - 0.2; a3 = at(n, "差别在哪") - 0.2
    P[n] = [("R", f"{F6}/A1-第一次写需求.mov", {"anchors": [[4.0, 0], [23.0, a2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "第一次", "set": {"zoom": 1.5, "label": "第一次：写一大段"}}],
                "badges": [{"from": 6.0, "to": 23.0, "text": "加速播放", "t0": 0}]}),
            ("R", f"{F6}/D-调用技能.mov", {"anchors": [[4.0, 0], [9.9, at(n,"选一个技能")-a2], [13.1, at(n,"再补一句")-a2], [17.0, a3-a2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "斜杠", "set": {"zoom": 1.6, "label": "第二次：一个斜杠"}}, {"contains": "技能", "set": {"label": None}},
                          {"contains": "选我的技能", "set": {"zoom": 1.5}}]}),
            ("R", f"{V}/footage/ep06/C-看技能.mov", {"anchors": [[14.0, 0], [14.0 + t - a3, t - a3]], "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 14.1, "kind": "move", "target": [298,110,350,100], "label": "存成了技能", "zoom": 1.8, "focus": True, "dur": t - a3}]})]
    n = "B封装"; t = T(n)
    P[n] = [("R", f"{F6}/B-封装技能.mov", {"anchors": [[3.0, 0], [5.0, at(n,"接着对它说")], [13.0, at(n,"它会自己")-0.4], [15.0, at(n,"它会自己")], [88.0, at(n,"一分多钟")+0.5], [92.6, t]],
                "events_shift": -65.2, "drop_masks": DROP, "masks_extra": [USER],
                "badges": [{"from": 15.0, "to": 86.0, "text": "加速播放 · 实际 {real}", "t0": 13.0}],
                "patch": [{"contains": "封装成技能", "set": {"zoom": 1.6}}],
                "events_extra": [{"t": 89.0, "kind": "move", "target": [855,90,585,770], "label": "技能的说明和模板", "zoom": 1.2, "dur": 2.8}]})]
    n = "C看技能"; t = T(n)
    P[n] = [("R", f"{F6}/C-看技能.mov", {"anchors": [[2.4, 0], [4.2, at(n,"左边")+0.8], [7.5, at(n,"选技能")+0.4], [11.7, at(n,"点我安装的")+0.5], [14.2, at(n,"用户自定义")], [18.7, at(n,"右上角")], [22.1, at(n,"还能查找")+0.4], [25.5, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO([[0, 3]])],
                "patch": [{"contains": "专家·技能", "set": {"zoom": 1.6}}, {"contains": "技能", "set": {"zoom": 1.8}}, {"contains": "我安装的", "set": {"zoom": 1.8}},
                          {"contains": "刚存的技能", "set": {"zoom": 1.8, "focus": True}}, {"contains": "添加技能", "set": {"zoom": 1.8}}],
                "events_extra": [{"t": 22.2, "kind": "move", "target": [1262,72,170,110], "label": "查找 · 上传 · 创建", "zoom": 2.0, "focus": True, "dur": 2.6}]})]
    n = "D调用"; t = T(n)
    P[n] = [("R", f"{F6}/D-调用技能.mov", {"anchors": [[3.4, 0], [5.0, at(n,"敲一个斜杠")+0.3], [8.0, at(n,"下拉菜单")], [9.9, at(n,"选中")], [13.1, at(n,"再补一句")], [18.3, at(n,"它就按")-0.4], [21.0, at(n,"它就按")], [205.0, at(n,"四段结构")], [215.0, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 21.0, "to": 203.0, "text": "加速播放 · 实际 {real}", "t0": 18.3}],
                "patch": [{"contains": "斜杠", "set": {"zoom": 1.6}}, {"contains": "技能", "set": {"zoom": 1.8, "label": "技能 / 指令 两组"}},
                          {"contains": "选我的技能", "set": {"zoom": 1.6, "focus": True}}],
                "events_extra": [{"t": 13.4, "kind": "move", "target": [454,358,500,40], "label": "技能 + 一句话", "zoom": 1.8, "dur": 3.0},
                                 {"t": 206.0, "kind": "move", "target": [855,170,585,690], "label": "按上次的四段结构", "zoom": 1.2, "dur": 4.0}]})]
    n = "E自动"; t = T(n); e2 = at(n, "所以技能") - 0.2
    P[n] = [("R", f"{F6}/X-技能被自动调用.mov", {"anchors": [[3.0, 0], [4.7, at(n,"有一次")], [7.8, at(n,"它就自己")-0.6], [16.0, at(n,"加载了")+0.3], [18.0, e2]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "只说一句", "set": {"zoom": 1.8, "label": "只说了一句"}}, {"contains": "发送", "set": {"label": None}}],
                "events_extra": [{"t": 15.0, "kind": "move", "target": [470,234,340,24], "label": "自己加载了周报技能", "zoom": 2.2, "focus": True, "dur": 3.0}]}),
            ("CARD", "e", t - e2, [{"from": 0, "to": t - e2, "last": True, "lines": [("技能的说明要写准", "b", 0.2), ("别让它用错地方", "s", 0.6)]}])]
    n = "F指令"; t = T(n)
    P[n] = [("R", f"{F6}/E-创建指令.mov", {"anchors": [[3.4, 0], [5.0, at(n,"你对它说")+0.3], [19.5, at(n,"它会在本机")-0.4], [22.0, at(n,"它会在本机")], [62.7, at(n,"指令文件")+0.3], [126.0, at(n,"两分钟")+0.8], [128.8, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 22.0, "to": 125.0, "text": "加速播放 · 实际 {real}", "t0": 19.5}],
                "patch": [{"contains": "创建斜杠指令", "set": {"zoom": 1.5}}]})]
    n = "G菜单"; t = T(n); g2 = at(n, "如果你那边") - 0.2
    P[n] = [("R", f"{F6}/F-斜杠菜单.mov", {"anchors": [[3.4, 0], [5.0, at(n,"敲斜杠")+0.3], [7.0, at(n,"往下翻")], [12.3, at(n,"周报速写")], [17.0, g2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "再敲斜杠", "set": {"label": None}}, {"contains": "新指令在这里", "set": {"zoom": 1.8, "focus": True}}]}),
            ("CARD", "g", t - g2, [{"from": 0, "to": t - g2, "last": True, "lines": [("没看到新指令？", "t", 0.15), ("重新开个任务，或重启一下", "b", 0.4)]}])]
    n = "H收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "h", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 做顺了就存成技能", "n", at(n,"做顺了")), ("② 常用的做成斜杠指令", "n", at(n,"常用的")), ("③ 技能的说明要写准", "n", at(n,"技能的说明"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("专家与专家团", "b", at(n,"认识专家"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep06-v1.mp4")
