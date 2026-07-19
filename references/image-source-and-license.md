# 图片来源与授权策略

## 来源优先级

### A 级：知识与图片主来源

1. Cleveland Museum of Art Open Access
   - JSON/CSV/API；大量图片提供 web、print、full 链接。
   - 仓库与开放图片以 CC0 为主，仍保留对象页和权利字段。
2. The Metropolitan Museum of Art Open Access
   - 数据集 CC0；只采用 `Is Public Domain = True` 且有 Primary Image 的对象图。
3. Smithsonian Open Access
   - 使用当前 API/AWS 数据入口；GitHub 旧仓库已归档。
   - 逐条检查媒体权利字段，不把元数据 CC0 自动等同于所有媒体 CC0。
4. Wikimedia Commons
   - 必须落到单个文件页，记录作者、许可证、署名要求和原文件 URL。
5. 其他博物馆开放 API
   - 只有在对象记录明确给出 Public Domain、CC0 或可复用 Creative Commons 许可时纳入。

### B 级：造型与轮廓补充

- KayKit 等明确 CC0 的 3D/2D 资产：适合轮廓和视角，不作为历史考据。
- Game Icons：适合类别与剪影；多数要求按作者署名，逐作者保留许可。

### C 级：检测与场景补充

- Open Images、OD-WeaponDetection 等：适合持握、遮挡、监控或检测任务。
- 训练集代码许可证、标注许可证、图片许可证必须分别记录。
- 不把低清监控帧作为高质量武器设计主参考。

## 不可作为开放图片主来源

- Pinterest、无来源图站、聚合下载站
- 游戏、影视、动漫截图和粉丝 Wiki 图
- 电商商品图、拍卖图、厂商宣传图，除非有明确复用许可
- 没有 LICENSE 的 GitHub 爬虫仓库或镜像数据
- “仓库代码 MIT”但图片来源未说明的训练项目

这些来源可以作为发现线索，但必须追溯原始来源和许可。

## 候选记录字段

```json
{
  "id": "W01",
  "title": "Sword",
  "image_url": "https://...",
  "thumbnail_url": "https://...",
  "landing_url": "https://...",
  "source": "Cleveland Museum of Art",
  "creator": "Unknown",
  "license": "CC0",
  "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
  "license_verified": true,
  "culture": "European",
  "date": "15th century",
  "materials": ["steel", "leather"],
  "tags": ["sword", "straight", "crossguard"],
  "match_reasons": ["轮廓匹配", "结构清晰"],
  "reference_strength": ["轮廓", "护手"]
}
```

`license_verified` 只有在本轮打开原始对象页或官方记录核验后才能设为 `true`。

## 检索策略

1. 组合中英文关键词：武器类型 + 文化/时代 + 结构 + `museum` / `open access`。
2. 先用图片搜索发现，再打开原始对象页。
3. 优先横向覆盖差异：轮廓、握柄、材质、年代，而不是返回同一物件的重复图。
4. 候选不足时扩大一个维度，不同时放宽所有条件。
5. 每轮最多 8 张；下一轮说明修改了哪个检索标签。

## 许可证表达

- `CC0 / Public Domain`：可作为优先最终参考，仍保留来源。
- `CC BY`：可使用，但必须保留作者、链接和署名要求。
- `CC BY-SA`：记录署名与相同方式共享要求；衍生发布前提示用户核验。
- `未核验`：仅用于选择讨论，不下载、不打包、不声称可商用。
- `All Rights Reserved / 未授权`：不作为本 Skill 的最终参考资产。

