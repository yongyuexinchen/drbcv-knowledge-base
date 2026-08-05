# Calculus 全量 LaTeX 修复

## 数学公式规范（严格遵守）
$(cat D:/DRBCV-Knowledge/Templates/数学公式规范.md)

## 任务
扫描 Concepts/ 下**所有 114 张卡片**，修正：
1. 双反斜杠 → 单反斜杠（`\\int`→`\int`、`\\frac`→`\frac`）
2. 表格内 `|x|` → `\lvert x\rvert`
3. 非表格内的 `|x|` 也统一改成 `\lvert x\rvert`（未来迁移表格更安全）
4. 缺失的 `\,dx` 间距补上
5. 缺失的 `\displaystyle` 在积分号前补上

## 执行方式
逐卡扫描、逐卡修正。只改 LaTeX 语法，不动文字内容。
每批完成后报告：修正了几张、每张修正了什么。

## 第一批：先做前 20 张
