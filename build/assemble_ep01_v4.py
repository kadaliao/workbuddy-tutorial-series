#!/usr/bin/env python3
"""第1集 v4 编排：画面按旁白逐字时间轴对齐；字幕放在画面下方独立字幕条；输出 video/ep01-v4.mp4。"""
import json, os, re, subprocess, sys, hashlib
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
V = "/Volumes/Data-External/workspace/cc-test/wbd/video"; B = os.environ.get("EP_BUILD", f"{V}/build/ep01v4"); F = f"{V}/footage/ep01"; A = os.environ.get("EP_AUDIO", f"{V}/audio/ep01v4")
PY = f"{V}/build/venv/bin/python"; ANN = f"{V}/build/annotate4.py"; os.makedirs(B, exist_ok=True)
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"; ACC = (255, 176, 32); BG = (20, 24, 31)
LEAD = 0.3   # 旁白在每段内延后 0.3s 开始
TAIL = 0.6

TEXT = {
 "A开场": "这是一份周报。三份日报、一张数据表，两分钟，它自己读完、自己对数、自己排好版。今天这集，我带你从零装好 WorkBuddy，跑通这第一个任务。",
 "B为什么": "每周五下午，翻聊天记录、对数据、调格式，一份周报动辄一两个小时。真正需要你动脑的，其实只有，这周哪件事最重要。剩下的整理活，交给它。",
 "C装好": "打开官网，下载按钮点一下。Mac 用户注意，M 系列芯片选苹果芯片版，老的 Intel 机器选另一个。下载好之后，双击安装包，把图标拖进应用程序文件夹。Windows 就是双击安装包，跟着向导走。第一次打开会有一分钟左右的，环境准备中，别急，它在配运行环境。然后点登录，扫码就行。现在这一版没有游客模式，必须先登录。",
 "D界面": "进来之后，左边是侧边栏，先认七个入口。第一个，新建任务，我们天天用它。第二个，助理，以后可以用手机遥控电脑。第三个，项目，团队协作用。第四个，专家、技能、连接器，是它的工具箱。第五个，定时任务，让它定点自己干活。第六个，资料库，放成品和资料。最后，更多。今天只用第一个，其他的后面几集慢慢讲。",
 "E选文件夹": "我提前建了一个文件夹，里面只放了三份日报和一张数据表，内容都是我自己编的。点输入框下面的，选择工作空间，选，打开本地文件夹，选中这个文件夹。这一步的意思是：它只能在这个文件夹里读和写，别的地方它碰不到。",
 "F写需求": "然后写需求。我只说三件事：做什么、有什么材料、要什么结果。比如：读取这个文件夹里的三份日报和数据表，写一份周报，分成本周完成、数据表现、问题与需求、下周计划四段，只用材料里的内容，不要编，输出成 Word，存在当前文件夹。",
 "G执行": "发送。你会看到它先读文件，再整理，最后生成文档。我这次大概一分钟出文件，一分半左右全部做完。右边可以直接预览成品。",
 "H验收": "先别急着夸它。看三样：数字对不对，有没有写材料里没有的事，四段是不是齐的。数字我逐个对过，全对，四段也齐。但你看问题这一条，它写了，通过比价确定场地，材料里只说场地定了，没说比价。这种小加工，就是你要动手改掉的地方。",
 "K找文件": "成品就在你选的这个文件夹里，右上角更多里可以直接打开文件夹，复制出去发给领导就行。",
 "I坑": "有三个坑。第一，它读不到你没授权的地方，所以材料一定要放进你选的文件夹。第二，别急着把重要文件直接丢进去，先放一份副本。第三，这一集我没有打开，允许完全访问，新手建议一直别开，第二集我专门讲。",
 "J收尾": "今天三句话。第一，先装好登录，认清左边七个入口。第二，让它在一个文件夹里干活。第三，需求说清，做什么、有什么材料、要什么结果。下一集，我们把门锁好：它到底能碰什么，怎么让它别乱来。",
}
ORDER = ["A开场","B为什么","C装好","D界面","E选文件夹","F写需求","G执行","H验收","K找文件","I坑","J收尾"]

def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
AD = {n: dur(f"{A}/{n}.wav") for n in ORDER}
EXTRA = {"G执行": 1.8}   # 旁白结束后多留画面
T = {n: round(AD[n] + LEAD + TAIL + EXTRA.get(n, 0), 3) for n in ORDER}
PUN = set("，。、：；！？,.:;!? “”「」")

