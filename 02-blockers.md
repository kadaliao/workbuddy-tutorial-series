# 阻塞记录

- 登录阻塞（2026-10-03）：已解决，用户已本人登录，体验继续完成。
- 当前无阻塞。未完成项：斜杠下拉菜单（/）未截到、添加定时任务对话框未弹出，均已在 03-hands-on-log.md 标注，需要时可再派我补拍。

## 阻塞 2：Mac 屏幕处于锁屏状态（2026-10-04 00:19）

- 卡在哪一步：第 1 集实机素材（镜头 E/G/H/I/J/K 录屏，以及 dmg 安装窗口截图 C）。开始时 screencapture 只能截到全黑画面，`CGSSessionScreenIsLocked` 为 true，System Events 看不到 WorkBuddy 窗口（窗口数为 0），无法点击或录屏。我没有尝试输入任何密码。
- 需要用户做什么：在 Mac 上解锁屏幕（输入本人登录密码），确认 WorkBuddy 仍是登录状态，并在录制期间保持不锁屏、不休眠（可在系统设置中暂时把锁屏时间调长，或录制期间运行 caffeinate）。解锁后告诉我，我从镜头 E 开始继续。
- 已完成：镜头 B（官网首页）不依赖屏幕，已用 Chrome headless 截好：footage/ep01/B-官网首页.png（3840x2160）。


## 阻塞 3：Mac 再次锁屏（2026-10-04 约 01:21）

- 卡在哪一步：第 1 集二次重录（D 连贯巡览、C 真拖拽安装）。准备录前发现屏幕已锁（CGSSessionScreenIsLocked=true，IOConsoleLocked=Yes），screencapture 失败，WorkBuddy 窗口无法操作。我没有输入任何密码。
- 需要用户做什么：解锁 Mac，保持不锁屏、不休眠（可临时调长锁屏时间，或在终端运行 caffeinate -d -i -t 3600 保持）；确认 WorkBuddy 仍是登录状态。解锁后告诉我，我继续录 D 和 C。
- 已完成：旧 D/C 文件改名 _old 备份；其余镜头标注文字已改成观众视角。

## 阻塞 4：Mac 锁屏（2026-10-04 约 11:00，第 2～6 集录制前）

- 卡在哪一步：第 2 集起的实机录屏。CGSSessionScreenIsLocked=true，无法操作 WorkBuddy 窗口。我没有输入任何密码。
- 需要用户做什么：解锁 Mac，录制期间保持不锁屏、不休眠（可运行 caffeinate -d -i -t 14400）；确认 WorkBuddy 仍是登录状态。
- 解锁前先做的：核对第 2～6 集脚本，写第 7～12 集和番外的脚本，生成 Charon 配音。
