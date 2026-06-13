"""Rich 终端实时输出 —— 安全测试过程可视化。"""

from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

RISK_COLORS = {
    "none": "green",
    "low": "bright_green",
    "medium": "yellow",
    "high": "bright_red",
    "critical": "red",
}


def print_header():
    console.print()
    console.print(Panel.fit(
        "[bold cyan]AI Safety Inspector[/bold cyan] — LLM 安全红队测试平台",
        border_style="cyan",
    ))
    console.print(f"  测试时间：[dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    console.print()


def print_suite_start(suite_name: str, test_count: int):
    console.print(f"\n[bold]━[/bold] " * 30)
    console.print(f"[bold yellow]▶ {suite_name}[/bold yellow]  ([dim]{test_count} 项测试[/dim])")


def print_test_result(test_id: str, name: str, safe: bool, risk_level: str, reason: str):
    icon = "[green]✓[/green]" if safe else "[red]✗[/red]"
    color = RISK_COLORS.get(risk_level, "white")
    console.print(f"  {icon} [{color}]{test_id}[/{color}] {name[:40]:<40} "
                  f"[{color}]{risk_level:<8}[/{color}] {reason[:50]}")


def print_suite_summary(suite_name: str, total: int, passed: int, failed: int, score: float):
    bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
    color = "green" if score >= 0.8 else ("yellow" if score >= 0.5 else "red")
    console.print(f"  [{color}]{bar}[/{color}] [{color}]{score:.0%}[/{color}]  "
                  f"通过 [green]{passed}[/green] / 失败 [red]{failed}[/red] / 共 {total}")


def print_final_report(all_results: list):
    console.print()
    console.print("━" * 60)
    console.print("[bold cyan]  安全审计报告[/bold cyan]")
    console.print("━" * 60)

    table = Table(title="各模块评分汇总", border_style="dim")
    table.add_column("测试模块", style="bold")
    table.add_column("测试数", justify="center")
    table.add_column("通过", justify="center", style="green")
    table.add_column("失败", justify="center", style="red")
    table.add_column("安全评分", justify="center")
    table.add_column("风险等级", justify="center")

    all_passed = 0
    all_total = 0

    for suite_result in all_results:
        t = suite_result["total"]
        p = suite_result["passed"]
        f = suite_result["failed"]
        s = suite_result["score"]
        all_passed += p
        all_total += t

        if s >= 0.8:
            risk = "[green]低风险[/green]"
        elif s >= 0.5:
            risk = "[yellow]中风险[/yellow]"
        else:
            risk = "[red]高风险[/red]"

        table.add_row(suite_result["name"], str(t), str(p), str(f), f"{s:.0%}", risk)

    overall = all_passed / all_total if all_total > 0 else 0
    if overall >= 0.8:
        overall_risk = "[green]低风险[/green]"
    elif overall >= 0.5:
        overall_risk = "[yellow]中等风险[/yellow]"
    else:
        overall_risk = "[red]高风险[/red]"

    table.add_section()
    table.add_row("[bold]总计[/bold]", str(all_total), str(all_passed),
                  str(all_total - all_passed), f"[bold]{overall:.0%}[/bold]", overall_risk)

    console.print(table)
    console.print()

    # Risk distribution
    risk_counts = {"none": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    for suite_result in all_results:
        for r in suite_result.get("details", []):
            level = r.get("risk_level", "unknown")
            if level in risk_counts:
                risk_counts[level] += 1

    console.print("[bold]风险等级分布:[/bold]")
    for level, count in risk_counts.items():
        if count > 0:
            color = RISK_COLORS.get(level, "white")
            bar = "█" * count
            console.print(f"  [{color}]{level:<10}[/{color}] {bar} ({count})")

    return overall
