# Handwritten Solutions · 仿手写解题页

将「题目 + 授权笔迹样本 + 本次要求」组织成可复用的 Codex Skill 工作流：先解题与校核，再参照书写习惯制作 PNG 或 PDF。

仓库：[Artoria-learnning/homework-breaker](https://github.com/Artoria-learnning/homework-breaker)。

**当前为实验性工作流。** 它不是独立网站，不包含训练好的个人笔迹模型，也不保证字迹完全一致或作业满分。图像生成仍可能改动公式，必须检查成品。

## 功能

- 识别题号和小问，整理规范步骤，回代或独立计算校验关键结果。
- 参照用户自己的字形、间距、笔画和图形习惯制作页面。
- 保存经授权的本地个人档案，后续复用样本，无需每次重发。
- 按要求设置页眉、圈号、纸张及输出格式；支持只修改已有页码。
- 提供图片按顺序拼成A4 PDF的脚本，等比缩放、不裁切、拒绝覆盖已有文件。

## 使用条件

需要支持 Skill 的 Codex 环境，以及可用的图像生成/编辑工具。克隆仓库不会自动获得模型、图像工具或调用额度；不同账号和宿主环境可能有差异。

PDF拼页脚本需要 Python 3.10+ 和 `requirements.txt` 中的依赖；只阅读Skill不需要安装Python依赖。数学与视觉复核仍由运行Skill的模型、工具和使用者完成。

## 安装与使用

### 在本仓库中使用

将仓库克隆或下载到本地，在 Codex 中打开该目录。Skill位于 `.agents/skills/handwritten-solutions/`。Codex按项目目录发现Skill，具体入口以[官方说明](https://learn.chatgpt.com/docs/build-skills)及当前客户端为准。

```sh
git clone https://github.com/Artoria-learnning/homework-breaker.git
cd homework-breaker
```

附上题目和本人手写样本，然后输入：

```text
使用 $handwritten-solutions，完成附件圈出的题目。
参照我上传的笔迹与书写习惯；页眉按本次提供的信息填写；
圈号从12开始；输出三张PNG图片。先核算解答，再生成并检查成品。
```

仅修改页码：

```text
使用 $handwritten-solutions，把这三张图片右上角圈号改为12、13、14。
保留正文、公式、图形及原有划改，交付三张图片。
```

输出PDF：

```text
使用 $handwritten-solutions，复用我已保存的本地笔迹档案，完成附件题目。
页眉留空，输出A4 PDF，包含关键计算步骤。
```

若列表中没有出现Skill，可让Codex读取本仓库的 `.agents/skills/handwritten-solutions/SKILL.md`。也可将该Skill文件夹复制到自己项目的 `.agents/skills/` 下；不要覆盖已有同名技能。

### 本地安装PDF脚本依赖（可选）

```text
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .agents/skills/handwritten-solutions/scripts/pack_pages.py --output output/solutions.pdf page1.png page2.png
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS / Linux：

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python .agents/skills/handwritten-solutions/scripts/pack_pages.py --output output/solutions.pdf page1.png page2.png
.venv/bin/python -m unittest discover -s tests -v
```

拼页脚本只合并已生成图片，不负责识题、解题或生成笔迹。跨环境安装尚未完整验证；本地验证记录见下文。

## 笔迹档案

公共仓库不包含任何人的真实样本、姓名或学号。首次使用请提供自己的授权样本；样本保存在本地 `private/`，该目录默认不提交。参考Skill中的 `references/style-profile.md` 建档。复用的是图片和习惯，**不是在聊天中自动训练模型**。

可以指定自然的书写不齐和手绘线条；划改痕迹需明确提出，且不能掩盖错误答案或被描述成真实解题历史。

## 当前限制与验证

- 笔迹相似度仍有待不同用户实测，手写数学符号及复杂图形可能失败。
- 结构、数值和最终图像都需复核；不能以重复询问模型代替独立校验。
- 已有原型完成过解题图片及PDF制作；目前公开包验证范围为Skill格式、资源引用和PDF脚本功能。
- 未包含多用户服务、账号系统、自动评分、专用训练模型或真实用户规模测试。

## 许可

本仓库代码与说明采用MIT许可，见 `LICENSE`。模型服务、用户样本、题目和第三方资源分别遵循各自的授权条件。
