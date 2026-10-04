# WorkBuddy 官方事实核查（面向零基础教学视频）

核查日期：2026-10-03。只使用官方来源：workbuddy.cn 官网及 /docs、官方更新日志、官方 llms.txt、官方定价页。以下结论均为抓取官方页面正文后的归纳，不是照抄旧说法。

## 0. 当前最新版本

- 官方更新日志最新条目：**5.6.2，发布日期 2026-09-21**（上一条 5.6.0，2026-09-19）。来源：https://www.workbuddy.cn/docs/workbuddy/Changelog 、https://www.workbuddy.cn/docs/workbuddy/Changelog-5.6.2
- 文档站构建时间为 2026-09-30，站点 sitemap 中也没有比 5.6.2 更新的版本页（https://www.workbuddy.cn/docs/sitemap-workbuddy-workbuddy.xml）。因此"最新版 = 5.6.2"在文档层面成立；官网下载按钮实际指向的安装包版本无法用 curl 核到（首页是前端渲染），见文末"需实机验证"。
- 「历史版本下载」页只列到 5.1.2（2026-06-17），不含 5.2 之后版本，不能用来判断最新版。来源：https://www.workbuddy.cn/docs/workbuddy/Download-History
- 版本节奏很快：2026-06-03 的 5.0.0 到 2026-09-21 的 5.6.2，约每 2 到 3 天一版。录制时务必再看一次「头像 > 检查更新」或「设置 > 关于」显示的版本号。
- 正式公测上线日期：2026-03-09（官方 llms.txt）。来源：https://www.workbuddy.cn/llms.txt

## 1. 下载、安装、登录

**平台与系统要求**
- macOS：要求 macOS 12 (Monterey) 及以上；安装包分 **Mac ARM64（M 系列）** 与 **Mac X64（Intel）**，官网识别不了设备时默认给 X64（可经 Rosetta 在 M 芯片运行，反之 ARM64 不能在 Intel 上运行）。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Mac-Guide
- Windows：Windows 10 及以上，x64；不支持 Win7/8/8.1；**Windows 11 ARM64 暂不支持**（FAQ 明确写了"当前版本暂不支持 ARM 64 架构的 Windows 11"）。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/FAQ
- 历史版本页的安装包文件名形如 darwin-arm64 / darwin-x64 / win32-x64-user（.dmg / .exe），与上面一致。来源：Download-History 页链接。
- 移动端：**iOS** 在 App Store 搜「WorkBuddy」；**Android** 在华为应用市场、小米应用商店、应用宝等搜「WorkBuddy」。来源：https://www.workbuddy.cn/docs/workbuddyapp/Overview
- **鸿蒙**：官方文档没有独立的"鸿蒙版 WorkBuddy App"说法。只在两处出现鸿蒙：QQ 邮箱连接器扫码要求"QQ 邮箱 App 7.1.5 / 鸿蒙 0.2.9 及更新版本"；FAQ 说"鸿蒙 6 的微信扫码当前不兼容，鸿蒙 4 正常，可先用安卓手机扫码再切回"。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector 、FAQ 页。可以说"华为应用市场可下载 Android 版"，但不要写"支持鸿蒙原生"。
- 微信小程序：搜「腾讯 WorkBuddy」或扫码进入，分"云上模式 / 本机模式"。来源：https://www.workbuddy.cn/docs/workbuddymini/quick-start/Overview
- 移动端 App 两种执行模式：「云端工作」（云沙箱，默认）与「连接电脑」（远程操控桌面端；要求 App 与电脑端用同一微信账号登录、电脑端保持运行）。来源：https://www.workbuddy.cn/docs/workbuddyapp/Quickstart

**安装流程**：Mac 双击 .dmg 把图标拖进 Applications；Windows 双击 .exe 按向导（建议勾选桌面快捷方式）。更新：头像 > 检查更新，有新版会自动下载并升级。来源：同上两份安装指南。