# ---------- 旁白逐字时间（whisper 词级时间 → 按字数比例映射到台本）----------
def char_times(n):
    d = json.load(open(f"{B}/wj/{n}.json")); ts = []
    for s in d["segments"]:
        for w in s["words"]:
            cs = [c for c in w["word"] if c not in PUN and not c.isspace()]
            for i, _ in enumerate(cs): ts.append(w["start"] + (w["end"]-w["start"])*i/max(len(cs),1))
    return ts
def script_chars(n): return [c for c in TEXT[n] if c not in PUN and not c.isspace()]
def at(n, phrase, k=0):
    """台本中第 k 次出现 phrase 的首字 → 段内输出时间（含 LEAD）"""
    txt = "".join(script_chars(n)); pos = -1
    for _ in range(k+1): pos = txt.index(phrase, pos+1)
    ts = char_times(n); j = min(len(ts)-1, round(pos*len(ts)/len(txt)))
    return round(ts[j] + LEAD, 3)

# ---------- 文字卡片 ----------
CARD_BG = None
def card_bg():
    global CARD_BG
    if CARD_BG is None:
        im = Image.new("RGB", (1920,1080), BG); d = ImageDraw.Draw(im)
        for y in range(970): c = int(10*y/970); d.line((0,y,1920,y), fill=(BG[0]+c, BG[1]+c, BG[2]+c))
        d.rectangle((0,0,14,970), fill=ACC); CARD_BG = im
    return CARD_BG
STY = {"t": (54, (165,173,186)), "n": (70, (240,243,247)), "b": (86, ACC), "s": (46, (200,206,214))}
def card(name, secs, groups):
    """groups: [{"from":a,"to":b,"lines":[(text, style, t_appear)]}]，时间为段内输出时间"""
    out = f"{B}/card_{name}.mp4"
    key = hashlib.md5(json.dumps([secs, groups], ensure_ascii=False).encode()).hexdigest()[:8]; out = out[:-4] + f"_{key}.mp4"
    if os.path.exists(out): return out
    wr = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r","30","-i","-",
                           "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE)
    fonts = {k: ImageFont.truetype(FONT, v[0]) for k, v in STY.items()}
    for i in range(int(round(secs*30))):
        t = i/30; im = card_bg().copy()
        for g in groups:
            if not (g["from"] <= t < g["to"]): continue
            q = 1.0 if g["to"] - t > 0.3 or g.get("last") else max(0, (g["to"]-t)/0.3)
            hs = [STY[s][0]*1.55 for _, s, _ in g["lines"]]; y = (970 - sum(hs))/2
            lay = Image.new("RGBA", (1920,1080), (0,0,0,0)); d = ImageDraw.Draw(lay)
            for (txt, s, ta), h in zip(g["lines"], hs):
                p = min(1, max(0, (t-ta)/0.45)); p = p*p*(3-2*p)
                if p > 0:
                    f = fonts[s]; w = d.textlength(txt, font=f)
                    d.text(((1920-w)/2, y + (h-STY[s][0])/2 + (1-p)*26), txt, font=f, fill=STY[s][1]+(int(255*p*q),))
                y += h
            im.paste(lay, (0,0), lay)
        wr.stdin.write(im.tobytes())
    wr.stdin.close(); wr.wait(); return out

def render(src, cfg):
    key = hashlib.md5((src + json.dumps(cfg, sort_keys=True, ensure_ascii=False) + hashlib.md5(open(ANN,"rb").read()).hexdigest()).encode()).hexdigest()[:8]
    out = f"{B}/r_{os.path.basename(src).rsplit('.',1)[0]}_{key}.mp4"
    if os.path.exists(out): return out
    cp = out[:-4] + ".cfg.json"; json.dump(cfg, open(cp,"w"), ensure_ascii=False)
    subprocess.run([PY, ANN, src, out, "--cfg", cp], check=True); return out

def seg_anchor(pairs, seg_from, seg_to):
    """pairs 中 out 是段内时间；转换成片段内时间（减 seg_from），并截到片段长度"""
    return [[s, round(o - seg_from, 3)] for s, o in pairs]

