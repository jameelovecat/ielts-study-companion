# 数据约定

初始化生成 `workspace/config.json`。`material_roots` 为资料目录列表，相对路径以配置文件所在的工作区为基准；也支持绝对路径及 `~`。不递归跟随资料目录内的符号链接，以免越界索引。索引跳过隐藏文件和不支持格式，只记录路径、扩展名与大小，不识别题目内容。

`review_intervals_days` 默认 `[1, 2, 4, 7, 15, 30]`。新词条 `level` 为0、`due` 为次日。首次答对升到1级，按2天安排；答错回0级，次日重试。升至6级后视为已掌握，`due` 为 `null`；再次答错可重新进入复习。相同条目同日可多次练习，但升降级每天最多一次，避免重复提交导致跳级。

## 表达本格式

`表达本.json` 是表达复习的唯一数据来源，Markdown 用于学习记录和错题说明，不另存一份表达本。

```json
{
  "entries": [
    {
      "id": "expr-0001",
      "expression": "keep an open mind",
      "meaning": "保持开放的心态",
      "example": "I try to keep an open mind when learning something new.",
      "original_error": null,
      "source": "用户练习，或已核实的资料定位",
      "level": 0,
      "due": "2026-11-02"
    }
  ],
  "reviews": []
}
```

用户完成作答后，助手调用 `review ID --result correct` 或 `incorrect`。脚本追加复习历史，仅更改该条目的等级、复习日期与最近复习日，保留其他字段；写入通过临时文件原子替换。不要在多个终端同时修改同一表达本。

`due` 只输出ID、中文含义和日期，不输出英文答案；助手按ID读取完整词条后，一次提问一条。

## 示例数据

`examples/session.md` 完全虚构，不能算成使用者的实际成绩。此项目不包含自动答案抓取、自动音频识别或官方评分模型。
