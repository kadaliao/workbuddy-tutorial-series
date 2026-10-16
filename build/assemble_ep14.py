"""拼接新片头、讲解段与原速样片；样片不叠教程BGM。"""
import json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from epkit import dur,BGM,PY,V
B=Path(V)/'build/ep14clean'
V=Path(V)
def run(a):subprocess.run(a,check=True)
def cat(files,out):
 lst=B/(out.stem+'.concat.txt');lst.write_text(''.join("file '"+str(p)+"'\n" for p in files))
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(lst),'-c:v','copy','-af','aresample=48000,aformat=channel_layouts=stereo','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)])
def mix(src,out,intro=0):
 run([PY,str(V/'build/bgm_mix.py'),str(src),BGM,str(out),'--intro',str(intro),'--start','52','--head','-17','--body','-23','--duck-th','0.1','--duck-ratio','2'])
def main(reel):
 intro=V/'intro/ep14clean/intro-ep14.mp4'
 cat([intro,B/'body-ABCDE.mp4'],B/'head.mp4')
 mix(B/'head.mp4',B/'head-mixed.mp4',dur(str(intro)))
 mix(B/'body-FG.mp4',B/'tail-mixed.mp4')
 # Normalize only the delivered tutorial's sample copy; preserve its original audio and original source file separately.
 run(['ffmpeg','-y','-v','error','-i',str(reel),'-vf','fps=30,scale=1920:1080,setsar=1','-af','loudnorm=I=-18:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',str(B/'reel-tutorial.mp4')])
 out=V/'ep14-v1.mp4'
 cat([B/'head-mixed.mp4',B/'reel-tutorial.mp4',B/'tail-mixed.mp4'],out)
 h=dur(str(B/'head-mixed.mp4'));r=dur(str(B/'reel-tutorial.mp4'))
 (B/'chapters.json').write_text(json.dumps([{'title':'技能安装与制作实操','start':0},{'title':'完整动效样片','start':h},{'title':'验收与复用','start':h+r}],ensure_ascii=False,indent=2))
 print(out)
if __name__=='__main__':main(Path(sys.argv[1]).resolve())