**登录**
- 点「登录」后浏览器打开 workbuddy.cn 登录页，勾选《用户服务协议》《隐私政策》，**微信扫码**；也支持**手机号、邮箱、SSO**，全程在当前页面完成。来源：Installation-Mac-Guide / Installation-Win-Guide。
- 个人用户选「个人登录」，购买企业版的用户选「企业登录」。来源：https://www.workbuddy.cn/docs/workbuddy/FirstTask
- 移动 App 登录可选手机号 / QQ / 微信 / 其他。来源：https://www.workbuddy.cn/docs/workbuddyapp/Quickstart
- 界面语言：头像 > 设置 > 通用 > 语言（5.6.0 新增巴西葡萄牙语、印尼语界面）。

**接入即时通讯（"助理"）**：支持**微信助理（官方推荐）、微信客服号、企微助理、QQ 机器人、飞书、钉钉机器人**；另有**元宝派**接入指南。配置入口：头像 > 设置 > 助理设置。要求电脑开机并运行 WorkBuddy；飞书、钉钉、企微、QQ 需先在各自开放平台建应用/机器人，微信客服号可扫码绑定。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Assistant 、https://www.workbuddy.cn/docs/workbuddy/WeixinBot-Guide 、https://www.workbuddy.cn/docs/workbuddy/YuanBaoPai-Guide
- 远程任务的安全边界：绑定身份、来源校验、删除文件/改系统配置/批准命令执行等高风险操作需在手机上确认。

## 2. 主界面入口

官方「左侧导航栏」页给出的一级入口自上而下：**新建任务、助理、项目、专家·技能·连接器、自动化、资料库、更多**。顶部显示版本号和「发现应用」；底部有消息中心、多端协同、头像。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Sidebar
- 「更多」收纳低频入口：**我的邮箱、腾讯文档、ima、乐享知识库、灵感、Genie BaaS**。
- 一级入口顺序可自定义：在侧栏任意位置右键 > 自定义菜单，拖动即时生效；「新建任务」固定不可移动；设置只保存在当前设备。
- 区域划分：工具栏、侧边栏（任务列表按文件夹/空间分组）、对话区、右侧结果区（概览、产物等）。来源：https://www.workbuddy.cn/docs/workbuddy/Overview
- **名称变化**：5.5.4（2026-09-08）起客户端把「自动化」统一更名为「**定时任务**」。但上面的侧栏页与自动化指南页仍沿用"自动化"。来源：https://www.workbuddy.cn/docs/workbuddy/Changelog-5.5.4 。录制时以实机显示为准。
- 注意：资料库在旧说法里属于"更多"，现在官方侧栏页把「资料库」列为一级入口，「更多」里放的是腾讯文档/ima/乐享/灵感等。

## 3. 工作空间与权限

- **工作空间**：当前任务主要读取和保存文件的文件夹。新建任务时选的目录、或 WorkBuddy 自动创建的任务目录，都作为本次任务的工作空间；入口在输入框左下角「选择工作空间」。不选则在默认目录生成结果。建议按任务类型分别建空间，并只放文件副本。来源：https://www.workbuddy.cn/docs/workbuddy/Create-Task 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes
- **两种权限**：「默认权限」与「完全访问权限」。入口是输入框底部常驻的权限状态按钮（默认显示「默认权限」），通过「允许完全访问」开关切换。来源：Permission-Modes 页。
- **默认权限**：以工作空间为边界；命令优先在**沙箱**约束下执行；写受保护/敏感路径、删除受保护文件或批量删除、执行脚本/命令/外部程序、网络访问或敏感能力命中安全规则时，会暂停并要求你确认（高危操作确认）；另有删除保护（安全删除/回收站）和**文件备份**（修改已有文件前备份，可在「设置 > 安全中心」开关）。
- **完全访问权限**：关闭二次确认，写文件、删文件、执行脚本、调用外部程序都不再逐步确认；**对当前客户端内所有任务全局生效**，不跨设备；切换时有「确认允许完全访问？」弹窗，需勾选风险确认。官方建议只在可恢复、隔离的环境（Docker、虚拟机、临时目录）使用。
- 官方对比表：默认权限"打断频率较高、风险低、当前任务"；完全访问"打断很低、风险高、全局"。
- **"日志"**：权限页正文未提到"日志"功能。只有「安全中心」「使用行为日志」等字样出现在隐私说明里。教学视频里不要承诺有权限日志页，见文末待验证。
- 自动化（定时任务）新建时也可选默认权限/完全访问权限。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide

## 4. 三种模式与三大场景

- **三种工作模式**：**默认（Agent）**、**计划（Plan）**、**仅问答（Ask）**。默认即 Agent；在输入框左侧「+」菜单里可开「计划」或「仅问答」，两者互斥，关闭后回默认；非默认模式时输入框下方显示标识，点 × 退出。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar
  - Plan：先补信息、给完整方案，确认后才执行；可反复调整。
  - Ask：只问答找思路，不做执行。
  - 差异：官方 llms.txt 仍把三模式写成 "Craft / Plan / Ask"，更新日志 5.1.1 也出现过"Chat/Craft"字样，是旧叫法。当前帮助文档用「默认（Agent）/ 计划 / 仅问答」。来源：https://www.workbuddy.cn/llms.txt
- **三大场景**：新建任务页按「日常办公、代码开发、设计创意」提供场景和提示词模板（悬停预览灰色文案，点击才填入）。来源：https://www.workbuddy.cn/docs/workbuddy/Create-Task
  - 设计创意：集成腾讯设计 **Ardot** 画布，首次使用需授权连接（通过登录手机号自动关联），在新建任务页最右侧「设计创意」Tab。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Design-Idea
  - 代码开发：兼容用户级/项目级 .codebuddy 配置；5.4.0 起支持 Worktree 任务、Git 分支展示、独立终端。来源：https://www.workbuddy.cn/docs/workbuddy/Changelog-5.4.0

## 5. 文件来源、产物、分享

- **添加上下文的方式**：「@」引用文件/文档/规则、Ctrl/Cmd+V 粘贴截图、上传按钮或拖拽文件（最多 50 个，单文件大小不限，格式规则同上传按钮）、粘贴超过 3000 字符自动收起为胶囊、从微信/企业微信转发聊天记录。来源：Create-Task 页、Task-Bar 页。
- **云端来源**：「+」菜单与上传图标旁可打开**腾讯文档、ima 知识库、乐享知识库**并勾选文件加入对话；也可在「资料库」里选择对应知识库后"添加到任务"。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Knowledge-Base/Lexiang 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Knowledge-Base/Tencent-Doc 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Knowledge-Base/IMA%20Knowledge%20Base/01-Workbuddy-IMA-Basic-Guide
  - 腾讯文档：授权后可搜索、预览、引用、回写；乐享：微信扫码或手机号登录，首次需绑手机号；ima：个人版微信扫码，企业账号有"企业版 + 个人版"双连接器。
- **产物预览**：右侧结果区含「概览/工作空间文件、浏览器、变更、产物」；产物支持 Word/MD/PDF、Excel/CSV、PPT 等预览；网页产物可在内置浏览器看效果。来源：https://www.workbuddy.cn/docs/workbuddy/Results 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar
- **保存**：预览产物时点右上角分享图标，可**上传到云端：我的云端网盘、腾讯文档、ima 知识库、乐享知识库**。文件预览窗的「更多」里有"打开文件夹"和"另存为"。产物默认就写在本地工作空间，右键"打开文件夹"可在 Finder/资源管理器定位。来源：Results 页、Right-Sidebar 页、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/File-Browser
- **分享**：对话区顶部有「分享任务」（自动生成**公开链接**）；产物也可生成分享链接并在线预览，5.x 起可分享到微信。已分享文件可在「头像 > 设置 > 数据管理」复制链接、下载或取消分享。来源：https://www.workbuddy.cn/docs/workbuddy/Conversation 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Data
- 对话顶部从左到右：对话内搜索、分享任务、历史提问、显示详情面板。

## 6. 技能、斜杠指令、专家、资料库、连接器、自动化

