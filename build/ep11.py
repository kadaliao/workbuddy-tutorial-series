#!/usr/bin/env python3
"""第 11 集：连接器。用法：ep11.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 11, "连接器：邮箱、文档、会议一键连"
TEXT = {
 "A开场": "它不只能读你电脑里的文件。接上连接器，你的在线文档、邮箱、会议，它也能用。今天讲连接器。",
 "B页面": "左边，专家、技能、连接器，选连接器。这里列着能接的服务：腾讯文档、QQ 邮箱、腾讯会议、企业微信、飞书、钉钉，还有更多。右上角还能自定义。",
 "C输入框": "在对话里也能开：点加号，连接器，这次要用哪个，就点哪个后面的连接。",
 "D授权": "第一次用，要先授权。点卡片右上角的加号，它会先告诉你要拿什么权限：读取文档内容，编辑和管理文件。看清楚再点前往授权，然后扫码同意。我的建议：只授权你这次真要用的那一个，别一口气全连上。",
 "E写": "写入要更小心。我让它在腾讯文档里新建一个测试文档，写一段虚构的会议纪要，还特意说了：先把草稿发给我看，确认后再创建，只操作这一个文档。它先把草稿列出来，等我回复确认，才真的去创建，最后告诉我只建了这一个文档。邮件也一样，先出草稿，你看过再发，发出去就收不回来。",
 "F读": "读就简单了。新开一个任务，让它读这份文档，三句话总结。不到一分钟，决议、负责人、下次开会时间都出来了，还说明了只读了这一个文档，没做修改。",
 "G断开": "已连接的卡片上有个绿点。不用了，点开卡片，这里有解绑。",
 "H收尾": "今天三句话：要用哪个连哪个，写入先出草稿，用完记得解绑。下一集，个性化、记忆和模型，越用越顺手。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F11 = K.F
BLUR = lambda t: {"name": "过程区路径", "rect": [470,60,770,640], "t": t, "style": "blur"}

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("R", f"{F11}/B-连接器页.mov", {"anchors": [[9.0, 0], [9.0 + t, t]], "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 9.2, "kind": "move", "target": [290,80,1130,330], "label": "在线文档、邮箱、会议", "zoom": 1.2, "dur": t - 1.0}]})]
    n = "B页面"; t = T(n)
    P[n] = [("R", f"{F11}/B-连接器页.mov", {"anchors": [[2.4, 0], [4.2, at(n,"左边")+0.6], [7.3, at(n,"选连接器")+0.4], [9.4, at(n,"这里列着")], [14.0, at(n,"腾讯文档")], [17.7, at(n,"QQ")], [20.8, at(n,"腾讯会议")], [30.1, at(n,"右上角")], [33.5, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO([[0, 3]])],
                "patch": [{"contains": "专家·技能", "set": {"zoom": 1.6}}, {"contains": "连接器", "set": {"zoom": 1.8}}, {"contains": "能接的", "set": {"zoom": 1.2}},
                          {"contains": "腾讯文档", "set": {"zoom": 1.8}}, {"contains": "QQ", "set": {"zoom": 1.8}}, {"contains": "腾讯会议", "set": {"zoom": 1.8}}, {"contains": "自定义", "set": {"zoom": 2.0}}]})]
    n = "C输入框"; t = T(n)
    P[n] = [("R", f"{F11}/C-输入框里开.mov", {"anchors": [[2.4, 0], [4.1, at(n,"点加号")+0.4], [5.7, at(n,"连接器")], [8.3, at(n,"这次要用")], [12.5, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "点「+」", "set": {"zoom": 1.8}}, {"contains": "连接器", "set": {"zoom": 1.6}}, {"contains": "点连接", "set": {"zoom": 1.6, "focus": True}}]})]
    n = "D授权"; t = T(n); d2 = at(n, "看清楚") - 0.2
    P[n] = [("R", f"{F11}/D-点授权.mov", {"anchors": [[1.6, 0], [4.2, at(n,"点卡片")+0.8], [6.0, at(n,"它会先告诉")], [9.0, d2]], "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "授权", "set": {"zoom": 2.2, "focus": True}}],
                "events_extra": [{"t": 6.1, "kind": "move", "target": [490,368,380,124], "label": "读取 · 编辑和管理", "zoom": 1.8, "focus": True, "dur": 2.6}]}),
            ("CARD", "d", t - d2, [{"from": 0, "to": t - d2, "last": True, "lines": [("看清权限，再前往授权、扫码同意", "n", 0.2),
                ("只授权这次真要用的那一个", "b", at(n,"我的建议")-d2)]}])]
    n = "E写"; t = T(n); e2 = at(n, "它先把草稿") - 0.3
    P[n] = [("R", f"{F11}/E1-草稿.mov", {"anchors": [[3.5, 0], [5.0, at(n,"我让它")], [23.8, e2-1.6], [26.0, e2-1.0], [57.0, e2-0.3], [59.3, e2]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 26.0, "to": 56.0, "text": "加速播放", "t0": 0}],
                "patch": [{"contains": "先出草稿", "set": {"zoom": 1.5}}]}),
            ("R", f"{F11}/E1-草稿.mov", {"anchors": seg_anchor([[59.3, e2], [60.4, at(n,"等我回复")]], e2), "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 59.4, "kind": "move", "target": [470,580,760,60], "label": "确认后才创建", "zoom": 1.6, "focus": True, "dur": 1.0}]}),
            ("R", f"{F11}/E2-确认创建.mov", {"anchors": seg_anchor([[3.6, at(n,"等我回复")], [7.8, at(n,"才真的")], [10.0, at(n,"才真的")+0.6], [195.0, at(n,"最后告诉我")-0.5], [205.0, at(n,"最后告诉我")-0.4], [256.0, at(n,"邮件也一样")], [256.8, t]], at(n,"等我回复")),
                "drop_masks": DROP, "masks_extra": [USER, BLUR([[9.0, 197.0]]),
                    {"name":"文档链接","rect":[935,60,470,34],"t":[[197,257]],"style":"fillmed"}, {"name":"链接与ID","rect":[296,176,420,52],"t":[[204,257]],"style":"fillmed"}],
                "badges": [{"from": 10.0, "to": 195.0, "text": "加速播放 · 实际 {real}", "t0": 7.8}],
                "patch": [{"contains": "再确认", "set": {"zoom": 1.6}}],
                "events_extra": [{"t": 205.5, "kind": "move", "target": [300,460,520,60], "label": "只建了这一个文档", "zoom": 1.6, "focus": True, "dur": 6.0}]}),
           ]
    n = "F读"; t = T(n)
    P[n] = [("R", f"{F11}/F-读取总结.mov", {"anchors": [[3.5, 0], [5.0, at(n,"让它读")], [20.1, at(n,"不到一分钟")-0.4], [22.0, at(n,"不到一分钟")], [121.0, at(n,"决议")], [124.4, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO(), BLUR([[21.0, 119.0]])],
                "badges": [{"from": 22.0, "to": 120.0, "text": "加速播放 · 实际 {real}", "t0": 20.1}],
                "patch": [{"contains": "在线文档", "set": {"zoom": 1.5}}],
                "events_extra": [{"t": 121.2, "kind": "move", "target": [470,300,760,230], "label": "决议 · 负责人 · 下次开会", "zoom": 1.3, "dur": 1.6},
                                 {"t": 123.2, "kind": "move", "target": [470,522,500,28], "label": "只读，没改", "zoom": 1.8, "focus": True, "dur": 0.8}]})]
    n = "G断开"; t = T(n)
    P[n] = [("R", f"{F11}/G-解绑位置.mov", {"anchors": [[1.6, 0], [2.2, at(n,"已连接")], [6.1, at(n,"点开卡片")+0.4], [8.8, at(n,"这里有解绑")], [12.8, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "绿点", "set": {"zoom": 2.0, "focus": True}}, {"contains": "解绑", "set": {"zoom": 2.2, "focus": True}}]})]
    n = "H收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "h", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 要用哪个连哪个", "n", at(n,"要用哪个")), ("② 写入先出草稿", "n", at(n,"写入先")), ("③ 用完记得解绑", "n", at(n,"用完"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("个性化、记忆和模型", "b", at(n,"个性化"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep11-v1.mp4")
