#!/usr/bin/env python3
"""第 5 集：验收三步。用法：ep05.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 5, "验收三步：它做对了吗"
TEXT = {
 "A开场": "这次我故意没加那两句限制，还在数据表里埋了个坑：客户投诉数，本周这一格是空的。它很快交了一份周报，看着很像样。但你敢直接发给领导吗？今天讲用它之后最重要的习惯：验收。",
 "B对数字": "第一步，对数字。原始数据是这张表，投诉数本周这一格是空的。再看周报：前三项都对得上。投诉数，它没有自己补一个数，写的是未填报。这一步它做得好。",
 "C对来源": "第二步，对来源。每一句话，都去材料里找原话。周三日报写的是，处理客户投诉两起，它写成了均在当周完成响应。周一日报写的是，修复官网表单提交问题，它又加了一句，恢复线上线索正常收集。还有，日报只说场地报价偏高、需要再比价，它写成了已完成多家比价。找不到原话的，就是它自己加工的。",
 "D对多余": "第三步，对遗漏，也对多出来的。四段是齐的，但下周计划多了两条：规范数据填报、跟进供应商交付，材料里都没有。别只看缺了什么，也要看多了什么。",
 "E修正": "发现问题怎么办？别重写，也别只说再改改。直接点名位置：哪一段、哪句话、为什么不对。我把这几处一次说清，发送。一分多钟后，它把我点名的地方都改了，还把改动列了出来。",
 "F再看": "但改完，还要再看一遍。它自己也说了：还有几处措辞是它组织的，我没点名，它就留着。下周计划还多出一个空行。所以验收不是一次，是改完再看一次。",
 "G收尾": "今天三句话：对数字，对来源，对多出来的。发现问题，点名位置。改完再看一遍。下一集，把做顺的活存成技能，下次一句话搞定。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F5 = K.F

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("R", f"{F5}/A-陷阱版周报.mov", {"anchors": [[3.2, 0], [5.0, 0.8], [18.5, at(n,"它很快")-0.4], [21.0, at(n,"它很快")+0.4], [122.0, at(n,"看着很像样")], [126.8, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 21.0, "to": 120.0, "text": "加速播放 · 实际 {real}", "t0": 18.5}],
                "patch": [{"contains": "不加两个限制", "set": {"zoom": 1.5, "label": "这次不加两个限制"}}],
                "events_extra": [{"t": 123.0, "kind": "move", "target": [855,170,585,690], "label": "看着很像样", "zoom": 1.2, "dur": 3.0}]})]
    n = "B对数字"; t = T(n); b2 = at(n, "再看周报") - 0.2
    P[n] = [("CARD", "csv", b2, [{"from": 0, "to": b2, "last": True, "lines": [("周数据.csv（原始数据）", "t", 0.15),
                ("新增客户数，48，41", "s", 0.3), ("成交订单数，23，19", "s", 0.45), ("销售额(万元)，86.5，72.0", "s", 0.6),
                ("客户投诉数，（空），5", "r", at(n,"投诉数")-0.1)]}]),
            ("R", f"{F5}/B-验收.mov", {"anchors": [[2.5, 0], [9.6, at(n,"前三项")-b2], [13.8, t-b2]], "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "① 数字", "set": {"zoom": 1.8, "focus": True}}]})]
    n = "C对来源"; t = T(n)
    P[n] = [("R", f"{F5}/B-验收.mov", {"anchors": [[13.8, 0], [14.3, at(n,"周三日报")-0.2], [18.8, at(n,"周一日报")-0.2], [27.4, at(n,"还有")], [31.0, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "日报里没这句", "set": {"zoom": 2.0, "focus": True, "label": "日报原话：处理客户投诉 2 起"}},
                          {"contains": "日报里也没这句", "set": {"zoom": 2.0, "focus": True, "label": "日报原话：修复官网表单提交问题"}},
                          {"contains": "需要再比价", "set": {"zoom": 2.0, "focus": True}}]})]
    n = "D对多余"; t = T(n)
    P[n] = [("R", f"{F5}/B-验收.mov", {"anchors": [[31.0, 0], [31.9, at(n,"但下周计划")], [39.2, at(n,"跟进供应商")-0.3], [44.8, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "③ 计划", "set": {"zoom": 1.8, "focus": True}}, {"contains": "材料里也没有", "set": {"zoom": 1.8, "focus": True}}]})]
    n = "E修正"; t = T(n)
    P[n] = [("R", f"{F5}/E-指出问题.mov", {"anchors": [[3.5, 0], [4.5, at(n,"直接点名")-0.3], [22.8, at(n,"发送")+0.3], [25.0, at(n,"一分多钟")], [133.0, at(n,"都改了")], [138.4, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "badges": [{"from": 25.0, "to": 132.0, "text": "加速播放 · 实际 {real}", "t0": 22.8}],
                "patch": [{"contains": "指出具体位置", "set": {"zoom": 1.5, "label": "点名：哪段、哪句、为什么"}}],
                "events_extra": [{"t": 134.0, "kind": "move", "target": [300,52,516,208], "label": "列出了改动", "zoom": 1.4, "dur": 3.5}]})]
    n = "F再看"; t = T(n)
    P[n] = [("R", f"{F5}/F-再看一遍.mov", {"anchors": [[1.5, 0], [6.7, at(n,"它自己也说")], [10.9, at(n,"下周计划还")], [16.1, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "点名的几处", "set": {"label": None, "zoom": False}},
                          {"contains": "没点名的", "set": {"zoom": 1.6, "focus": True}}, {"contains": "空行", "set": {"zoom": 2.0, "focus": True}}]})]
    n = "G收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "g", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 对数字、对来源、对多出来的", "n", at(n,"对数字")), ("② 发现问题，点名位置", "n", at(n,"发现问题")), ("③ 改完再看一遍", "n", at(n,"改完再看"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("把做顺的活存成技能", "b", at(n,"把做顺")), ("下次一句话搞定", "s", at(n,"下次一句话"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep05-v1.mp4")
