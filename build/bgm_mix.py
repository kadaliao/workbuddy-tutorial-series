#!/usr/bin/env python3
"""给成片铺背景音乐：曲子循环接满全片（交叉淡化）→ 片头稍响、正片压低 → 人声出现时再自动避让 → 结尾淡出。
用法: bgm_mix.py 输入.mp4 曲子.mp3 输出.mp4 [--intro 片头秒数] [--start 曲子起点秒] [--len 只输出前 N 秒]
曲子来源与授权见 video/audio/bgm/README.md
"""
import argparse, subprocess, re

def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def lufs(f):
    o = subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","ebur128","-f","null","-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("track"); ap.add_argument("out")
ap.add_argument("--intro", type=float, default=15.09); ap.add_argument("--start", type=float, default=4.0)
ap.add_argument("--len", type=float, default=0); ap.add_argument("--body", type=float, default=-31.0, help="正片配乐响度 LUFS（避让前）")
ap.add_argument("--head", type=float, default=-23.0, help="片头配乐响度 LUFS")
ap.add_argument("--duck-th", type=float, default=0.03, help="人声避让阈值（越大避让越轻）")
ap.add_argument("--bed-only", action="store_true", help="只输出避让后的配乐（用于测电平）")
ap.add_argument("--duck-ratio", type=float, default=5.0, help="人声避让压缩比（越小避让越轻）")
a = ap.parse_args()
L = a.len or dur(a.src); T = dur(a.track); seg = T - a.start - 3.0; XF = 4.0
n = int(L // (seg - XF)) + 2
g = a.body - lufs(a.track)              # 把整首拉到正片目标响度
dh = a.head - a.body                     # 片头额外抬高的 dB
fi = a.intro
# 曲子切段循环
parts = []; chain = []
for i in range(n):
    parts += ["-ss", f"{a.start}", "-t", f"{seg}", "-i", a.track]
fc = []
for i in range(n): fc.append(f"[{i+1}:a]aresample=48000,aformat=channel_layouts=mono[m{i}]")
last = "m0"
for i in range(1, n):
    fc.append(f"[{last}][m{i}]acrossfade=d={XF}:c1=tri:c2=tri[x{i}]"); last = f"x{i}"
# 音量：片头 dh dB → 片头结束前后 1.2s 过渡到正片 → 结尾 4s 淡出
vol = f"volume='{g:.2f}dB',volume='if(lt(t,{fi-0.6}),{10**(dh/20):.4f},if(lt(t,{fi+0.6}),{10**(dh/20):.4f}+(1-{10**(dh/20):.4f})*(t-{fi-0.6})/1.2,1))':eval=frame"
fc.append(f"[{last}]atrim=0:{L},{vol},afade=t=in:d=0.4,afade=t=out:st={L-4}:d=4[bg]")
fc.append(f"[0:a]aresample=48000,asplit=2[vo][key]")
fc.append(f"[bg][key]sidechaincompress=threshold={a.duck_th}:ratio={a.duck_ratio}:attack=40:release=600:makeup=1[duck]")
fc.append(f"[vo][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" if not a.bed_only else "[vo]anullsink;[duck]anull[a]")
cmd = ["ffmpeg","-y","-v","error","-i",a.src] + parts + ["-filter_complex",";".join(fc),"-map","0:v","-map","[a]",
       "-t",f"{L}","-c:v","copy","-c:a","aac","-b:a","192k","-ac","1","-movflags","+faststart",a.out]
subprocess.run(cmd, check=True)
print(a.out, dur(a.out), "mix LUFS", lufs(a.out))