- **技能 Skills**：入口「专家·技能·连接器」的技能页，分「技能市场」与「已安装」。添加方式：**上传技能（导入本地技能包）、查找技能（描述需求让 WorkBuddy 找）、创建技能（描述需求自动创建）**；可启用/关闭（不卸载）、搜索、批量卸载。官方称内置 20+ 技能包，兼容 OpenClaw 社区技能导入。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market 、Task-Bar 页
- **斜杠指令**：输入 `/` 出补全面板。项目会话里读取项目 `.codebuddy/commands/` 与用户级、内置命令；插件也可带快捷指令，如 `/周报`。5.5.0 提升了斜杠命令面板响应速度。来源：Task-Bar 页、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Plug-In 、https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project 。官方没有一份面向普通用户的"内置斜杠命令清单"，见待验证。
- **插件**：打包技能、MCP、快捷指令、Hooks、Agents，有插件市场，可启用/停用/更新。
- **专家 / 专家团**：专家中心按行业分类；专家 = 角色切换（人设 + 方法论 + 工具链），专家团 = 多专家协作（团长自动拆解、并行、整合）。使用：专家·技能·连接器 > 专家，点「召唤」；创建：右上角「我的专家」> 创建专家，由内置专家管理工具通过对话引导配置。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Expert-Center
- **资料库**：人与 Agent 共用的产物存放地，一棵目录树（MD/CSV/HTML 为 AI 三件套，也放 PDF/Office/图音视频），个人「我的文档」与「团队空间」分区；AI 对 MD 的修改以待确认状态呈现；可把本地 HTML 发布成在线链接。套餐决定容量（体验版 5GB 起）。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Library
- **连接器**：当前支持 QQ 邮箱、腾讯文档、腾讯乐享、腾讯会议、TAPD、腾讯网盘等，也支持自定义连接器。添加：专家·技能·连接器 > 连接器页签 > 卡片右上「+」授权；使用：连接器页「去对话」，或输入框「+ > 连接器」开启，或任务中途按引导卡片连接。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector
- **MCP**：用户级 `~/.workbuddy/mcp.json`、项目级 `<项目>/.workbuddy/mcp.json`；5.6.0 恢复"可直接编辑 mcp.json 整份配置并即时生效"。MCP 页写的入口是「侧边栏 插件 > MCP 服务器 > 配置 MCP」，与侧栏页"专家·技能·连接器"的叫法不完全一致。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide 、https://www.workbuddy.cn/docs/workbuddy/Changelog-5.6.0
- **定时任务（原"自动化"）**：配置项为名称、提示词、工作空间（默认自动分配 automation-xxxx）、权限模式、模型/技能/专家/连接器、定时规则（支持每周多天、每月多天、单次、生效日期区间）、可选推送到小程序或企业微信 bot；提供任务模板（新闻推送、周报等）。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide 。5.5.4 起客户端改名「定时任务」。
- **项目**：团队协作能力，项目配置含指令、连接器、专家、技能，任务可分享/转交/多人协作。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project

## 7. 个性化、增强提示词、模型、对话与搜索

- **个性化设置**：设置 > 功能个性化，含回复风格、加载欢迎语、**自定义指令**、称呼与身份。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Setting
  - **自定义指令字数上限：官方文档未写明任何数字**（全站检索无）。不能沿用旧数字，必须实机核。
- **记忆**：默认开启；每晚整理当天会话，仅本人可见；入口「头像 > 设置 > 记忆与进化」，可查看、对话式编辑、清空、一键关闭；**支持从其他 AI 导入记忆**（复制官方示例提示词到其他 AI，把结果粘贴回来点「添加到记忆」）；记忆提取不消耗积分；支持历史会话检索。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory
- **增强提示词**：帮助文档没有任何正式说明页，只在更新日志里以"修复增强提示词跨会话泄漏 / 回流误判 / 海外版不可用"出现，说明功能存在。入口和交互需实机核。来源：https://www.workbuddy.cn/docs/workbuddy/Changelog
- **模型（桌面端内置，以 5.6.2 对应文档为准）**：Hy4 preview、Hy3、GLM-5.3、GLM-5.3-Flash、GLM-5.2、GLM-5.1、GLM-5v-Turbo、MiniMax-M3、MiniMax-m2.7、Kimi-K3、Kimi-K2.7-Code、Kimi-K2.6、DeepSeek-V4-Flash、DeepSeek-V4-Pro；另有 **Auto** 自动选模型（App 端默认）。企业管理员可禁用部分模型。来源：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Model 、https://www.workbuddy.cn/docs/workbuddyapp/features/Model
  - 旧说法"混元/DeepSeek/GLM/Kimi/MiniMax"五个系列仍在，但具体型号全部更新（混元已是 Hy3 / Hy4 preview，DeepSeek 是 V4，Kimi 是 K3 等）。
  - 另有三档模型模式：快速、均衡、极致；思考强度；上下文窗口默认 **200K**（部分模型支持 1M），**Max 模式**（不压缩上下文，积分消耗明显更快）默认关闭。5.5.4 起上下文档位按模型分别记忆。
  - 支持自定义模型（可视化界面添加；API Key 仅存本地 models.json），可接腾讯云 Token Plan、Coding Plan、Ollama 本地模型。
  - 对话中途换模型：当前轮进行时，切换下一轮生效，并提示可能降低性能、增加积分消耗。来源：Task-Bar 页。