USER = {"name": "用户行", "rect": [8,795,180,55], "style": "fillmed"}
PROMO = lambda t=None: dict({"name": "推广", "rect": [1262,6,172,42], "style": "fillmed"}, **({"t": t} if t else {}))
DROP = ["推广", "用户行"]

# ---------- 分段画面 ----------
def plan():
    P = {}
    # A 开场：成品预览，推近表格
    n = "A开场"; t = T[n]
    P[n] = [("R", f"{F}/H5-验收.mov", {"anchors": [[2.0, 0], [2.0 + t, t]], "drop_masks": DROP, "masks_extra": [USER],
        "events_override": [
            {"t": 2.3, "kind": "move", "target": [864,169,565,659], "label": "它写好的周报", "zoom": 1.3, "dur": 2.6},
            {"t": 2.0 + at(n,"自己读完") - 0.2, "kind": "move", "target": [947,477,384,100], "label": "数据它自己对好", "zoom": 2.0, "focus": True, "dur": 3.2}]})]
    # B 为什么：卡片，逐行跟旁白
    n = "B为什么"; t = T[n]; c2 = at(n,"一份周报") - 0.2; c3 = at(n,"其实只有") - 0.1
    P[n] = [("CARD", "b", t, [
        {"from": 0, "to": c2, "lines": [("每周五下午", "t", at(n,"每周五")), ("翻聊天记录 · 对数据 · 调格式", "b", at(n,"翻聊天"))]},
        {"from": c2, "to": c3, "lines": [("一份周报，动辄一两个小时", "n", c2+0.1), ("真正要动脑的，只有一件事", "b", at(n,"真正需要"))]},
        {"from": c3, "to": t, "last": True, "lines": [("这周哪件事最重要？", "n", c3+0.1), ("其余的整理活，交给它", "b", at(n,"剩下的"))]}])]
    # C 装好：官网 → 拖拽安装 → Windows 卡片 → 登录页
    n = "C装好"; t = T[n]; c1 = at(n,"下载好之后") - 0.1; c2 = at(n,"Windows") - 0.1; c3 = at(n,"第一次打开") - 0.15
    P[n] = [("R", f"{F}/B-官网首页.png", {"anchors": [[0, 0], [c1, c1]], "events_override": [
                {"t": 0.6, "kind": "move", "target": [1700,690,440,120], "label": "点「立即下载」", "zoom": 1.6, "dur": 2.6},
                {"t": at(n,"Mac"), "kind": "move", "target": [1700,690,440,120], "label": "Mac：M 系列选 Apple 芯片版", "zoom": 1.6, "dur": at(n,"下载好")-at(n,"Mac")-1.1}]}),
            ("R", f"{F}/C-安装.mov", {"anchors": [[1.6, 0], [6.55, c2-c1]], "cam_fixed": [300,120,624,400], "drop_masks": DROP,
                "events_override": [
                {"t": 2.6, "kind": "move", "target": [409,265,86,108], "label": "双击安装包，拖图标", "dur": 1.6, "side": "bottom"},
                {"t": 4.6, "kind": "move", "target": [729,265,86,108], "label": "拖进「应用程序」", "dur": 2.0, "side": "bottom"}]}),
            ("CARD", "c_win", c3-c2, [{"from": 0, "to": c3-c2, "lines": [("Windows", "t", 0.15), ("双击安装包，跟着向导走", "b", 0.4)]}]),
            ("R", f"{V}/shots/01-启动登录页.png", {"anchors": [[0, 0], [t-c3, t-c3]], "events_override": [
                {"t": 0.3, "kind": "move", "target": [900,420,600,500], "label": "首次启动约 1 分钟「环境准备中」", "dur": at(n,"然后点登录")-c3-1.4},
                {"t": at(n,"然后点登录")-c3, "kind": "click", "x": 1200, "y": 1022, "target": [1020,984,360,76], "label": "点登录，用微信扫码", "zoom": False, "dur": at(n,"现在这一版")-at(n,"然后点登录")-0.9},
                {"t": at(n,"现在这一版")-c3, "kind": "move", "target": [1020,984,360,76], "label": "没有游客模式，必须先登录", "zoom": False, "dur": 2.4}]})]
    # D 认识界面：每个入口的点击对齐到旁白念到它的时刻
    n = "D界面"; t = T[n]
    clicks = [(5.0,"助理"), (8.5,"项目"), (12.0,"专家"), (17.2,"定时任务"), (20.7,"资料库"), (24.2,"最后"), (27.8,"今天只用")]
    anc = [[0.8, 0], [2.6, at(n,"第一个")-0.4]] + [[s, at(n, w)-0.25] for s, w in clicks] + [[34.3, t]]
    P[n] = [("R", f"{F}/D-侧栏巡览.mov", {"anchors": anc, "drop_masks": ["推广", "用户行"],
        "masks_extra": [USER, PROMO([[0, 5.3], [28.0, 34.4]]), {"name": "活动气泡", "rect": [1004,150,238,150], "t": [[27.5, 34.4]], "style": "fill", "color": [255,255,255]}],
        "events_extra": [{"t": 1.0, "kind": "move", "target": [12,108,245,230], "label": "左边 7 个入口", "dur": 1.4},
                         {"t": 2.7, "kind": "move", "target": [12,108,245,34], "label": "新建任务：每天都用", "dur": 1.6}],
        "drop_events_t": [[30.0, 30.7]], "drop_labels": ["专家、技能、连接器"],
        "mask_times": {"所有者": [[20.5, 28.4]]},
        # 镜头：先推近看清 7 个入口 → 逐个讲时框住侧栏 + 左侧内容 → 讲完拉回全景
        "cam_keys": [[0.8, 0,0,1440,860], [1.0, 0,0,1440,860], [2.0, 0,40,560,335], [3.3, 0,40,560,335],
                     [4.4, 0,0,920,550], [27.9, 0,0,920,550], [29.4, 0,0,1440,860], [34.3, 0,0,1440,860]],
        "patch": [{"contains": "新建任务：天天用它", "set": {"label": "今天只用这一个"}},
                  {"contains": "工具箱", "set": {"dx": 190}}]})]
    # E 选文件夹：先看素材文件夹（对话框内容），再完整操作一遍
    n = "E选文件夹"; t = T[n]; e1 = at(n,"点输入框") - 0.4
    emask = {"name": "对话框侧栏", "rect": [288,213,136,436], "t": [[7.4, 14.3]], "style": "fillmed"}
    P[n] = [("R", f"{F}/E5-选工作空间.mov", {"anchors": [[10.9, 0], [11.6, e1]], "drop_masks": ["推广","用户行","对话框"], "masks_extra": [USER, PROMO(), emask],
                "events_override": [{"t": 11.0, "kind": "move", "target": [440,290,430,100], "label": "只放 3 份日报 + 1 张数据表", "zoom": 1.6, "focus": True, "dur": 0.4}]}),
            ("R", f"{F}/E5-选工作空间.mov", {"anchors": seg_anchor([[2.4, e1], [4.2, at(n,"选择工作空间")-0.15], [7.1, at(n,"打开本地")-0.1], [14.0, at(n,"选中这个")+0.6], [16.1, at(n,"这一步")+0.5], [20.0, t]], e1, t),
                "drop_masks": ["推广","用户行","对话框"], "masks_extra": [USER, PROMO(), emask], "drop_labels": ["只放"],
                "patch": [{"contains": "点这里选择", "set": {"zoom": 1.8}}, {"contains": "打开本地", "set": {"zoom": 1.8}}, {"contains": "点「打开」", "set": {"zoom": 1.6}},
                          {"contains": "选好了", "set": {"zoom": 1.8, "focus": True, "label": "工作空间：它只能在这里读写", "dur": 3.0}}]})]
    # F 写需求
    n = "F写需求"; t = T[n]
    P[n] = [("R", f"{F}/F5-写需求.mov", {"anchors": [[1.5, 0], [4.3, at(n,"三件事")], [5.2, at(n,"读取")-0.25], [25.6, t]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
        "events_extra": [{"t": 3.0, "kind": "move", "target": [454,358,795,143], "label": "做什么 + 有什么材料 + 要什么结果", "dur": 1.0}],
        "patch": [{"contains": "写清", "set": {"label": None, "zoom": 1.45}}]})]
    # G 执行：真实 1 分 23 秒，等待部分加速，角标显示真实计时
    n = "G执行"; t = T[n]
    P[n] = [("R", f"{F}/G5-执行.mov", {"anchors": [[2.6, 0], [4.7, at(n,"发送")+0.35], [6.0, at(n,"你会看到")], [80.5, at(n,"右边")-0.6], [88.0, t-2.4], [91.0, t]],
        "events_shift": -81.3, "drop_masks": DROP, "masks_extra": [USER, PROMO([[0, 5.5]])],
        "badges": [{"from": 6.0, "to": 80.5, "text": "加速播放 · 实际 {real}", "t0": 5.0}],
        "events_extra": [{"t": 82.0, "kind": "move", "target": [855,0,585,860], "label": "右边直接预览成品", "dur": 2.2},
                         {"t": 88.7, "kind": "move", "target": [296,159,124,26], "label": "实际用时 1 分 23 秒", "zoom": 1.9, "dur": 1.6}],
        "patch": [{"contains": "点发送", "set": {"zoom": 1.8}}]})]
    # H 验收：三样检查清单 + 指出“比价”
    n = "H验收"; t = T[n]
    good = (120, 220, 140); warn = (255, 176, 32)
    P[n] = [("R", f"{F}/H5-验收.mov", {"anchors": [[1.5, 0], [3.0, 1.0], [5.4, at(n,"数字我")+0.0], [8.6, at(n,"但你看")-0.3], [10.0, at(n,"它写了")-0.4], [13.9, at(n,"这种小加工")], [17.1, t]],
        "drop_masks": DROP, "masks_extra": [USER],
        "patch": [{"contains": "数字：", "set": {"label": "数字和数据表逐个对", "zoom": 1.9, "focus": True}},
                  {"contains": "比价", "set": {"label": "材料里没提「比价」", "zoom": 2.2, "focus": True}},
                  {"contains": "右侧是成品", "set": {"label": None}}],
        "notes": [{"out": [at(n,"看三样")-0.2, t-0.2], "x": 180, "y": 300, "title": "验收看三样", "lines": [
            ["① 数字对不对", at(n,"数字对不对"), "全对", at(n,"全对"), good],
            ["② 有没有编", at(n,"有没有写"), "多写了「比价」", at(n,"没说比价"), warn],
            ["③ 四段齐不齐", at(n,"四段是不是"), "齐", at(n,"四段也齐"), good]]}]})]
    # K 找文件
    n = "K找文件"; t = T[n]
    P[n] = [("R", f"{F}/K5-找文件.mov", {"anchors": [[2.2, 0], [4.6, at(n,"右上角")+0.5], [7.0, at(n,"打开文件夹")+0.3], [13.0, t]],
        "drop_masks": DROP, "masks_extra": [USER, {"name": "Finder侧栏", "rect": [428,126,168,428], "t": [[7.2, 20]], "style": "fillmed"}],
        "events_extra": [{"t": 8.6, "kind": "move", "target": [958,182,78,96], "label": "成品在这里", "zoom": 1.5, "dur": 3.2}],
        "patch": [{"contains": "右上角", "set": {"zoom": 1.9}}, {"contains": "打开文件夹", "set": {"zoom": 1.9}}]})]
    # I 三个坑：前两个用卡片，第三个配权限实拍
    n = "I坑"; t = T[n]; p2 = at(n,"第二") - 0.15; p3 = at(n,"第三") - 0.15
    P[n] = [("CARD", "pit12", p3, [
                {"from": 0, "to": p2, "lines": [("容易踩的坑 · 1", "t", 0.2), ("它读不到你没授权的地方", "s", at(n,"它读不到")), ("材料一定放进选中的文件夹", "b", at(n,"所以材料"))]},
                {"from": p2, "to": p3, "lines": [("容易踩的坑 · 2", "t", p2+0.1), ("重要文件别直接丢进去", "s", at(n,"别急着")), ("先放一份副本", "b", at(n,"先放"))]}]),
            ("R", f"{F}/I-权限.mov", {"anchors": seg_anchor([[2.0, p3], [4.1, at(n,"这一集")], [5.5, at(n,"允许完全")-0.1], [6.8, at(n,"新手建议")-0.2], [12.4, t]], p3, t),
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "默认是关着", "set": {"zoom": 2.3, "focus": True, "dur": 3.4, "label": "新手一直别开", "side": "bottom"}},
                          {"contains": "完全访问开关", "set": {"label": "「允许完全访问」默认关", "zoom": False, "side": "bottom"}}]})]
    # J 收尾
    n = "J收尾"; t = T[n]; nx = at(n,"下一集") - 0.15
    P[n] = [("CARD", "j", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 装好、登录，认清左边 7 个入口", "n", at(n,"先装好")), ("② 让它在一个文件夹里干活", "n", at(n,"让它在")),
                                         ("③ 需求说清：做什么 · 有什么材料 · 要什么结果", "n", at(n,"需求说清"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("把门锁好", "b", at(n,"把门锁好")), ("它到底能碰什么，怎么让它别乱来", "s", at(n,"它到底"))]}])]
    return P

