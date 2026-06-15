# AI Safety Inspector

LLM 安全红队测试平台 —— 自动化 AI 模型安全审计工具。

[![CI](https://github.com/sophie20260601/ai_safety_inspector/actions/workflows/ci.yml/badge.svg)](https://github.com/sophie20260601/ai_safety_inspector/actions)

## 功能

基于 **LLM-as-Judge** 架构，对 AI 模型进行 5 个维度的自动化安全审计：

| 模块 | 测试数 | 说明 |
|------|--------|------|
| 越狱攻击防御 | 10 | DAN 模式、前缀注入、情感操纵等 |
| 提示注入防御 | 8 | 分隔符注入、JSON 注入、系统指令泄露等 |
| 有害内容拒绝 | 8 | 武器、毒品、自残、欺诈等 |
| 幻觉抵抗 | 8 | 编造事实、虚假引用等 |
| 偏见检测 | 6 | 性别/年龄/地域等系统性偏见（配对比较） |

每个攻击 case 输出 `safe` / `risk_level` / `reason` 三维判定，最终生成 Markdown 安全审计报告。

## 快速开始

```bash
git clone https://github.com/sophie20260601/ai_safety_inspector.git
cd ai_safety_inspector
pip install -r requirements.txt
cp .env.example .env   # 编辑 .env 填入 DEEPSEEK_API_KEY
python run.py
```

## CI/CD

- **Push 自动触发**：pytest 结构验证（无需 API Key）
- **手动触发**：[Actions 页面](https://github.com/sophie20260601/ai_safety_inspector/actions) → Run workflow → 勾选 Run full safety audit → 运行全量安全审计，报告自动归档

## 技术栈

Python · OpenAI SDK · DeepSeek API · Pydantic Settings · Tenacity · GitHub Actions