- **积分倍率**：模型选择面板在每个模型名下标注倍率，如 x0.80、x1.00，数字越低消耗越少（App 文档给出的描述）。**桌面端文档没有给出各模型倍率表**，见待验证。来源：https://www.workbuddy.cn/docs/workbuddyapp/features/Model
- **对话折叠**：更新日志有 4.8.0「对话流指令折叠」、4.21.0「对话消息分段折叠」；长文本粘贴超 3000 字符自动收起为胶囊。官方帮助文档没有独立的"对话折叠"说明页。来源：https://www.workbuddy.cn/docs/workbuddy/Changelog
- **多任务并行**：每个对话是独立任务，各有独立工作空间与上下文，侧栏可切换，官方明确支持多任务并行；模型运行中仍可继续发消息，进入输入框上方队列（可编辑、删除、拖动排序）。来源：Task-Bar 页、Conversation 页。
- **历史搜索**：窗口左上角搜索按钮或 **Cmd+K / Ctrl+K**，全局搜索覆盖任务、空间、产物，分「全部/任务/空间/产物」；另有列表筛选（按状态、日期）、对话内搜索、「历史提问」。来源：https://www.workbuddy.cn/docs/workbuddy/Task-Management

## 8. 计费、积分、免费额度、会员

来源：https://www.workbuddy.cn/docs/workbuddy/Pricing 、https://www.workbuddy.cn/docs/workbuddy/Credits 、https://www.workbuddy.cn/docs/workbuddy/Usage 、https://www.workbuddy.cn/docs/workbuddy/Plan

- 2026-07-01 起，个人版从单一"专业版"改为**体验版（免费）/ 标准版 / 高级版 / 旗舰版**四档。
- 价格：标准 99 元/月、高级 199 元/月、旗舰 999 元/月；连续包月 7 折（70 / 140 / 700 元/月）；连续包年 5.6 折（672 / 1,344 / 6,720 元/年）。
- 积分：体验版基础 500/月；标准 2,000、高级 4,000、旗舰 20,000 基础积分/月，另有"限时加赠"（标准 2,000、高级 5,000、旗舰 30,000），每月实得标准 4,000 / 高级 9,000 / 旗舰 50,000。赠送积分自到账日起 1 个月有效；积分按月发放，当月有效不结转。
- 体验版限免项：自动任务 3 个（限免 99 个）、全模型可选（限免）、单项目成员 3 人（限免 5 人）、代码补全 5,000 次/月（限免无限次）。限免截止日期官方页未写。
- 加量包：1,000 积分 / 50 元 / 有效期 1 个月，标准版及以上才能买；生效后不可退款。
- 扣减顺序：先扣最先到期的，同时到期先扣基础积分再扣赠送积分。所有对话相关请求都耗积分；记忆提取不耗积分。
- WorkBuddy 与 CodeBuddy 共用同一账号积分。
- 套餐只能升不能降；升级按剩余价值折算。到期降为体验版，已生成内容不受影响。
- 查看：客户端「头像 > 设置 > 套餐与积分」；官网「个人中心 > 套餐与用量」可看积分消耗明细。
- 其他：5.0 起文档里还有"成长计划"（个人中心 / 头像里，完成任务领 Credits），属活动性质，可能随时变。企业版计费另有页面（Pricing 页指向企业版计费概述）。
- 对视频的影响：价格、积分、限免都是易变项，口播里建议说"以官网定价页为准"，画面避免定格具体数字，或在字幕标注日期 2026-10。

---

## 与旧说法的差异清单

