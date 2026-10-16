#!/usr/bin/env python3
"""第14集正式版：设计师技能与动效视频。素材目录保留 ep14clean 命名。"""
import json,sys,subprocess
from pathlib import Path
from epkit import *
ROOT=Path(V); B=ROOT/'build/ep14clean'
EP, TITLE = 14, "安装设计师技能，让 AI 做动效视频"
TEXT = {
  "A开场": "给 WorkBuddy 装上设计师的技能，再让它直接做一条动效视频，效果怎么样？这一期，我们从技能准备、下达需求，一直做到真正导出和播放视频。",
  "B技能": "先选一个独立的工作空间，把设计师的仓库地址交给 WorkBuddy。要求安装全部技能，保留原有内容；如果已经装过，就核验后直接使用。这台机器检测到了十五个技能，和仓库内容一致。随后，它实际加载了设计规范与动效制作技能，并读取审查标准。",
  "C需求": "需求先说清楚：制作一个动效样片，展示各种各样的动效风格，内容丰富，审美和动效能力都要好。接着把交付写具体：六十到九十秒，横屏一零八零，三十帧，最终输出能直接播放的 MP4。再要求完整编排、配乐、封面和源码，完成前审查并检查视频。",
  "D制作": "提交后，WorkBuddy 先检查浏览器、字体和编码工具，再做一张中文测试帧。确认画面能正常渲染后，才继续制作样片。这段执行需要等待，教程里做了删减。你自己操作时，可以重点看任务列表和实际输出文件。",
  "E样片": "接下来，完整看一遍 WorkBuddy 做出的动效样片。这里保留原速和它生成的配乐。",
  "F验收": "最后，打开导出的 MP4，检查开场、各个章节和结尾，再确认分辨率、帧率与声音。这次成品是七十二秒，横屏一零八零、三十帧，带有独立配乐。封面、源码和启动脚本也都放在同一工作空间。以后要换配色、节奏或者文案，可以从这些源码继续改。",
  "G收尾": "这一期的流程可以直接复用：给出技能仓库，检查安装结果，新开任务明确调用，最后验收真实作品。想让 AI 做出好动效，别只说要高级。把想看的风格、怎么体验、怎样算完成，一起说清楚。"
}
ORDER=['A开场','B技能','C需求','D制作','E样片','F验收','G收尾']
def kit(order):
 k=Kit(14,TEXT,order); k.A=str(ROOT/'audio/ep14'); k.B=str(B); return k
K=kit([n for n in ORDER if n in TEXT])
def shot(name,a,b,seconds,crop,notes=None):
 return ('R',str(B/(name+'.mov')),dict(anchors=[[a,0],[b,seconds]],cam_keys=[[a,*crop],[b,*crop]],events_override=[],drop_masks=['用户行','推广'],notes=notes or []))
def plan():
 P={}; allk=kit([n for n in ORDER if n in TEXT]); at,T=allk.at,allk.T
 n='A开场';t=T(n)
 P[n]=[shot('teaser',0,t,t,[0,0,1920,1080],notes=[{'out':[0,t],'x':190,'y':32,'title':'本期作品预览','lines':[]}])]
 n='B技能'; t=T(n); p=at(n,'要求安装'); q=at(n,'这台机器'); z=at(n,'随后')
 P[n]=[
 shot('prompt',0,5,p,[300,240,850,510]),
 ('CARD','repo',q-p,[dict(from_=0)]),
 shot('skills',5,7,z-q,[270,75,870,522]),
 shot('skills',7,13,t-z,[270,225,870,522])]
 P[n][1]=('CARD','repo',q-p,[{'from':0,'to':q-p,'last':True,'lines':[
 ('设计师技能仓库','t',0),('github.com/emilkowalski/skills','s',0.15),('安装全部技能 · 保留已有内容','n',0.5),('已安装时，先核验再调用','s',1.2)]}])
 n='C需求';t=T(n); q=at(n,'接着'); z=at(n,'再要求')
 P[n]=[
 ('CARD','request',q,[{'from':0,'to':q,'last':True,'lines':[
 ('向 WorkBuddy 下达需求','t',0),('制作一个动效样片','b',0.4),('展示丰富风格，体现审美与动效能力','s',1.6)]}]),
 shot('prompt',19,22,z-q,[325,310,800,480]),
 shot('prompt',22,25,t-z,[325,395,800,480])]
 n='D制作'; t=T(n); q=at(n,'确认画面'); z=at(n,'这段执行')
 P[n]=[shot('pipeline',0,6,q,[270,340,870,522]),
 shot('build',0,5,z-q,[270,320,870,522]),
 shot('build',5,17,t-z,[270,320,870,522],notes=[{'out':[0,t-z],'x':1050,'y':50,'title':'执行过程已删减','lines':[]}])]
 n='E样片';t=T(n)
 P[n]=[('CARD','reel-intro',t,[{'from':0,'to':t,'last':True,'lines':[
 ('WorkBuddy 动效样片','t',0),('完整作品 · 原速播放','b',0.4),('保留样片自身配乐','s',1.2)]}])]
 n='F验收';t=T(n);q=at(n,'这次成品');z=at(n,'封面')
 P[n]=[shot('result',0,8,q,[0,0,1920,1080],notes=[{'out':[0,q],'x':190,'y':32,'title':'成品验收','lines':[]}]),
 ('CARD','specs',z-q,[{'from':0,'to':z-q,'last':True,'lines':[
 ('已核对实际导出文件','t',0),('72 秒 · 1920 × 1080 · 30 fps','n',0.25),('MP4 · H.264 + AAC · 独立配乐','s',0.6),('完整解码与播放器实测通过','s',1.2)]}]),
 ('CARD','files',t-z,[{'from':0,'to':t-z,'last':True,'lines':[
 ('工作空间 / motion-reel','t',0),('视频与配乐：out/','n',0.3),('可编辑源码：src/','n',0.7),('启动脚本：run.sh','s',1.1)]}])]
 n='G收尾'; t=T(n);q=at(n,'想让')
 P[n]=[('CARD','wrap',t,[{'from':0,'to':q,'lines':[
 ('你也可以复用这个流程','t',0),('给仓库 → 核验技能 → 明确需求','n',0.4),('最后，打开真实成品验收','s',1.2)]},
 {'from':q,'to':t,'last':True,'lines':[
 ('让「高级」变成具体要求','t',q),('风格 · 交付格式 · 完成标准','b',q+0.4),('把审美要求与可验证结果一起说清楚','s',q+1.2)]}])]
 return P
if __name__=='__main__':
 selected=sys.argv[1:] or ORDER[:5]
 K=kit(selected)
 P=plan()
 K.build_body({n:P[n] for n in selected},str(B/('body-'+''.join(n[0] for n in selected)+'.mp4')))
