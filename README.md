# 奶蛙光标套装 · Naiwa Cursors

一套为 Windows 10 / 11 制作的「奶蛙」鼠标指针主题，共 17 个指针状态。每个 `.cur` 内置 32 / 48 / 64 / 128 / 256 五档图像，白色图形配深色描边，浅色和深色背景下都清晰可见。

![总览](总览.png)

## 特点

- **17 个完整状态**：对应 Windows「鼠标指针」设置里的全部 17 个角色
- **五档尺寸**：32 / 48 / 64 / 128 / 256，32bpp + AND mask，兼容旧软件
- **白色描边版**：图形为白色填充 + 深色描边，每档额外描 1px 边，小尺寸也清楚
- **热点按档位等比缩放**：以 256px 基准值换算，见 `manifest.json`
- **双安装方式**：右键 `.inf` 安装，或双击 `.bat` 一键安装
- **可二次修改**：附带 1024px 透明底母版和重建脚本

## 安装

### 方式 A：右键安装（推荐）

1. 右键 `右键安装.inf` → **安装**
2. 打开「设置 → 辅助功能 → 鼠标指针与触控」（Win10：控制面板 → 鼠标 → 指针）
3. 方案选择 **NaiwaCursors** → 应用

> `.inf` 末尾有一条 HKLM RunOnce 记录，用于安装后自动打开鼠标属性，因此会触发一次管理员权限提示（UAC）。

### 方式 B：脚本安装

双击 `双击安装.bat`，或在 PowerShell 中执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-cursors.ps1
```

脚本只做三件事：把 `.cur` 复制到 `%LOCALAPPDATA%\Microsoft\Windows\Cursors\NaiwaCursors`、在 `HKCU\Control Panel\Cursors` 写入方案、刷新系统光标。不需要管理员权限。

### 恢复默认

鼠标属性 → 指针 → 方案改回「Windows 默认」即可。

## 状态对照

| # | 状态 | 文件 | Windows 角色 | 注册表键 | 热点 (256) |
|---|------|------|--------------|----------|-----------|
| 01 | 正常选择 | `normal_select.cur` | Normal select | Arrow | 18,18 |
| 02 | 文本选择 | `text_select.cur` | Text select | IBeam | 128,128 |
| 03 | 链接选择 | `link_select.cur` | Link select | Hand | 18,18 |
| 04 | 后台运行 | `working_in_background.cur` | Working in background | AppStarting | 77,130 |
| 05 | 垂直调整 | `vertical_resize.cur` | Vertical resize | SizeNS | 128,128 |
| 06 | 水平调整 | `horizontal_resize.cur` | Horizontal resize | SizeWE | 128,128 |
| 07 | 斜向调整 1 | `diagonal_resize_nwse.cur` | Diagonal resize 1 | SizeNWSE | 128,128 |
| 08 | 斜向调整 2 | `diagonal_resize_nesw.cur` | Diagonal resize 2 | SizeNESW | 128,128 |
| 09 | 移动 | `move.cur` | Move | SizeAll | 128,128 |
| 10 | 帮助选择 | `help_select.cur` | Help select | Help | 18,18 |
| 11 | 不可用 | `unavailable.cur` | Unavailable | No | 126,123 |
| 12 | 忙碌 | `busy.cur` | Busy | Wait | 75,138 |
| 13 | 候选选择 | `alternate_select.cur` | Alternative select | UpArrow | 128,18 |
| 14 | 精确选择 | `precision_select.cur` | Precision select | Crosshair | 128,128 |
| 15 | 手写 | `handwriting.cur` | Pen | NWPen | 18,18 |
| 16 | 位置选择 | `location_select.cur` | Location select | Pin | 125,238 |
| 17 | 个人选择 | `person_select.cur` | Person select | Person | 128,128 |

另见 `状态映射表.csv`（可直接用 Excel 打开）。

## 目录结构

```
.
├─ *.cur                    可安装光标（17 个）
├─ cursor_assets/masters/   1024px 透明底设计母版
├─ tools/build_cursors.py   从母版重建 .cur（可选）
├─ install-cursors.ps1      脚本安装
├─ 双击安装.bat             install-cursors.ps1 的快捷入口
├─ 右键安装.inf             INF 安装
├─ manifest.json            主题规格、状态命名、热点表
├─ 状态映射表.csv           逐状态对照表
├─ 总览.png                 17 状态总览（红色十字为热点）
└─ 使用说明.txt             安装与文件说明
```

## 二次修改

1. 修改 `cursor_assets/masters/*.png`（1024×1024，透明底）
2. 如需调整热点，编辑 `manifest.json` 中对应状态的 `hotspot_256`
3. 安装依赖并重建：

```bash
pip install -r tools/requirements.txt
python tools/build_cursors.py
```

脚本沿用原始生成规则：按 alpha 裁边 → 等比缩放到正方形 → 居中，热点按 `round(hotspot_256 * size / 256)` 缩放，并为每档白色图形补 1px 深色描边。

## 已知限制

- 部分浏览器、游戏和专业软件会自行绘制光标，不显示系统主题，属于软件自身机制
- `busy`、`working_in_background` 目前为静态光标
- 少量系统级界面（如登录界面）可能沿用默认光标

## 许可

- 代码（`.ps1` / `.bat` / `.inf` / `tools/`）：[MIT](LICENSE)
- 美术素材（`.cur` / `cursor_assets/masters/` / `总览.png`）：[CC BY 4.0](LICENSE-ART.md)

转载或再创作时请保留署名：**Naiwa Cursors by wdaaaa**。

---

## English

A 17-state frog cursor theme for Windows 10/11. Every `.cur` embeds five sizes (32/48/64/128/256) with white glyphs and dark outlines, readable on both light and dark backgrounds.

**Install**

- Right-click `右键安装.inf` → *Install* (UAC prompt expected), then choose **NaiwaCursors** in Settings → Accessibility → Mouse pointer.
- Or run `双击安装.bat` / `install-cursors.ps1`, which copies cursors to `%LOCALAPPDATA%` and writes the scheme to `HKCU` without admin rights.

**Rebuild**

```bash
pip install -r tools/requirements.txt
python tools/build_cursors.py
```

**License**

Code: MIT. Artwork: CC BY 4.0. Attribution: *Naiwa Cursors by wdaaaa*.