1. 当前最新版 5.6.2（2026-09-21），不要再使用任何更早的版本截图；界面几乎每周在变。
2. 三种模式官方称谓：默认（Agent）/ 计划 / 仅问答；"Craft"是旧称，仍残留在官方 llms.txt 中。
3. 「自动化」自 5.5.4 起客户端更名为「定时任务」；官方侧栏页和自动化指南页还沿用旧名。
4. 侧栏一级入口现为：新建任务、助理、项目、专家·技能·连接器、自动化(定时任务)、资料库、更多；「资料库」已是一级入口，「更多」里是我的邮箱、腾讯文档、ima、乐享知识库、灵感、Genie BaaS。入口可右键自定义。
5. 平台：官方只写了 macOS（ARM64 与 X64）、Windows x64（Win11 ARM64 不支持）、iOS、Android、微信小程序；**没有鸿蒙原生 App 的官方说法**，鸿蒙仅作为兼容性备注出现。
6. 助理接入除微信助理、企业微信、QQ、飞书、钉钉外，还有微信客服号与元宝派；微信助理被标为"推荐"。
7. 模型列表已大幅更新：Hy4 preview / Hy3、GLM-5.3 / 5.2 / 5.1 等、MiniMax-M3 / m2.7、Kimi-K3 / K2.7-Code / K2.6、DeepSeek-V4-Flash / Pro，另有 Auto；新增快速/均衡/极致、思考强度、200K/1M 上下文、Max 模式。
8. 计费由旧"专业版"改为 2026-07-01 起的体验/标准/高级/旗舰四档，含限时加赠积分和限免项；基础积分 500 / 2,000 / 4,000 / 20,000。
9. 文件来源与分享：产物可上传到我的云端网盘、腾讯文档、ima、乐享；分享任务生成公开链接，已分享文件在「设置 > 数据管理」统一管理。
10. 新增能力（旧版可能没有）：行业 Buddy 应用（5.5.0）、微信聊天记录转发进输入框、消息队列、引用模型输出（5.6.0 还可引用他人消息）、全局搜索 Cmd/Ctrl+K、Worktree 任务、图片处理（去水印、抠图等）、设置里的「应用管理」、语音输入。

## 官方文档没覆盖、需要实机验证的点

1. 官网首页「立即下载」当前提供的安装包版本号、各平台下载入口的实际文案（Mac ARM64 / X64 / Windows），以及客户端「设置 > 关于」显示的版本。
2. 自定义指令的**字数上限**（官方无数字）；个性化页的实际字段和提示文案。
3. **增强提示词**的入口位置、触发方式、效果（官方只有更新日志侧面提及）。
4. 权限相关：是否有可查看的"日志/审计"页面；「安全中心」里实际有哪些开关（删除保护、文件备份）；高危操作确认弹窗的真实样子；切到完全访问权限的确认弹窗。
5. 侧栏实际显示：入口是叫「自动化」还是「定时任务」；「资料库」在一级还是「更多」；腾讯文档/ima/乐享是在资料库内还是「更多」里。
6. 「+」菜单当前包含哪些项（计划、仅问答、连接器、腾讯文档/ima/乐享入口）与顺序；输入框上方的场景 Tab（日常办公 / 代码开发 / 设计创意）当前叫法。
7. 模型选择面板里每个模型的**积分倍率**真实数字，以及体验版账号当前可选的模型范围（限免是否仍有效）；Auto 是否仍为默认。
8. 体验版账号的实际积分余额、限免是否过期，以及「套餐与积分」页的实际布局。
9. 内置斜杠命令清单（输入 `/` 后默认出现哪些命令），不带项目时的表现。
10. 对话折叠的实际表现与是否可由用户控制；多任务并行时侧栏的状态标识。
11. 保存产物到本地与云端的实际按钮位置（桌面端"分享图标 > 上传到云端"与"另存为"的菜单文案）。
12. 官方「分享任务」的实际流程与链接有效期、隐私提示；录屏前注意脱敏。
13. 登录页：个人 / 企业登录的实际入口，微信扫码以外的方式（手机号、邮箱、SSO）是否都展示。
14. 鸿蒙设备能否安装 Android 版、应用市场实际搜索结果（官方未说明）。
