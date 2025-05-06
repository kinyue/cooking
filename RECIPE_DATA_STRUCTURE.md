# 菜谱数据结构

本文档描述了菜谱及其相关数据在应用中的存储和使用结构，以表格形式呈现。

## `recipes` 表结构

| 字段名             | 类型/描述             | 说明                                                                 |
| :----------------- | :-------------------- | :------------------------------------------------------------------- |
| `id`               | INTEGER PRIMARY KEY   | 菜谱的唯一标识符                                                     |
| `name`             | TEXT NOT NULL         | 菜谱名称                                                             |
| `description`      | TEXT                  | 菜谱描述                                                             |
| `ingredients`      | TEXT (JSON 字符串)    | 食材列表，存储为 JSON 字符串，应用中解析为对象数组 `[{name, quantity, unit}, ...]` |
| `instructions`     | TEXT (JSON 字符串)    | 步骤列表，存储为 JSON 字符串，应用中解析为字符串数组 `["步骤 1", "步骤 2", ...]` |
| `image_url`        | TEXT                  | 外部图片 URL，如果图片存储在 `recipe_images` 表中，此字段可能为 NULL |
| `tags`             | TEXT (JSON 字符串)    | 标签列表，存储为 JSON 字符串，应用中解析为字符串数组 `["标签1", "标签2"]`    |
| `difficulty`       | TEXT                  | 难度级别，如 "简单", "中等", "困难"                                  |
| `cuisine`          | TEXT                  | 菜系，如 "川菜", "粤菜"                                              |
| `prep_time_minutes`| INTEGER               | 准备时间（分钟）                                                     |
| `cook_time_minutes`| INTEGER               | 烹饪时间（分钟）                                                     |
| `servings`         | INTEGER               | 份量                                                                 |
| `created_at`       | TIMESTAMP             | 菜谱创建时间                                                         |
| `updated_at`       | TIMESTAMP             | 菜谱最后更新时间                                                     |

## `recipe_images` 表结构

| 字段名        | 类型/描述           | 说明                                   |
| :------------ | :------------------ | :------------------------------------- |
| `id`          | INTEGER PRIMARY KEY | 图片记录的唯一标识符                   |
| `recipe_id`   | INTEGER NOT NULL    | 关联的菜谱 ID，外键关联 `recipes` 表 |
| `image_data`  | BLOB NOT NULL       | 图片的二进制数据                       |
| `alt_text`    | TEXT                | 图片的替代文本                         |
| `is_primary`  | INTEGER (0 或 1)    | 是否是菜谱的主图 (0: 否, 1: 是)        |
| `uploaded_at` | TIMESTAMP           | 图片上传时间                           |