def build(it):
    if it[0] == "R": return render(it[1], it[2])
    if it[0] == "CARD": return card(it[1], it[2], it[3])

def subs_cues():
    cues = []; off = 0.0
    for n in ORDER:
        parts = [p for p in re.split(r"(?<=[。！？，：；])", TEXT[n]) if p.strip()]; cl = []; cur = ""
        for p in parts:
            if len(cur) + len(p) <= 18 or not cur: cur += p
            else: cl.append(cur); cur = p
        if cur: cl.append(cur)
        sc = "".join(script_chars(n)); starts = [0.0]*len(cl)
        # 按字数位置直接取时间，避免短语重复匹配
        ts = char_times(n); k = 0
        for i, c in enumerate(cl):
            cc = [ch for ch in c if ch not in PUN and not ch.isspace()]
            j = min(len(ts)-1, round(k*len(ts)/len(sc))); starts[i] = ts[j] + LEAD; k += len(cc)
        for i, c in enumerate(cl):
            e = starts[i+1] - 0.05 if i+1 < len(cl) else AD[n] + LEAD + 0.25
            cues.append((off + starts[i], off + e, c.rstrip("，。；：！？").strip()))
        off += T[n]
    return cues

def main():
    P = plan(); items = [(n, it) for n in ORDER for it in P[n]]
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(lambda x: build(x[1]), items))
    segfiles = []; i = 0
    for n in ORDER:
        ps = res[i:i+len(P[n])]; i += len(P[n])
        lst = f"{B}/lst_{n}.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in ps))
        vcat = f"{B}/seg_{n}_v.mp4"; subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lst,"-c","copy",vcat], check=True)
        vd = dur(vcat); total = T[n]; out = f"{B}/seg_{n}.mp4"
        subprocess.run(["ffmpeg","-y","-v","error","-i",vcat,"-i",f"{A}/{n}.wav","-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={max(0,total-vd)+0.1:.3f},fps=30,trim=duration={total:.3f}[v];"
            f"[1:a]aresample=48000,adelay={int(LEAD*1000)}:all=1,apad=whole_dur={total:.3f}[a]",
            "-map","[v]","-map","[a]","-t",f"{total:.3f}","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",
            "-c:a","pcm_s16le",out.replace(".mp4",".mov")], check=True)
        segfiles.append(out.replace(".mp4",".mov")); print(f"{n}: video {vd:.2f}s / seg {total:.2f}s")
    open(f"{B}/final.txt","w").write("".join(f"file '{p}'\n" for p in segfiles))
    nosub = f"{B}/final_nosub.mov"
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{B}/final.txt","-c","copy",nosub], check=True)
    # 字幕条
    font = ImageFont.truetype(FONT, 44); ins = []; fl = []; last = "0:v"
    for k, (a_, b_, t_) in enumerate(subs_cues()):
        im = Image.new("RGBA", (1920,110), (0,0,0,0)); d = ImageDraw.Draw(im)
        w = d.textlength(t_, font=font); d.text(((1920-w)/2, 26), t_, font=font, fill=(250,250,250,255))
        pth = f"{B}/sub{k}.png"; im.save(pth); ins += ["-i", pth]
        fl.append(f"[{last}][{k+1}:v]overlay=0:970:enable='between(t,{a_:.3f},{b_:.3f})'[v{k}]"); last = f"v{k}"
    final = os.environ.get("EP_OUT", f"{V}/ep01-v4.mp4")
    subprocess.run(["ffmpeg","-y","-v","error","-i",nosub]+ins+["-filter_complex",";".join(fl)+f";[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]",
        "-map",f"[{last}]","-map","[a]","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",final], check=True)
    print("final", dur(final))

if __name__ == "__main__": main()
