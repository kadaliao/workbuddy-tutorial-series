#!/usr/bin/env python3
"""第 12 集：个性化、记忆与模型。用法：ep12.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 12, "个性化、记忆与模型"
TEXT = {
 "A开场": "用了一阵子，你会发现有些话每次都要重复说。今天讲三件事，让它越用越懂你。",
 "B设置": "左下角头像，设置。左边功能分组里，先看个性化。",
 "C自定义指令": "自定义指令，就是你希望它每次都遵守的规则，写一次，以后所有任务都生效。比如：回答先给结论；数字保留一位小数；不确定的写待确认。最多一千五百字，但越短越好，只写真正每次都需要的。下面还能设置它怎么称呼你。",
 "D记忆": "第二件，记忆。打开生成对话记忆，它会从对话里记住你的偏好和习惯。记忆只有你自己能看，每晚自动整理，可以随时查看、编辑，也能一键关掉。不想让它记，就关着。",
 "E模型": "第三件，模型。在输入框右下角，这里写着快速。点开，有三档：快速、均衡、极致，旁边是消耗倍率，越往下越强，也越费积分。下面还能直接选具体的模型。最上面是 Max 模式，消耗明显更快，平时不用开。倍率和限免活动经常变，以你当天看到的为准。",
 "F怎么选": "怎么选？日常整理、改写、汇总，快速就够。长文档、复杂分析、出错代价大的，换均衡或极致。先用快速跑，不满意再升档，比一开始就用最贵的划算。",
 "G收尾": "今天三句话：常说的话写进自定义指令，记忆可以看也可以关，简单活用快速、难活再升档。番外篇，我们看看积分到底是怎么花掉的。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F12 = K.F
MENU = [{"name":"菜单昵称","rect":[22,240,130,38],"t":[[4,8]],"style":"fillmed"},{"name":"菜单积分","rect":[222,350,100,30],"t":[[4,8]],"style":"fillmed"}]

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("CARD", "a", t, [{"from": 0, "to": t, "last": True, "lines": [("让它越用越懂你", "b", 0.3),
        ("自定义指令 · 记忆 · 模型", "s", at(n,"今天讲"))]}])]
    n = "B设置"; t = T(n)
    P[n] = [("R", f"{F12}/BC-个性化.mov", {"anchors": [[2.4, 0], [4.3, at(n,"左下角")+0.6], [7.0, at(n,"设置")+0.3], [10.9, at(n,"先看个性化")+0.4], [12.0, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()] + MENU,
                "patch": [{"contains": "头像", "set": {"zoom": 1.8}}, {"contains": "设置", "set": {"zoom": 1.6}}, {"contains": "个性化", "set": {"zoom": 1.8}}]})]
    n = "C自定义指令"; t = T(n)
    P[n] = [("R", f"{F12}/BC-个性化.mov", {"anchors": [[12.0, 0], [12.6, at(n,"自定义指令")+0.3], [17.1, at(n,"比如")], [22.0, at(n,"最多")], [23.9, at(n,"下面还能")], [27.4, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "每次都生效", "set": {"zoom": 1.6, "focus": True}}, {"contains": "写下", "set": {"zoom": 1.6}},
                          {"contains": "1500", "set": {"zoom": 2.2}}, {"contains": "称呼与身份", "set": {"zoom": 1.5}}]})]
    n = "D记忆"; t = T(n)
    P[n] = [("R", f"{F12}/D-记忆.mov", {"anchors": [[5.0, 0], [7.2, at(n,"第二件")+0.6], [8.9, at(n,"打开生成")], [12.2, at(n,"记忆只有")], [15.1, at(n,"每晚")], [18.5, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "记忆与进化", "set": {"zoom": 1.8}}, {"contains": "开关", "set": {"zoom": 1.6, "focus": True}},
                          {"contains": "本人可见", "set": {"zoom": 1.8, "focus": True}}, {"contains": "每晚", "set": {"zoom": 1.8, "focus": True}}]})]
    n = "E模型"; t = T(n)
    P[n] = [("R", f"{F12}/E-模型.mov", {"anchors": [[2.2, 0], [2.7, at(n,"在输入框")], [4.1, at(n,"点开")+0.3], [5.6, at(n,"有三档")], [9.1, at(n,"旁边是")], [12.0, at(n,"下面还能")], [15.0, at(n,"最上面")], [18.5, at(n,"倍率和限免")], [20.1, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "模型在这里", "set": {"zoom": 2.0}}, {"contains": "快速 /", "set": {"zoom": 2.0, "focus": True}}, {"contains": "倍率", "set": {"zoom": 2.0, "focus": True}},
                          {"contains": "直接选", "set": {"zoom": 1.8, "focus": True}}, {"contains": "Max", "set": {"zoom": 2.0, "focus": True}}],
                "events_extra": [{"t": 18.6, "kind": "move", "target": [826,90,310,350], "label": "倍率以当天为准", "zoom": 1.4, "dur": 1.0}]})]
    n = "F怎么选"; t = T(n)
    P[n] = [("CARD", "f", t, [{"from": 0, "to": t, "last": True, "lines": [("怎么选档位", "t", 0.2),
        ("日常整理、改写、汇总 → 快速", "n", at(n,"日常整理")), ("长文档、复杂分析 → 均衡 / 极致", "n", at(n,"长文档")), ("先用快速，不满意再升档", "b", at(n,"先用快速"))]}])]
    n = "G收尾"; t = T(n); nx = at(n, "番外篇") - 0.15
    P[n] = [("CARD", "g", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 常说的话写进自定义指令", "n", at(n,"常说的话")), ("② 记忆可以看，也可以关", "n", at(n,"记忆可以")), ("③ 简单活用快速，难活再升档", "n", at(n,"简单活"))]},
        {"from": nx, "to": t, "last": True, "lines": [("番外", "t", nx+0.1), ("积分到底是怎么花掉的", "b", at(n,"积分到底"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep12-v1.mp4")
