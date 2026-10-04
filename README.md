# WorkBuddy 零基础实战 · 系列教程视频工程

2026-10-03 ～ 10-04 制作的 WorkBuddy 5.6.2 零基础教学系列（第 1～12 集 + 番外），已发布到微信视频号合集「Buddy零基础实战」。

成片视频不放在仓库里，见 GitHub Release 附件。

## 目录
- `00-brief.md`：项目要求；`10-series-plan.md`：系列规划
- `01-official-facts.md`：官方事实核查；`03-hands-on-log.md`：实机记录与全过程日志；`02-blockers.md`：阻塞记录
- `scripts/`：每集脚本（含成片实际使用的口播）
- `shots/`：实机截图
- `build/`：制作工具
  - `human.py`：拟人鼠标键盘 + 录屏（ffmpeg avfoundation）；`ocr.py`：macOS Vision 屏幕文字定位；`wslib.py`：选工作空间等通用操作；`inputsrc.py`：录制时切换输入法
  - `annotate4.py`：录屏/静帧 → 带推近、高亮框、标注、字幕条、遮挡的画面
  - `epkit.py`：每集流水线（Gemini TTS 配音 + whisper 逐字对齐 + 听验 → 画面 → 字幕 → 片头 → 配乐）；`epNN.py`：各集编排；`scene_*.py`：各集录制脚本
  - `intro.py`：系列片头；`bgm_mix.py`：配乐循环、避让、响度；`covers.py`：视频号 3:4 / 4:3 封面
  - `publish_ep.py`：发布到审阅页；`sph.py` / `sph_one.py`：微信视频号助手批量上传与定时
- `publish/`：视频号文案与封面
- `site/`：审阅页（不含视频）
- `audio/bgm/README.md`：配乐来源与授权（Mixkit 免费授权）

## 依赖
macOS、ffmpeg、Python venv（Pillow、numpy、pyobjc Quartz/Vision）、openai-whisper、tts skill（Gemini 3.8 Flash TTS via aihubmix）。
