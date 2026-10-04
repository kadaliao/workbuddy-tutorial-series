"""发布一集到审阅页：publish_ep.py <集数> <脚本md文件名> <视频文件> <标签名> <说明html>"""
import sys, re, os, importlib.util, shutil, subprocess
V = "/Volumes/Data-External/workspace/cc-test/wbd/video"; SITE = f"{V}/site/vr-7k3x9q"
ep, md, vid, tab, note = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
notes_extra = (sys.argv[6] if len(sys.argv) > 6 else "").replace("\\n", "\n")
sys.path.insert(0, f"{V}/build"); sys.argv = ["x"]
spec = importlib.util.spec_from_file_location("e", f"{V}/build/ep{ep:02d}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = f"{V}/scripts/{md}"; s = open(p).read()
a = s.find("## 口播稿"); s = s[:a] if a >= 0 else s
s += "## 口播稿（成片实际使用版）\n" + "".join(f"\n【{k}】\n{v}\n" for k, v in m.TEXT.items())
if notes_extra: s += "\n## 成片说明\n" + notes_extra + "\n"
open(p, "w").write(s)
shutil.copy(p, f"{SITE}/md/{md}"); shutil.copy(f"{V}/{vid}", f"{SITE}/{vid}")
h = open(f"{SITE}/index.html").read()
sid = f"ep{ep}v"
if f'id="{sid}"' in h:
    h = re.sub(rf'<section id="{sid}">.*?</section>\n', "", h, flags=re.S)
sec = (f'<section id="{sid}"><div class="card"><b>{tab}</b><p class="muted">{note}</p>'
       f'<video controls playsinline preload="metadata" style="width:100%;border-radius:8px;background:#000" src="{vid}"></video></div>'
       f'<div class="card md" data-md="md/{md}"></div></section>\n')
h = h.replace('<section id="ep1">', sec + '<section id="ep1">')
key = f'["{sid}","第{ep}集"],'
if key not in h:
    prev = '["vid","第1集视频"],'
    for e in range(ep-1, 1, -1):
        if f'["ep{e}v","第{e}集"],' in h: prev = f'["ep{e}v","第{e}集"],'; break
    h = h.replace(prev, prev + key)
h = re.sub(r"更新于 2026-10-04 \d\d:\d\d", "更新于 2026-10-04 " + subprocess.check_output(["date", "+%H:%M"]).decode().strip(), h)
open(f"{SITE}/index.html", "w").write(h)
print("published", sid)
