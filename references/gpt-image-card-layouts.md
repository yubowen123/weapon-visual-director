# GPT Image 2 武器介绍卡

## 默认：博物馆档案卡

- 画幅：竖版 3:4
- 背景：暖黑、炭灰、象牙白或档案纸
- 主武器：完整入画，占画布约 58–66%
- 角度：正侧或轻微三分之四侧视，避免透视缩短掩盖结构
- 细节窗：固定 3 个，分别展示攻击端、关键连接/纹样、握柄/尾部
- 标注线：细、克制、不得穿过标题或简介
- 文字：标题、副标题、3 个局部标签、1 段简介；不添加其他文字

适用于历史、写实、考据感和电影道具。

## 兵工档案卡

- 画幅：横版 4:3 或竖版 3:4
- 背景：冷灰金属、蓝黑技术纸、低饱和网格
- 主武器：完整侧视，结构优先
- 细节窗：连接机构、握持区、表面标识
- 装饰：少量编号框和分区线，但禁止模型自行生成数据

适用于近现代或工业风视觉；不得出现未经用户提供的性能参数。

## 科幻遗物卡

- 画幅：竖版 3:4
- 背景：深色档案界面或考古扫描台
- 主武器：完整视图 + 低强度轮廓辉光
- 细节窗：能量/材料节点、铭刻、接口
- 装饰：克制的界面线；不得使用随机乱码

适用于架空和科幻武器。所有名称与标签必须提前写定。

## 文案限制

- 中文标题：1–8 个字符
- 中文副标题：1–12 个字符
- 局部标签：恰好 3 个，每个 1–8 个字符
- 中文简介：建议 30–60 个字符，最多 80 个字符
- 英文标题：最多 5 个单词
- 英文局部标签：每个最多 4 个单词

避免生僻字、超长专名和密集段落。文字越重要，越应减少总量。

## 固定提示词骨架

```text
Create a vertical 3:4 museum-grade weapon introduction card using the uploaded image as the primary structural reference.

Preserve {structural locks}. Transform {narrative changes}.

Layout:
- Place one complete {view} of the weapon in the center, occupying about {58-66}% of the card.
- Add three detail panels showing {detail 1}, {detail 2}, and {detail 3}.
- Connect each panel with a thin annotation line.
- Use {background, typography, accent color, lighting}.

Render the following text exactly:
Title: "{title}"
Subtitle: "{subtitle}"
Detail label 1: "{label 1}"
Detail label 2: "{label 2}"
Detail label 3: "{label 3}"
Description: "{description}"

Keep all text correctly spelled and clearly separated. Do not add any other text, numbers, logos or watermarks. One weapon only. {remaining constraints}
```

## 卡片文案写法

标题命名：`身份/命题 + 可见特征`，如“守陵烟刃”。

副标题：`时代/世界 + 武器身份`，如“明末·守墓人佩刀”。

局部标签：只命名能在细节窗中看到的东西，例如“烟蚀钢刃”“镇魂铭纹”“旧绯缠柄”。

简介：一句说明谁使用、为何存在、最重要的可见历史痕迹。不要写性能数值、制造参数或无法证实的考据。

