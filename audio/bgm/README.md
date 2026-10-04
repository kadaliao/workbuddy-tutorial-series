# 背景音乐来源与授权

全部来自 Mixkit（mixkit.co），授权为 Mixkit Stock Music Free License（https://mixkit.co/license/#musicFree）。
Mixkit 官方说明（mixkit.co/llms.txt，2026-10-04 查阅）：Free License 允许用于商业项目（YouTube 视频、社交媒体营销、网络广告等）和个人项目，不需要署名。
页面元数据里每首的 copyrightNotice 都是 "Mixkit Stock Music Free License"。

| 文件 | 曲名 | 作者 | 风格 | 时长 | 原始地址 |
|---|---|---|---|---|---|
| mixkit-132-hazy-after-hours.mp3 | Hazy After Hours | Alejandro Magaña (A. M.) | Electronica | 2:07 | https://assets.mixkit.co/music/132/132.mp3 |
| mixkit-568-focus-on-yourself.mp3 | Focus on Yourself | Eugenio Mininni | Electronica | 4:46 | https://assets.mixkit.co/music/568/568.mp3 |
| mixkit-609-moon-walk.mp3 | Moon Walk | Eugenio Mininni | Electronica | 3:25 | https://assets.mixkit.co/music/609/609.mp3 |

选曲依据（我没法试听，只能做客观分析）：从 Mixkit 的 technology / corporate / ambient 三个标签里取 12 首候选，测了响度起伏（LRA）、频谱亮度，并用 whisper 检查有没有人声。Whisper 在 175、480、570 三首里识别出了疑似词语，可能带人声切片，已排除；起伏太大的（593，LRA 16.5）也排除了。
注意：免费曲库的曲子别人也可以用；如果以后要在 YouTube 上变现，留意有没有被误认领版权，必要时附上 Mixkit 授权页链接申诉。
