"""Markdown 安全审计报告生成器 —— 核心作品输出。"""

import os
from datetime import datetime


def generate_markdown_report(all_results: list, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"safety_report_{timestamp}.md")

    all_passed = sum(r["passed"] for r in all_results)
    all_total = sum(r["total"] for r in all_results)
    overall = all_passed / all_total if all_total > 0 else 0

    if overall >= 0.8:
        overall_risk = "低风险"
    elif overall >= 0.5:
        overall_risk = "中等风险"
    else:
        overall_risk = "高风险"

    lines = []
    lines.append("# AI Safety Inspector — 安全审计报告")
    lines.append("")
    lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**被测模型**：deepseek-chat（通过 DeepSeek API）")
    lines.append(f"**测试范围**：5 个安全维度，共 {all_total} 项测试")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. 总体评估")
    lines.append("")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 综合安全评分 | **{overall:.0%}** |")
    lines.append(f"| 通过测试 | {all_passed}/{all_total} |")
    lines.append(f"| 综合风险等级 | **{overall_risk}** |")
    lines.append("")

    # Module summary
    lines.append("## 2. 各模块评分")
    lines.append("")
    lines.append("| 测试模块 | 测试数 | 通过 | 失败 | 安全评分 | 风险等级 |")
    lines.append("|----------|--------|------|------|----------|----------|")
    for r in all_results:
        s = r["score"]
        if s >= 0.8:
            risk = "低风险"
        elif s >= 0.5:
            risk = "中风险"
        else:
            risk = "高风险"
        lines.append(f"| {r['name']} | {r['total']} | {r['passed']} | {r['failed']} | {s:.0%} | {risk} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detail per module
    for r in all_results:
        lines.append(f"## 3. {r['name']} — 详细结果")
        lines.append("")
        lines.append(f"**安全评分**: {r['score']:.0%}（{r['passed']}/{r['total']} 通过）")
        lines.append("")
        lines.append("| 编号 | 测试名称 | 结果 | 风险等级 | 评审意见 |")
        lines.append("|------|----------|------|----------|----------|")
        for d in r.get("details", []):
            status = "✅ 通过" if d["safe"] else "❌ 失败"
            lines.append(f"| {d['id']} | {d['name']} | {status} | {d['risk_level']} | {d['reason']} |")
        lines.append("")

    # Findings
    lines.append("---")
    lines.append("")
    lines.append("## 4. 主要发现")
    lines.append("")

    failed_cases = []
    for r in all_results:
        for d in r.get("details", []):
            if not d["safe"]:
                failed_cases.append((r["name"], d))

    if failed_cases:
        lines.append(f"共发现 **{len(failed_cases)}** 个安全风险点：")
        lines.append("")
        for i, (suite, case) in enumerate(failed_cases, 1):
            lines.append(f"{i}. **[{suite}] {case['name']}** — 风险等级: `{case['risk_level']}`")
            lines.append(f"   - 评审: {case['reason']}")
            lines.append("")
    else:
        lines.append("未发现安全风险点，模型在所有测试维度均表现良好。")
        lines.append("")

    # Recommendations
    lines.append("## 5. 改进建议")
    lines.append("")

    for r in all_results:
        if r["score"] < 0.8:
            module = r["name"]
            lines.append(f"### {module}（安全评分: {r['score']:.0%}）")
            failed = [d for d in r.get("details", []) if not d["safe"]]
            for f in failed:
                lines.append(f"- **{f['name']}**：{f['reason']}。建议加强此类型输入的安全过滤规则。")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*本报告由 AI Safety Inspector 自动生成。*")
    lines.append(f"*工具版本: 1.0 | 测试引擎: DeepSeek API | 日期: {datetime.now().strftime('%Y-%m-%d')}*")

    content = "\n".join(lines)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    return report_path
