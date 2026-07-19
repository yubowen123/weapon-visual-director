# 三模型提示词适配

三个平台共享同一设计事实，但使用不同表达方式。不得复制同一段文字后只改标题。

平台版本与参数可能变化。需要实际提交或付费生成前，以官方文档为准：

- Midjourney Image Prompts：https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts
- Midjourney Parameters：https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List
- GPT Image 2：https://developers.openai.com/api/docs/models/gpt-image-2
- OpenAI 图片提示：https://openai.com/academy/image-generation/
- Nano Banana Pro：https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image

## 共享输入

- 单一主参考图
- 可选次参考图及唯一职责
- 设计命题
- Preserve / Change / Avoid
- 输出用途、画幅、背景、构图、材质、光线
- 统一禁止项

## Midjourney

### 职责

用于造型探索、气质强化和一组视觉变体。图片参考影响内容、构图与色彩，但不是精确编辑器。

### 写法

1. Discord 形式把有效图片 URL 放在最前；Web 形式说明把选中图设为 Image Prompt。
2. 正文描述最终可见画面，不写 `change this`、`keep that` 式编辑清单。
3. 顺序：主体原型 → 剧情化外观 → 结构与材质 → 构图 → 灯光/背景 → 风格。
4. 参数放在末尾；默认 `--v 8.1 --raw`。
5. 主参考身份较强时建议 `--iw 1.2–2.0`；探索性更强时降低。
6. 单件资产默认 `--ar 3:2` 或 `--ar 4:3`；竖版介绍视觉可用 `--ar 3:4`。
7. `--s` 保持低到中等，避免风格吞没结构。只有用户需要时才加 `--hd` 或 `--q 4`。

### 模板

```text
[REFERENCE_IMAGE_URL]

A {credible derived weapon} preserving {visible prototype traits}, redesigned for {owner/context}, {visible narrative changes}, {materials and surface history}, {ornament discipline}, one complete weapon fully visible, {view and composition}, {lighting and background}, {visual medium} --v 8.1 --raw --iw {1.2-2.0} --ar {ratio} --s {value}
```

## Nano Banana Pro

### 职责

用于高保真图生图、复杂指令遵循和结构化局部修改。默认输出纯武器概念资产，不加说明文字。

### 写法

明确图片编号和职责，使用以下段落：

```text
Use Image 1 as the primary structural reference.

Preserve:
- ...

Change:
- ...

Composition:
- ...

Material and lighting:
- ...

Constraints:
- ...
```

要求：

- Preserve 写几何、比例和连接逻辑。
- Change 写视觉变化及其剧情原因。
- 明确 one weapon only、完整入画、背景、角度和细节可读性。
- 默认禁止文字、人物、手、血液、Logo、水印和随机装饰。
- 需要次参考时写 `Use Image 2 only for material/ornament; do not copy its silhouette.`

## GPT Image 2

### 职责

默认生成“武器介绍卡”：主武器视觉 + 3 个局部细节窗 + 精确短文案。也可在用户明确要求时生成纯概念图。

### 写法

1. 说明上传图是 primary structural reference。
2. 明确哪些部分必须保持，哪些需要变化。
3. 用自然语言描述画布、网格、占比、局部窗和标注线。
4. 所有图片内文字放入直引号，逐条列出，禁止模型补写。
5. 文字短、层级少；标题、标签和简介由 Skill 先写好。
6. 明确 `Do not add any other text, numbers, logos or watermarks.`

卡片布局与字数限制见 [gpt-image-card-layouts.md](gpt-image-card-layouts.md)。

## 统一禁止项

根据任务裁剪，默认包括：

```text
one weapon only; no extra weapons; no hands or characters; no blood or gore; no floating fragments; no random runes; no excessive spikes; no modern fasteners unless requested; no broken geometry; no contradictory blade edges; no logo; no watermark; no unintended text
```

## 输出差异检查

- MJ 是否是紧凑的最终画面描述并带正确尾部参数？
- Nano 是否清楚写出参考图职责和 Preserve/Change/Constraints？
- GPT Image 2 是否包含卡片网格、局部窗和精确短文案？
- 三者是否继承相同的结构锁定与剧情变化？
