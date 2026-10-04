#!/usr/bin/env python3
"""第 3 集：一句话说清需求。用法：ep03.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 3, "一句话说清需求"
TEXT = {
 "A开场": "同一份材料，两种说法。第一种，我只说了一句：帮我写个周报。它也写出来了，看着还挺像样。但仔细看，它自己分成了五段，还多了好几句材料里根本没有的话，比如线上线索收集恢复正常，交付节奏和责任边界已明确。第二种，是第一集里我把需求说清楚的版本：四段，结构是我定的，多写的内容也少得多。差别，就在这一句话。",
 "B三要素": "这句话怎么写？记住三件事。第一，做什么，比如整理本周周报。第二，有什么材料，比如这个文件夹里的三份日报和数据表。第三，要什么结果，比如分四段，输出成 Word。三件事说全，它就不用猜。",
 "C现场写": "我们现场写一条。先写做什么：整理本周周报。材料如果不在工作空间里，点加号，添加文件，本地文件、资料库、腾讯文档都能选。能直接指给它的文件，就别自己复述。然后补上材料和结果：分四段，输出 Word。",
 "D增强": "不会写怎么办？先随便写一句大白话，比如：把这几个日报整理成周报。输入框里有字之后，右下角会出现一个星形按钮，这就是增强提示词。点一下，十来秒，它把大白话改写成了更完整的版本。不满意，点恢复原文，就回到原话。",
 "E两个限制": "最后，有两句话我建议你每次都加。第一句，只用材料里的内容，不要编。第二句，查不到的，写待确认。开头那份多写的周报，缺的就是这两句。",
 "F收尾": "今天三句话：说全三件事，大白话可以先增强，别忘了两个限制。下一集，讲三种模式：复杂任务，怎么让它先给方案再动手。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F3 = K.F; F1 = f"{V}/footage/ep01"

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n); a1 = at(n, "它也写出来了") - 0.3; a2 = at(n, "第二种") - 0.2
    P[n] = [("R", f"{F3}/A-模糊指令.mov", {"anchors": [[2.5, 0], [8.3, a1*0.75], [12.0, a1*0.85], [90.0, a1], [92.0, a2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "只说一句", "set": {"zoom": 1.8, "focus": True}}, {"contains": "发送", "set": {"label": None}}],
                "badges": [{"from": 12.0, "to": 88.0, "text": "加速播放", "t0": 0}],
                "events_extra": [
                    {"t": 90.2, "kind": "move", "target": [940,230,410,60], "label": "它自己定的标题和结构", "zoom": 1.4, "dur": 0.8},
                    {"t": 90.9, "kind": "move", "target": [940,742,410,24], "label": "材料里没有", "zoom": 2.0, "focus": True, "dur": 0.4},
                    {"t": 91.4, "kind": "move", "target": [940,604,410,22], "label": "材料里也没有", "zoom": 2.0, "focus": True, "dur": 0.5}]}),
            ("R", f"{F1}/H5-验收.mov", {"anchors": [[2.0, 0], [2.0 + t - a2, t - a2]], "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 2.3, "kind": "move", "target": [864,169,565,659], "label": "说清楚的版本：四段", "zoom": 1.3, "dur": t - a2 - 1.5}]})]
    n = "B三要素"; t = T(n); b2 = at(n, "第一") - 0.2
    P[n] = [("CARD", "b", t, [
        {"from": 0, "to": b2, "lines": [("一句需求，说全三件事", "b", 0.3)]},
        {"from": b2, "to": t, "last": True, "lines": [("① 做什么", "n", at(n,"第一")), ("整理本周周报", "s", at(n,"比如整理")),
            ("② 有什么材料", "n", at(n,"第二")), ("三份日报 + 一张数据表", "s", at(n,"比如这个")),
            ("③ 要什么结果", "n", at(n,"第三")), ("分四段，输出 Word", "s", at(n,"比如分四段"))]}])]
    n = "C现场写"; t = T(n); c2 = at(n, "材料如果") - 0.2; c3 = at(n, "然后补上") - 0.2
    P[n] = [("R", f"{F3}/CE-写需求.mov", {"anchors": [[2.6, 0], [5.1, at(n,"先写做什么")], [7.2, c2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "做什么", "set": {"zoom": 1.6, "label": "① 做什么"}}, {"contains": "点「+」", "set": {"label": None}}]}),
            ("R", f"{F3}/C2-添加文件.mov", {"anchors": [[2.4, 0], [4.2, at(n,"点加号")-c2+0.3], [5.4, at(n,"添加文件")-c2+0.2], [11.0, c3-c2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "点「+」", "set": {"zoom": 1.8}}, {"contains": "添加文件", "set": {"zoom": False}}],
                "events_extra": [{"t": 6.6, "kind": "move", "target": [662,262,200,180], "label": "本地文件、资料库、腾讯文档…", "zoom": 1.6, "focus": True, "dur": 2.8}]}),
            ("R", f"{F3}/CE-写需求.mov", {"anchors": [[14.5, 0], [22.3, t-c3]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "有什么材料", "set": {"zoom": 1.5, "label": "② 有什么材料"}}, {"contains": "要什么结果", "set": {"zoom": 1.5, "label": "③ 要什么结果"}},
                          {"contains": "两个限制", "set": {"label": None}}]})]
    n = "D增强"; t = T(n); d2 = at(n, "不满意") - 0.3
    P[n] = [("R", f"{F3}/D-增强提示词.mov", {"anchors": [[2.6, 0], [5.0, at(n,"比如")], [7.4, at(n,"输入框里有字")+0.3], [10.1, at(n,"点一下")+0.3], [23.5, at(n,"它把大白话")], [27.5, d2]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 10.3, "to": 23.0, "text": "等待约 10 秒", "t0": 0}],
                "patch": [{"contains": "大白话", "set": {"zoom": 1.6}}, {"contains": "增强提示词", "set": {"zoom": 2.6, "focus": True, "dur": 2.4}}],
                "events_extra": [{"t": 24.0, "kind": "move", "target": [452,362,790,56], "label": "改写成更完整的版本", "zoom": 1.5, "dur": 3.0}]}),
            ("R", f"{F3}/D2-恢复原文.mov", {"anchors": [[6.6, 0], [9.1, at(n,"恢复原文")-d2+0.3], [14.5, t-d2]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "改写成", "set": {"label": None}}, {"contains": "恢复原文", "set": {"zoom": 2.4, "focus": True}}, {"contains": "回到原话", "set": {"zoom": 1.6}}]})]
    n = "E两个限制"; t = T(n); e3 = at(n, "开头那份") - 0.2
    P[n] = [("R", f"{F3}/CE-写需求.mov", {"anchors": [[21.5, 0], [22.4, at(n,"第一句")], [29.0, e3]], "cam_fixed": [440,340,820,120], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "events_override": [{"t": 22.4, "kind": "move", "target": [452,362,790,60], "label": None, "dur": 0.1}]}),
            ("CARD", "e", t - e3, [{"from": 0, "to": t - e3, "last": True, "lines": [("每次都加这两句", "t", 0.15),
                ("只用材料里的内容，不要编", "b", 0.3), ("查不到的，写待确认", "b", 0.7)]}])]
    n = "F收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "f", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 说全三件事", "n", at(n,"说全")), ("② 大白话可以先增强", "n", at(n,"大白话")), ("③ 别忘了两个限制", "n", at(n,"别忘了"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("三种模式", "b", at(n,"讲三种")), ("复杂任务，先给方案再动手", "s", at(n,"复杂任务"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep03-v1.mp4")
