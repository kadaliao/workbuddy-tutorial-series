# WorkBuddy 零基础实战 · 系列教程视频工程

WorkBuddy 5.6.2 零基础教学系列。第 1～12 集 + 番外于 2026-10-03 ～ 10-04 制作，已发布到微信视频号合集「Buddy零基础实战」。第 14 集「安装设计师技能，让 AI 做动效视频」于 2026-10-16 完成交付与归档；三平台发布状态见实机记录。

成片、音频缓存和打包工程不纳入 Git；下载见 GitHub Release：

- [v1.0 · 第 1～12 集、番外与片头](https://github.com/kadaliao/workbuddy-tutorial-series/releases/tag/v1.0)
- [v1.1 · 第 14 集、动效样片与可编辑工程](https://github.com/kadaliao/workbuddy-tutorial-series/releases/tag/v1.1)

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
- `publish/`：各平台 `*_posts.json` 文案；`covers/epNN-3x4.png`、`epNN-4x3.png` 为系列封面，`epNN-16x9.png` 为已有横版封面
- `site/`：审阅页与脚本镜像（不含视频）；第 14 集入口为 `site/vr-7k3x9q/index.html#ep14v`
- `audio/epNN/`：口播文本和听验记录，音频文件从 Git 排除
- `delivery/`、`build/epNN*/`：本机交付与制作缓存，不纳入 Git
- `audio/bgm/README.md`：配乐来源与授权（Mixkit 免费授权）

## 依赖
macOS、ffmpeg、Python venv（Pillow、numpy、pyobjc Quartz/Vision）、openai-whisper、tts skill（Gemini 3.8 Flash TTS via aihubmix）。

## 第14集

正式脚本见 [设计师技能与动效视频](scripts/ep14-设计师技能与动效视频.md)，编排入口为 `build/ep14.py`，最终拼接为 `build/assemble_ep14.py`。音视频素材和依赖说明包含在 Release 的 `ep14-editing-project.zip` 中，独立样片源码为 `ep14-motion-source.zip`。

教程使用实机录屏、中文合成旁白、字幕与系列片头；中段完整播放 72 秒样片。制作时的检查记录见 [第14集验收](site/vr-7k3x9q/md/ep14-validation.md)。
