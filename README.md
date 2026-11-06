# ins-layout

把普通照片排成 ins 风的版式。这是 126 套「排版效果库」的开源实现，目前完成 106 套。可以当 Claude Code Skill 用，也可以直接跑命令行。

![12 个排版示例](examples/gallery/gallery.jpg)

> 示例里的人物都是 AI 生成的虚构人物，不是真实照片。

## 致谢

版式设计来自抖音作者 **普渡众神花** 的「排版效果库 · The INS Layout Archive · 126 layouts for your photos」，原帖在这里：<https://www.douyin.com/note/7704661887081909540>。

这 126 套版式的视觉创意和第 15 页的建库规则都是原作者的成果。没有这份作品就没有这个项目，请去原帖支持作者。

本仓库不包含原作者的 15 张图片。所有版式都是看着参考图用代码重新写的，不是原作者的模板源文件。

## 本仓库的原创部分

以下内容由 [@yuanshengbo8-sketch](https://github.com/yuanshengbo8-sketch) 在原作基础上完成，原作里没有：

- **审美校准**：每张照片生成 4 张候选（A/B/C/D），不满意选 E 换一批，选择写进日志，下一轮候选会向你选的风格靠拢。
- **智能推荐**：给每套版式预先算好遮挡图，再结合人头位置、照片横竖和版式家族打分。推荐结果会避开人脸，保证风格不重复，并留一个对照位。
- **自动测量**：用 YuNet 找人头，用 MediaPipe 找脚的位置，渲染时自动使用，不用手填坐标。
- **成片画质**：裁切以人头为中心，文字和界面先按 2 倍渲染再缩小，放大看也清晰。
- **绿幕双生素材**：给场景图各做一张屏幕或地面涂成纯绿的版本，自动算出手机屏幕的四个角和前景抠图，让照片能真实地放进手机里，甜甜圈、眼镜这些前景还能压在照片上面。
- **遮挡下的屏幕定位**：逐条边拟合直线再求交点，手机屏幕被食物挡住一部分时也能贴准。
- **场景变体**：12 个场景各有 3 个版本，比如木桌、白大理石、绿丝绒。默认按照片内容选一个，所以不同的人用同一套版式也不容易撞图。文字颜色会跟着场景调整。

## 快速开始

需要 Python 3.12 和约 1.2GB 磁盘空间（主要是 Chromium 和依赖）。网络顺畅时，从下载到出第一张图大约 2 分钟。

没装 Git 也可以：在 GitHub 页面点 **Code → Download ZIP**，解压后进入文件夹，从 `python -m venv .venv` 这一步开始。

```bash
git clone https://github.com/yuanshengbo8-sketch/ins-layout.git
```

```bash
cd ins-layout
```

```bash
python -m venv .venv
```

Mac 上这一步要写 `python3 -m venv .venv`，因为系统没有 `python` 这个命令。提示找不到时，先从 [python.org](https://www.python.org/downloads/) 安装 Python 3.12。激活虚拟环境之后，后面的命令都能直接用 `python`。

激活虚拟环境。Windows PowerShell 用第一行，macOS 和 Linux 用第二行：

```powershell
.venv\Scripts\Activate.ps1
```

```bash
source .venv/bin/activate
```

安装依赖并检查环境：

```bash
pip install -r requirements.txt
```

```bash
playwright install chromium
```

```bash
python scripts/preflight.py
```

用自带的演示照片试一次。4 张候选和一张对比图会写到 `out/`：

```bash
python scripts/candidates.py --photo examples/photos/demo_01_park.jpg --auto --out out
```

换成你自己的照片时，把路径改掉就行。支持 JPG、PNG、WebP 和 iPhone 的 HEIC，手机原图的旋转方向会自动处理。

Linux 服务器还需要装系统库和中文字体：

```bash
sudo apt-get install -y libgl1 libglib2.0-0 libegl1 libgles2 fonts-noto-cjk fonts-noto-color-emoji
```

## 桌面窗口（Windows）

不想敲命令的话，运行一次下面这行，桌面上会多一个「ins排版台」图标：

```bash
powershell -ExecutionPolicy Bypass -File app/make_shortcut.ps1
```

双击图标打开窗口，把照片拖进去，每张照片是一道选择题：A、B、C、D 四个方案，E 换一批。每张图右上角可以全屏查看。全部选完点提交，成品保存到桌面的 `ins排版` 文件夹。你的选择会记下来，下一次的推荐会更合你的口味。

照片只在你的电脑上处理，不会上传，窗口关闭后程序留存的副本会自动清除。

## 常用命令

```bash
# 指定版式
python scripts/render.py --id 164 --photos me.jpg --out out

# 改文字
python scripts/render.py --id 164 --photos me.jpg --out out --text l1="今天也很好"

# 多张照片的版式，指定场景变体 1、2、3，输出 Instagram 4:5 尺寸
python scripts/render.py --id 038 --photos a.jpg b.jpg --variant 2 --size 1080x1350 --out out

# 只看推荐结果
python scripts/recommend.py me.jpg --n 4

# 查看完成进度
python scripts/status.py
```

每页都会输出 PNG、分层 SVG 和记录用料的 recipe JSON。

## 作为 Claude Code Skill 使用

把仓库克隆到 Skill 目录，再安装依赖：

```bash
git clone https://github.com/yuanshengbo8-sketch/ins-layout.git ~/.claude/skills/ins-layout
```

```bash
python3 -m pip install -r ~/.claude/skills/ins-layout/requirements.txt
```

```bash
python3 -m playwright install chromium
```

Windows 上把 `python3` 换成 `python`。然后直接对 Claude 说「帮我把这几张照片做成 ins 排版」就可以。

## 现状和限制

- **完成度**：126 套完成 106 套。没做的 20 套是 036 043 066 067 069 072 073 074 078 092 106 115 116 117 119 129 130 132 133 148。
- **系统**：Windows、macOS（Apple 芯片）和 Linux 都从全新安装实测通过，每次提交都会在 GitHub Actions 上自动重测。不同系统的字体不完全相同，文字观感可能和示例略有差别。
- **推荐**：默认审美只来自一个人的 4 次选择，只是一个起点，用得越多越准。自动推荐目前只考虑单图版式，多图版式要手动指定。
- **文案**：版式里的默认文字是英文占位，建议用 `--text` 换成你自己的。
- **素材**：场景图为了控制仓库体积转成了 WebP，绿幕原图没有放进来。

## 许可

代码和本仓库的素材使用 [MIT 许可](LICENSE)，第三方模型和原作版式的说明见 [NOTICE.md](NOTICE.md)。

原作者没有声明开源许可，MIT 只覆盖本仓库的内容，不代表原版式设计也按 MIT 授权。如果你是原作者并希望调整署名或内容，请开 issue，我们会尽快处理。

## English

ins-layout turns ordinary photos into Instagram-style layouts. It is an open-source re-implementation of 106 of the 126 layouts in *The INS Layout Archive* by 普渡众神花 ([original post](https://www.douyin.com/note/7704661887081909540)). The original pages are not included.

Added by this project: taste calibration with A/B/C/D candidates, a recommender that keeps faces clear, automatic head and feet measurement, head-centred cropping with supersampling, green-screen twins for perspective mapping and cut-outs, occlusion-tolerant screen fitting, and scene variants.

Run the Quick Start commands above. It works as a command-line tool and as a Claude Code Skill. Clean installs are tested on Windows, macOS (Apple silicon) and Linux on every push. Code is MIT licensed. See NOTICE.md for the original work and third-party models.
