#!/usr/bin/env python3
"""Build a conservative, auditable statistical decision packet.

This tool is a gate, not an automatic analyst: an absent design, data-quality,
or power assessment results in ``needs-confirmation`` or ``blocked`` rather
than a substitute method.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


REVIEW_CHOICES = ("confirmed", "unknown", "concern")
MIN_NORMALITY_DIAGNOSTIC_N = 8
MIN_RANK_GROUP_N = 5
MIN_SURVIVAL_EVENTS = 5


def load_table(path: Path, sheet: str | int | None) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, encoding="utf-8-sig")
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=int(sheet) if sheet and str(sheet).isdigit() else (sheet or 0))
    raise ValueError("Only CSV, XLSX, and XLS inputs are supported.")


def table_profile(frame: pd.DataFrame) -> dict:
    numeric = [str(c) for c in frame if pd.api.types.is_numeric_dtype(frame[c])]
    categorical = [str(c) for c in frame if not pd.api.types.is_numeric_dtype(frame[c])]
    column_names = " ".join(str(c).casefold() for c in frame.columns)
    return {
        "rows": int(len(frame)), "numeric_columns": numeric, "categorical_columns": categorical,
        "missing_by_column": {str(c): int(frame[c].isna().sum()) for c in frame if frame[c].isna().any()},
        "duplicate_rows": int(frame.duplicated().sum()),
        "has_subject_id_hint": bool(re.search(r"subject|participant|patient|sample.?id|受试|个体|样本.*id", column_names)),
        "has_survival_hint": bool(re.search(r"event|status|censor|事件|结局", column_names) and re.search(r"time|duration|日期|时间", column_names)),
    }


def need_confirmation(args: argparse.Namespace) -> list[str]:
    missing = []
    if args.intent == "unspecified":
        missing.append("研究目的：描述、比较、关联、预测、聚类、生存或功效")
    if args.outcome == "unspecified":
        missing.append("结果变量类型：连续、等级、二元或生存时间")
    if args.intent == "compare" and args.design == "unspecified":
        missing.append("研究设计：独立组、配对或重复测量")
    if args.intent == "compare" and not args.value_column:
        missing.append("待比较的结果列")
    if args.intent == "compare" and not args.group_column:
        missing.append("分组列")
    return missing


def review_missing(args: argparse.Namespace, *, need_power: bool) -> list[str]:
    checks = [
        (args.experimental_unit, "实验单位（不是记录行或技术重复）"),
        (args.independence_review, "独立性审查结果"),
        (args.missingness_review, "缺失数据机制与处理审查结果"),
        (args.outlier_review, "异常值/录入错误审查结果"),
    ]
    missing = [label for value, label in checks if not value or value == "unknown"]
    concerns = [label for value, label in checks if value == "concern"]
    if concerns:
        missing.append("以下审查存在问题，不能自动推荐：" + "、".join(concerns))
    if need_power:
        if args.minimum_effect_size is None:
            missing.append("最小有科学意义的标准化效应量（Cohen d 或 ANOVA 的 Cohen f）")
        if args.target_power is None:
            missing.append("目标功效（通常预先指定，如 0.80 或 0.90）")
    return missing


def group_diagnostics(frame: pd.DataFrame, value: str, group: str, alpha: float) -> dict:
    subset = frame[[value, group]].replace([np.inf, -np.inf], np.nan).dropna()
    groups = {str(name): values[value].to_numpy(dtype=float) for name, values in subset.groupby(group, observed=True)}
    sizes = {name: int(len(values)) for name, values in groups.items()}
    normality, normality_reliable = {}, True
    for name, values in groups.items():
        n = len(values)
        if n < MIN_NORMALITY_DIAGNOSTIC_N or n > 5000:
            normality[name] = {"status": "sample-limited", "n": n}
            normality_reliable = False
        elif np.ptp(values) == 0:
            normality[name] = {"status": "zero-variance", "n": n}
            normality_reliable = False
        else:
            _, p_value = stats.shapiro(values)
            normality[name] = {"status": "pass" if p_value > alpha else "fail", "p": round(float(p_value), 6), "n": n}
    variance = {"status": "not-testable"}
    if len(groups) >= 2 and all(len(values) >= 2 and np.ptp(values) > 0 for values in groups.values()):
        _, p_value = stats.levene(*groups.values(), center="median")
        variance = {"status": "pass" if p_value > alpha else "fail", "p": round(float(p_value), 6)}
    return {
        "rows_used": int(len(subset)), "rows_excluded": int(len(frame) - len(subset)), "groups": sizes,
        "normality": normality, "normality_reliable": normality_reliable,
        "variance_homogeneity": variance,
    }


def two_sample_power(n1: int, n2: int, effect_size: float, alpha: float) -> float:
    """Two-sided noncentral-t power for a planned standardized mean difference."""
    df = n1 + n2 - 2
    critical = stats.t.ppf(1 - alpha / 2, df)
    ncp = effect_size / np.sqrt(1 / n1 + 1 / n2)
    return float(stats.nct.cdf(-critical, df, ncp) + stats.nct.sf(critical, df, ncp))


def anova_power(total_n: int, group_count: int, effect_size: float, alpha: float) -> float:
    dfn, dfd = group_count - 1, total_n - group_count
    critical = stats.f.ppf(1 - alpha, dfn, dfd)
    return float(stats.ncf.sf(critical, dfn, dfd, total_n * effect_size**2))


def paired_power(n: int, effect_size: float, alpha: float) -> float:
    critical = stats.t.ppf(1 - alpha / 2, n - 1)
    ncp = effect_size * np.sqrt(n)
    return float(stats.nct.cdf(-critical, n - 1, ncp) + stats.nct.sf(critical, n - 1, ncp))


def correlation_power(n: int, correlation: float, alpha: float) -> float:
    if n <= 3 or not 0 < abs(correlation) < 1:
        return 0.0
    critical = stats.norm.ppf(1 - alpha / 2)
    mean = np.sqrt(n - 3) * np.arctanh(abs(correlation))
    return float(stats.norm.cdf(-critical - mean) + stats.norm.sf(critical - mean))


def two_proportion_power(n1: int, n2: int, p1: float, p2: float, alpha: float) -> float:
    pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    null_se = np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    alternative_se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    critical = stats.norm.ppf(1 - alpha / 2) * null_se
    delta = abs(p2 - p1)
    return float(stats.norm.cdf((-critical - delta) / alternative_se) + stats.norm.sf((critical - delta) / alternative_se))


def normality_diagnostic(values: np.ndarray, alpha: float) -> dict:
    n = len(values)
    if n < MIN_NORMALITY_DIAGNOSTIC_N or n > 5000:
        return {"status": "sample-limited", "n": n}
    if np.ptp(values) == 0:
        return {"status": "zero-variance", "n": n}
    _, p_value = stats.shapiro(values)
    return {"status": "pass" if p_value > alpha else "fail", "p": round(float(p_value), 6), "n": n}


def review_result(args: argparse.Namespace, *, need_power: bool, labels: list[tuple[str, str]] | None = None) -> list[str]:
    missing = review_missing(args, need_power=need_power)
    for attribute, label in labels or []:
        value = getattr(args, attribute)
        if value == "unknown":
            missing.append(label)
        elif value == "concern":
            missing.append(f"{label}存在问题，不能自动推荐")
    return missing


def require_columns(frame: pd.DataFrame, columns: list[str | None]) -> str | None:
    absent = [column for column in columns if not column or column not in frame.columns]
    return None if not absent else "以下必需列缺失或未指定：" + "、".join(str(column) for column in absent)


def parse_columns(text: str | None) -> list[str]:
    return [value.strip() for value in (text or "").split(",") if value.strip()]


def binary_event_vector(series: pd.Series, event_value: str | None) -> tuple[np.ndarray | None, str | None]:
    """Validate an explicit binary encoding without guessing a noncanonical event."""
    values = series.dropna()
    unique = list(pd.unique(values))
    if len(unique) > 2:
        return None, "结果列包含两个以上取值，不能作为二元结果自动分析。"
    event = event_value
    if event is None:
        if set(unique) <= {0, 1, False, True}:
            event = "1"
        else:
            return None, "需要二元事件取值（--event-value）。"
    vector = (values.astype(str) == str(event)).to_numpy(dtype=int)
    if len(unique) < 2 or vector.sum() in {0, len(vector)}:
        return None, "二元结果没有同时出现事件与非事件，不能拟合或推荐回归模型。"
    return vector, None


def external_power_gate(args: argparse.Namespace) -> tuple[bool, str | None, dict | None]:
    """Require an externally validated power analysis when no safe local formula exists."""
    if args.power_assessment != "confirmed":
        return False, "需要外部功效分析记录（--power-assessment confirmed）", None
    if args.achieved_power is None or not 0 < args.achieved_power < 1:
        return False, "需要有效的外部已达功效（--achieved-power）", None
    if args.target_power is None or not 0 < args.target_power < 1:
        return False, "需要有效的目标功效", None
    result = {"achieved_power": args.achieved_power, "target_power": args.target_power, "basis": "externally validated method-specific power analysis"}
    if args.achieved_power < args.target_power:
        return False, "外部功效分析低于目标功效", result
    return True, None, result


def power_gate(diagnostic: dict, args: argparse.Namespace) -> tuple[bool, dict | None, str | None]:
    sizes = list(diagnostic["groups"].values())
    if args.minimum_effect_size is None or args.target_power is None:
        return False, None, "功效输入缺失"
    if not 0 < args.target_power < 1 or args.minimum_effect_size <= 0:
        return False, None, "目标功效必须在 (0, 1) 内，效应量必须为正数"
    if len(sizes) == 2:
        achieved = two_sample_power(sizes[0], sizes[1], args.minimum_effect_size, args.alpha)
        basis = "two-sided noncentral t approximation"
    else:
        achieved = anova_power(sum(sizes), len(sizes), args.minimum_effect_size, args.alpha)
        basis = "one-way ANOVA noncentral F approximation"
    result = {
        "minimum_effect_size": args.minimum_effect_size, "target_power": args.target_power,
        "achieved_power": round(achieved, 6), "basis": basis,
    }
    if achieved < args.target_power:
        return False, result, "按声明的最小有意义效应量计算，当前样本功效不足"
    return True, result, None


def decide_compare(frame: pd.DataFrame, args: argparse.Namespace, profile: dict) -> dict:
    if args.design == "paired":
        return decide_paired(frame, args)
    if args.design == "repeated":
        return decide_repeated(frame, args)
    if args.design != "independent":
        return {"status": "needs-confirmation", "missing": ["需要声明独立、配对或重复测量设计。"], "recommendations": []}
    if len(parse_columns(args.factor_columns)) >= 2:
        return decide_factorial_anova(frame, args)
    if args.value_column not in frame or args.group_column not in frame:
        return {"status": "blocked", "reasons": ["指定的结果列或分组列不存在。"], "recommendations": []}
    if not pd.api.types.is_numeric_dtype(frame[args.value_column]):
        return {"status": "blocked", "reasons": ["比较结果列必须是数值型。"], "recommendations": []}
    diagnostic = group_diagnostics(frame, args.value_column, args.group_column, args.alpha)
    group_count, minimum_n = len(diagnostic["groups"]), min(diagnostic["groups"].values(), default=0)
    if group_count < 2:
        return {"status": "blocked", "reasons": ["至少需要两个非空组。"], "diagnostics": diagnostic, "recommendations": []}
    if minimum_n < 3:
        return {"status": "blocked", "reasons": ["至少一组少于 3 条有效观测，无法支持自动推断推荐。"], "diagnostics": diagnostic, "recommendations": []}
    if args.outcome not in {"continuous", "ordinal"}:
        return {"status": "blocked", "reasons": ["结果变量类型与当前独立组适配器不匹配。"], "diagnostics": diagnostic, "recommendations": []}
    missing = review_missing(args, need_power=args.outcome == "continuous")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "diagnostics": diagnostic, "recommendations": []}
    if args.outcome == "ordinal":
        if minimum_n < MIN_RANK_GROUP_N:
            return {"status": "blocked", "reasons": [f"等级资料每组少于 {MIN_RANK_GROUP_N} 条；当前适配器不输出小样本秩检验推荐。"], "diagnostics": diagnostic, "recommendations": []}
        if args.rank_shape_review != "confirmed":
            return {"status": "needs-confirmation", "missing": ["等级/非正态比较的分布形状与 ties 审查结果"], "diagnostics": diagnostic, "recommendations": []}
        return {
            "status": "eligible", "recommendations": [{"method_id": "mann-whitney" if group_count == 2 else "kruskal-wallis", "evidence": "independent ordinal groups; design, quality, and rank-shape reviews confirmed"}],
            "diagnostics": diagnostic, "caution": "秩检验的解释限于预先声明的位置或分布问题；多组情形仍需预先指定事后比较与校正。",
        }
    power_ok, power, power_reason = power_gate(diagnostic, args)
    if not power_ok:
        return {"status": "blocked", "reasons": [power_reason or "功效门未通过"], "diagnostics": diagnostic, "power": power, "recommendations": []}
    normal_pass = diagnostic["normality_reliable"] and all(item["status"] == "pass" for item in diagnostic["normality"].values())
    if not normal_pass:
        return {
            "status": "needs-confirmation", "missing": [f"正态性诊断不足或未通过；当前自动适配器不以秩检验替代均值问题（最小组样本量 {minimum_n}）。"],
            "diagnostics": diagnostic, "power": power, "recommendations": [],
        }
    if group_count == 2:
        return {
            "status": "eligible", "recommendations": [{"method_id": "two-sample-t", "variant": "Welch", "evidence": "two independent continuous groups; reviewed data quality, normality diagnostic, and planned power gate pass"}],
            "diagnostics": diagnostic, "power": power,
        }
    if diagnostic["variance_homogeneity"]["status"] != "pass":
        return {
            "status": "eligible",
            "recommendations": [{"method_id": "one-way-anova", "variant": "Welch", "evidence": "three or more independent continuous groups; normality and power gates pass; unequal variances routed to Welch omnibus test"}],
            "diagnostics": diagnostic, "power": power,
            "caution": "Welch ANOVA does not justify pooled-variance post-hoc comparisons; use the qualified pairwise Welch + Holm artifact before annotating individual contrasts.",
        }
    return {
        "status": "eligible", "recommendations": [{"method_id": "one-way-anova", "evidence": "three or more independent continuous groups; reviewed data quality, normality, variance, and planned power gates pass"}],
        "diagnostics": diagnostic, "power": power,
    }


def decide_factorial_anova(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    factors = parse_columns(args.factor_columns)
    if len(factors) not in {2, 3}:
        return {"status": "blocked", "reasons": ["因子 ANOVA 仅支持恰好两个或三个预先指定因素。"], "recommendations": []}
    absent = require_columns(frame, [args.value_column, *factors])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    if args.outcome != "continuous" or not pd.api.types.is_numeric_dtype(frame[args.value_column]):
        return {"status": "blocked", "reasons": ["双/三因素 ANOVA 要求连续数值结果。"], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("factorial_balance_review", "因子单元完整性、平衡性及交互项预先指定审查结果"), ("residual_review", "因子模型残差、方差齐性与影响点审查结果")])
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.value_column, *factors]].replace([np.inf, -np.inf], np.nan).dropna()
    levels = [list(pd.unique(subset[factor])) for factor in factors]
    if any(len(values) < 2 for values in levels):
        return {"status": "blocked", "reasons": ["每个因素至少需要两个实际水平。"], "recommendations": []}
    cell_counts = subset.groupby(factors, observed=True).size()
    expected_cells = int(np.prod([len(values) for values in levels]))
    if len(cell_counts) != expected_cells:
        return {"status": "blocked", "reasons": ["存在空因子组合；不能估计完整主效应与交互项。"], "recommendations": []}
    if cell_counts.min() < 3:
        return {"status": "blocked", "reasons": ["至少一个因子组合少于 3 条有效观测。"], "diagnostics": {"cell_counts": {str(key): int(value) for key, value in cell_counts.items()}}, "recommendations": []}
    power_ok, reason, power = external_power_gate(args)
    if not power_ok:
        return {"status": "needs-confirmation", "missing": [reason or "因子 ANOVA 功效审查未通过"], "recommendations": []}
    method_id = "two-way-anova" if len(factors) == 2 else "three-way-anova"
    return {"status": "eligible", "recommendations": [{"method_id": method_id, "evidence": "complete factorial cells; reviewed interaction specification, residual assumptions, and external power gate"}], "diagnostics": {"factors": factors, "levels": {factor: int(len(values)) for factor, values in zip(factors, levels)}, "minimum_cell_n": int(cell_counts.min())}, "power": power}


def decide_paired(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    absent = require_columns(frame, [args.value_column, args.group_column, args.subject_column])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    if not pd.api.types.is_numeric_dtype(frame[args.value_column]):
        return {"status": "blocked", "reasons": ["配对结果列必须是数值型。"], "recommendations": []}
    missing = review_result(args, need_power=args.outcome == "continuous", labels=[("pairing_review", "受试者配对与条件映射审查结果")])
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.subject_column, args.group_column, args.value_column]].replace([np.inf, -np.inf], np.nan).dropna()
    if subset.duplicated([args.subject_column, args.group_column]).any():
        return {"status": "blocked", "reasons": ["同一受试者在同一条件下存在多条记录；请先声明聚合规则，不能自动伪重复。"], "recommendations": []}
    conditions = list(pd.unique(subset[args.group_column]))
    if len(conditions) != 2:
        return {"status": "blocked", "reasons": ["配对适配器要求恰好两个条件。"], "recommendations": []}
    wide = subset.pivot(index=args.subject_column, columns=args.group_column, values=args.value_column)
    if wide.isna().any(axis=None):
        return {"status": "blocked", "reasons": ["存在不完整配对；请在分析计划中预先处理缺失配对，不能静默丢弃。"], "recommendations": []}
    differences = (wide[conditions[1]] - wide[conditions[0]]).to_numpy(dtype=float)
    diagnostic = {"complete_pairs": int(len(wide)), "conditions": [str(value) for value in conditions], "difference_normality": normality_diagnostic(differences, args.alpha)}
    if len(wide) < 3:
        return {"status": "blocked", "reasons": ["完整配对少于 3 对。"], "diagnostics": diagnostic, "recommendations": []}
    if args.outcome == "ordinal":
        if len(wide) < MIN_RANK_GROUP_N:
            return {"status": "blocked", "reasons": [f"等级配对少于 {MIN_RANK_GROUP_N} 对。"], "diagnostics": diagnostic, "recommendations": []}
        if args.symmetry_review != "confirmed":
            return {"status": "needs-confirmation", "missing": ["配对差值对称性与零差/ties 审查结果"], "diagnostics": diagnostic, "recommendations": []}
        return {"status": "eligible", "recommendations": [{"method_id": "paired-wilcoxon", "evidence": "complete ordinal pairs; pairing, quality, and difference-symmetry reviews confirmed"}], "diagnostics": diagnostic}
    if args.outcome != "continuous":
        return {"status": "blocked", "reasons": ["当前配对适配器只支持连续或等级结果。"], "diagnostics": diagnostic, "recommendations": []}
    if diagnostic["difference_normality"]["status"] != "pass":
        return {"status": "needs-confirmation", "missing": ["配对差值的正态性诊断不足或未通过；不自动将均值问题替代为秩检验。"], "diagnostics": diagnostic, "recommendations": []}
    if args.minimum_effect_size is None or args.target_power is None or args.minimum_effect_size <= 0 or not 0 < args.target_power < 1:
        return {"status": "needs-confirmation", "missing": ["有效的配对 Cohen dz 与目标功效"], "diagnostics": diagnostic, "recommendations": []}
    achieved = paired_power(len(wide), args.minimum_effect_size, args.alpha)
    power = {"minimum_effect_size": args.minimum_effect_size, "target_power": args.target_power, "achieved_power": round(achieved, 6), "basis": "two-sided noncentral paired t"}
    if achieved < args.target_power:
        return {"status": "blocked", "reasons": ["按声明的最小有意义配对效应量计算，完整配对数的功效不足。"], "diagnostics": diagnostic, "power": power, "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "paired-t", "evidence": "complete continuous pairs; reviewed pairing, difference normality, and planned power gates pass"}], "diagnostics": diagnostic, "power": power}


def decide_repeated(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    absent = require_columns(frame, [args.value_column, args.group_column, args.subject_column])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("pairing_review", "受试者重复测量映射审查结果")])
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.subject_column, args.group_column, args.value_column]].replace([np.inf, -np.inf], np.nan).dropna()
    if subset.duplicated([args.subject_column, args.group_column]).any():
        return {"status": "blocked", "reasons": ["同一受试者/条件有重复记录；须预先定义聚合规则。"], "recommendations": []}
    wide = subset.pivot(index=args.subject_column, columns=args.group_column, values=args.value_column)
    if wide.shape[1] < 3:
        return {"status": "blocked", "reasons": ["重复测量适配器至少需要三个完整条件。"], "recommendations": []}
    if wide.isna().any(axis=None):
        return {"status": "blocked", "reasons": ["存在不完整重复测量；不能静默删行或填补。"], "recommendations": []}
    diagnostic = {"complete_subjects": int(len(wide)), "conditions": int(wide.shape[1])}
    if len(wide) < MIN_RANK_GROUP_N:
        return {"status": "blocked", "reasons": [f"完整受试者少于 {MIN_RANK_GROUP_N}；不推荐重复测量推断。"], "diagnostics": diagnostic, "recommendations": []}
    if args.outcome == "ordinal":
        return {"status": "eligible", "recommendations": [{"method_id": "friedman", "evidence": "three or more complete repeated ordinal conditions; pairing and data-quality reviews confirmed"}], "diagnostics": diagnostic}
    if args.outcome == "continuous":
        if args.sphericity_review != "confirmed":
            return {"status": "needs-confirmation", "missing": ["球形性审查或预先指定的校正方案；当前不自动推荐重复测量 ANOVA。"], "diagnostics": diagnostic, "recommendations": []}
        normality = {str(column): normality_diagnostic(wide[column].to_numpy(dtype=float), args.alpha) for column in wide.columns}
        diagnostic["condition_normality"] = normality
        if not all(item["status"] == "pass" for item in normality.values()):
            return {"status": "needs-confirmation", "missing": ["至少一个条件的正态性诊断不足或未通过；不自动把连续重复测量替代为等级检验。"], "diagnostics": diagnostic, "recommendations": []}
        power_ok, reason, power = external_power_gate(args)
        if not power_ok:
            return {"status": "needs-confirmation", "missing": [reason or "重复测量功效审查未通过"], "diagnostics": diagnostic, "power": power, "recommendations": []}
        return {"status": "eligible", "recommendations": [{"method_id": "one-way-repeated-anova", "evidence": "complete continuous repeated conditions; normality, sphericity/correction, and external method-specific power reviews confirmed"}], "diagnostics": diagnostic, "power": power}
    return {"status": "blocked", "reasons": ["当前重复测量适配器仅支持连续或等级结果。"], "diagnostics": diagnostic, "recommendations": []}


def parse_proportions(text: str | None) -> tuple[float, float] | None:
    if not text:
        return None
    try:
        values = tuple(float(value.strip()) for value in text.split(","))
    except ValueError:
        return None
    return values if len(values) == 2 and all(0 < value < 1 for value in values) else None


def decide_binary(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    absent = require_columns(frame, [args.value_column, args.group_column])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False)
    planned = parse_proportions(args.planned_proportions)
    if planned is None:
        missing.append("两个组的预先声明目标比例（--planned-proportions p1,p2）")
    if args.target_power is None:
        missing.append("目标功效")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.value_column, args.group_column]].dropna()
    groups = list(pd.unique(subset[args.group_column]))
    if len(groups) != 2:
        return {"status": "blocked", "reasons": ["双比例适配器要求恰好两个非空组。"], "recommendations": []}
    raw = subset[args.value_column]
    event = args.event_value
    if event is None:
        unique = set(raw.unique())
        if unique <= {0, 1, False, True}:
            event = 1
        else:
            return {"status": "needs-confirmation", "missing": ["二元事件取值（--event-value）"], "recommendations": []}
    outcomes = {group: subset.loc[subset[args.group_column] == group, args.value_column] for group in groups}
    if raw.astype(str).nunique() > 2:
        return {"status": "blocked", "reasons": ["结果列包含两个以上取值，不能作为二元结果自动分析。"], "recommendations": []}
    sizes = [len(outcomes[group]) for group in groups]
    successes = [int((outcomes[group].astype(str) == str(event)).sum()) for group in groups]
    expected = [value for count, size in zip(successes, sizes) for value in (count, size - count)]
    if min(expected) < 5:
        return {"status": "blocked", "reasons": ["至少一个组的观察到成功或失败数少于 5；普通双比例 z 检验不适用，当前不自动替代为精确检验。"], "diagnostics": {"groups": sizes, "successes": successes}, "recommendations": []}
    if not 0 < args.target_power < 1:
        return {"status": "blocked", "reasons": ["目标功效必须在 (0, 1) 内。"], "recommendations": []}
    achieved = two_proportion_power(sizes[0], sizes[1], planned[0], planned[1], args.alpha)
    power = {"planned_proportions": planned, "target_power": args.target_power, "achieved_power": round(achieved, 6), "basis": "two-sided normal approximation for difference in proportions"}
    if achieved < args.target_power:
        return {"status": "blocked", "reasons": ["按预先声明的目标比例计算，当前样本功效不足。"], "diagnostics": {"groups": sizes, "successes": successes}, "power": power, "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "two-sample-proportion", "evidence": "independent binary groups; expected counts, data-quality reviews, and planned power gate pass"}], "diagnostics": {"groups": sizes, "successes": successes, "event_value": event}, "power": power}


def decide_association(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    covariates = [value.strip() for value in (args.covariate_columns or "").split(",") if value.strip()]
    if covariates:
        return decide_partial_correlation(frame, args, covariates)
    absent = require_columns(frame, [args.value_column, args.predictor_column])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    if args.outcome != "continuous":
        return {"status": "blocked", "reasons": ["当前关联适配器仅支持两个连续变量的 Pearson 相关。"], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("linearity_review", "线性关系、异常值与影响点审查结果")])
    if args.minimum_effect_size is None or args.target_power is None:
        missing.append("最小有意义相关系数绝对值与目标功效")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.value_column, args.predictor_column]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(subset) < MIN_NORMALITY_DIAGNOSTIC_N or subset.nunique().min() < 2:
        return {"status": "blocked", "reasons": ["有效观测少于 8 或至少一个变量无变异。"], "recommendations": []}
    effect = abs(args.minimum_effect_size)
    if not 0 < effect < 1 or not 0 < args.target_power < 1:
        return {"status": "blocked", "reasons": ["相关效应量必须在 (0,1) 内，目标功效必须在 (0,1) 内。"], "recommendations": []}
    achieved = correlation_power(len(subset), effect, args.alpha)
    power = {"minimum_abs_correlation": effect, "target_power": args.target_power, "achieved_power": round(achieved, 6), "basis": "Fisher-z normal approximation"}
    if achieved < args.target_power:
        return {"status": "blocked", "reasons": ["按声明的最小有意义相关计算，样本功效不足。"], "power": power, "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "pearson-correlation", "evidence": "two continuous variables; reviewed linearity/outliers and planned correlation-power gate pass"}], "diagnostics": {"rows_used": int(len(subset)), "x": args.predictor_column, "y": args.value_column}, "power": power}


def decide_partial_correlation(frame: pd.DataFrame, args: argparse.Namespace, covariates: list[str]) -> dict:
    absent = require_columns(frame, [args.value_column, args.predictor_column, *covariates])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("linearity_review", "线性、异常值与影响点审查结果"), ("model_specification_review", "协变量选择和因果/测量时序审查结果")])
    if args.minimum_rows_per_feature is None:
        missing.append("预先声明的每控制变量最低有效样本数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    columns = [args.value_column, args.predictor_column, *covariates]
    subset = frame[columns].replace([np.inf, -np.inf], np.nan).dropna()
    if args.minimum_rows_per_feature <= 0 or len(subset) < args.minimum_rows_per_feature * (len(covariates) + 2):
        return {"status": "blocked", "reasons": ["有效样本量低于用户声明的偏相关资格门槛。"], "recommendations": []}
    if any(not pd.api.types.is_numeric_dtype(subset[column]) or subset[column].nunique() < 2 for column in columns):
        return {"status": "blocked", "reasons": ["偏相关涉及的结果、暴露和控制变量必须均为有变异的数值变量。"], "recommendations": []}
    power_ok, reason, power = external_power_gate(args)
    if not power_ok:
        return {"status": "needs-confirmation", "missing": [reason or "偏相关功效审查未通过"], "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "partial-correlation", "evidence": "predeclared numeric controls; reviewed specification/linearity and external power gates pass"}], "diagnostics": {"rows_used": int(len(subset)), "controls": covariates}, "power": power}


def decide_regression(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    predictors = [value.strip() for value in (args.predictor_columns or "").split(",") if value.strip()]
    absent = require_columns(frame, [args.value_column, *predictors]) if predictors else "需要 --predictor-columns"
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    if args.outcome != "continuous":
        return {"status": "blocked", "reasons": ["当前回归推断适配器仅支持连续结果；二元/生存回归须使用相应模型适配器。"], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("linearity_review", "线性和影响点审查结果"), ("residual_review", "残差正态性/异方差/独立性诊断审查结果"), ("model_specification_review", "预先指定的变量、交互项与模型选择审查结果")])
    if args.minimum_rows_per_feature is None:
        missing.append("预先声明的每模型参数最低有效样本数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.value_column, *predictors]].replace([np.inf, -np.inf], np.nan).dropna()
    parameter_count = len(predictors) + 1
    if args.minimum_rows_per_feature <= 0 or len(subset) < args.minimum_rows_per_feature * parameter_count:
        return {"status": "blocked", "reasons": ["有效样本量低于用户声明的回归资格门槛。"], "recommendations": []}
    if any(not pd.api.types.is_numeric_dtype(subset[column]) or subset[column].nunique() < 2 for column in subset.columns):
        return {"status": "blocked", "reasons": ["回归结果和预测变量必须均为有变异的数值变量；分类变量须先声明编码方案。"], "recommendations": []}
    power_ok, reason, power = external_power_gate(args)
    if not power_ok:
        return {"status": "needs-confirmation", "missing": [reason or "回归功效审查未通过"], "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "multiple-linear-regression", "evidence": "predeclared continuous regression with reviewed specification, residual diagnostics, and external power gate"}], "diagnostics": {"rows_used": int(len(subset)), "predictors": predictors, "parameters": parameter_count}, "power": power}


def regression_inputs(frame: pd.DataFrame, args: argparse.Namespace) -> tuple[pd.DataFrame | None, list[str], dict | None]:
    predictors = parse_columns(args.predictor_columns)
    absent = require_columns(frame, [args.value_column, *predictors]) if predictors else "需要 --predictor-columns"
    if absent:
        return None, predictors, {"status": "blocked", "reasons": [absent], "recommendations": []}
    subset = frame[[args.value_column, *predictors]].replace([np.inf, -np.inf], np.nan).dropna()
    if any(not pd.api.types.is_numeric_dtype(subset[column]) or subset[column].nunique() < 2 for column in predictors):
        return None, predictors, {"status": "blocked", "reasons": ["回归预测变量必须均为有变异的预先定义数值变量；分类变量须先声明编码方案。"], "recommendations": []}
    return subset, predictors, None


def decide_binary_regression(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    subset, predictors, failure = regression_inputs(frame, args)
    if failure:
        return failure
    missing = review_result(args, need_power=False, labels=[("linearity_review", "连续预测变量与 logit 线性关系审查结果"), ("separation_review", "完全/准完全分离审查结果"), ("model_specification_review", "预先指定的变量、交互项和编码方案审查结果")])
    if args.events_per_predictor is None or args.events_per_predictor <= 0:
        missing.append("预先声明的每模型参数最少事件数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    events, error = binary_event_vector(subset[args.value_column], args.event_value)
    if error:
        return {"status": "blocked", "reasons": [error], "recommendations": []}
    required = int(np.ceil(args.events_per_predictor * (len(predictors) + 1)))
    if min(int(events.sum()), int(len(events) - events.sum())) < required:
        return {"status": "blocked", "reasons": [f"事件或非事件数低于用户声明的二元回归门槛 {required}。"], "diagnostics": {"events": int(events.sum()), "non_events": int(len(events) - events.sum()), "required_per_outcome": required}, "recommendations": []}
    power_ok, reason, power = external_power_gate(args)
    if not power_ok:
        return {"status": "needs-confirmation", "missing": [reason or "二元回归功效审查未通过"], "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "logistic-regression", "evidence": "binary outcome; reviewed logit-linearity, separation, specification, events-per-parameter, and external power gates"}], "diagnostics": {"rows_used": int(len(subset)), "predictors": predictors, "events": int(events.sum()), "non_events": int(len(events) - events.sum()), "required_per_outcome": required}, "power": power}


def decide_ordinal_regression(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    subset, predictors, failure = regression_inputs(frame, args)
    if failure:
        return failure
    missing = review_result(args, need_power=False, labels=[("ordinal_order_review", "有序类别编码和阈值方向审查结果"), ("proportional_odds_review", "比例优势假设及其替代方案审查结果"), ("model_specification_review", "预先指定的变量、交互项和编码方案审查结果")])
    if args.minimum_category_count is None or args.minimum_category_count <= 0:
        missing.append("预先声明的每个有序类别最低样本数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    outcome = subset[args.value_column]
    categories = outcome.value_counts(dropna=False)
    if len(categories) < 3:
        return {"status": "blocked", "reasons": ["等级回归至少需要三个有序结果类别。"], "recommendations": []}
    if categories.min() < args.minimum_category_count:
        return {"status": "blocked", "reasons": ["至少一个有序结果类别少于用户声明的最低样本数。"], "diagnostics": {"category_counts": {str(key): int(value) for key, value in categories.items()}}, "recommendations": []}
    power_ok, reason, power = external_power_gate(args)
    if not power_ok:
        return {"status": "needs-confirmation", "missing": [reason or "等级回归功效审查未通过"], "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": "ordinal-regression", "evidence": "ordered multi-category outcome; reviewed ordering, proportional odds, specification, category support, and external power gates"}], "diagnostics": {"rows_used": int(len(subset)), "predictors": predictors, "category_counts": {str(key): int(value) for key, value in categories.items()}}, "power": power}


def decide_pls(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    subset, predictors, failure = regression_inputs(frame, args)
    if failure:
        return failure
    if args.outcome != "continuous":
        return {"status": "blocked", "reasons": ["当前 PLS 适配器只支持连续结果。"], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("component_selection_review", "成分数仅由训练折内选择的审查结果"), ("leakage_review", "训练/验证数据泄漏审查结果"), ("preprocessing_review", "标准化/缺失处理仅在训练折拟合的审查结果")])
    if args.validation_plan == "unknown":
        missing.append("嵌套交叉验证、独立测试或时间外推验证方案")
    if args.minimum_rows_per_feature is None or args.minimum_rows_per_feature <= 0:
        missing.append("预先声明的每特征最低有效样本数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    if len(subset) < args.minimum_rows_per_feature * (len(predictors) + 1):
        return {"status": "blocked", "reasons": ["样本量低于用户声明的 PLS 开发资格门槛。"], "recommendations": []}
    return {"status": "eligible-development", "recommendations": [{"method_id": "pls", "evidence": "continuous multivariable outcome; leakage-safe component selection and external validation plan confirmed"}], "development_eligibility": {"rows_used": int(len(subset)), "predictors": predictors, "validation_plan": args.validation_plan}, "caution": "该资格不代表拟合性能；成分数、预处理和性能指标必须在嵌套验证或独立测试中计算。"}


def decide_discriminant(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    predictors = parse_columns(args.predictor_columns)
    absent = require_columns(frame, [args.class_column, *predictors]) if predictors else "需要 --class-column 和 --predictor-columns"
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("class_balance_review", "类别支持与抽样代表性审查结果"), ("covariance_review", "类别协方差结构和线性可分性审查结果"), ("leakage_review", "训练/验证数据泄漏审查结果"), ("preprocessing_review", "仅在训练折拟合预处理的审查结果")])
    if args.validation_plan == "unknown":
        missing.append("分层且与数据生成机制匹配的验证方案")
    if args.minimum_class_count is None or args.minimum_class_count <= 0:
        missing.append("预先声明的每类别最低样本数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[[args.class_column, *predictors]].replace([np.inf, -np.inf], np.nan).dropna()
    counts = subset[args.class_column].value_counts(dropna=False)
    if len(counts) < 2 or counts.min() < args.minimum_class_count:
        return {"status": "blocked", "reasons": ["类别数不足或至少一个类别低于用户声明的最低样本数。"], "diagnostics": {"class_counts": {str(key): int(value) for key, value in counts.items()}}, "recommendations": []}
    if any(not pd.api.types.is_numeric_dtype(subset[column]) or subset[column].nunique() < 2 for column in predictors):
        return {"status": "blocked", "reasons": ["判别分析预测变量必须是有变异的预先定义数值变量；分类变量须先声明编码方案。"], "recommendations": []}
    return {"status": "eligible-development", "recommendations": [{"method_id": "discriminant-analysis", "evidence": "supported classes; reviewed covariance/representativeness and leakage-safe validation plan confirmed"}], "development_eligibility": {"rows_used": int(len(subset)), "predictors": predictors, "class_counts": {str(key): int(value) for key, value in counts.items()}, "validation_plan": args.validation_plan}, "caution": "该资格不代表分类性能或临床/业务可用性；准确率、校准和阈值必须仅在未见数据上报告。"}


def decide_survival(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    absent = require_columns(frame, [args.duration_column, args.event_column])
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("censoring_review", "非信息性删失与随访完整性审查结果")])
    if args.minimum_events is None:
        missing.append("预先声明的最少可解释事件数")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    duration = frame[args.duration_column]
    event = frame[args.event_column]
    if not pd.api.types.is_numeric_dtype(duration):
        return {"status": "blocked", "reasons": ["生存时间列必须为数值型时长。"], "recommendations": []}
    subset = pd.DataFrame({"duration": duration, "event": event}).replace([np.inf, -np.inf], np.nan).dropna()
    if (subset["duration"] < 0).any():
        return {"status": "blocked", "reasons": ["生存时长不能为负。"], "recommendations": []}
    if set(subset["event"].unique()) - {0, 1, False, True}:
        return {"status": "blocked", "reasons": ["事件列必须编码为 0/1。"], "recommendations": []}
    event_count = int(subset["event"].astype(bool).sum())
    threshold = max(MIN_SURVIVAL_EVENTS, int(args.minimum_events))
    diagnostic = {"rows_used": int(len(subset)), "events": event_count, "censored": int(len(subset) - event_count), "minimum_events": threshold}
    if event_count < threshold:
        return {"status": "blocked", "reasons": [f"观察到 {event_count} 个事件，少于声明门槛 {threshold}；不推荐 Kaplan-Meier 曲线作为推断证据。"], "diagnostics": diagnostic, "recommendations": []}
    covariates = [value.strip() for value in (args.covariate_columns or "").split(",") if value.strip()]
    if args.survival_model == "cox" or covariates:
        absent = require_columns(frame, covariates)
        if absent:
            return {"status": "blocked", "reasons": [absent], "diagnostics": diagnostic, "recommendations": []}
        if not covariates:
            return {"status": "needs-confirmation", "missing": ["Cox 模型的预先指定协变量列"], "diagnostics": diagnostic, "recommendations": []}
        if args.proportional_hazards_review != "confirmed":
            return {"status": "needs-confirmation", "missing": ["比例风险假设与时间变效应审查结果"], "diagnostics": diagnostic, "recommendations": []}
        if args.events_per_covariate is None or args.events_per_covariate <= 0:
            return {"status": "needs-confirmation", "missing": ["预先声明的每协变量最低事件数及其依据"], "diagnostics": diagnostic, "recommendations": []}
        required_events = int(np.ceil(args.events_per_covariate * len(covariates)))
        if event_count < required_events:
            return {"status": "blocked", "reasons": [f"事件数 {event_count} 低于用户声明的 Cox 模型门槛 {required_events}。"], "diagnostics": diagnostic, "recommendations": []}
        covariate_frame = frame[covariates].replace([np.inf, -np.inf], np.nan)
        if covariate_frame.isna().any(axis=None) or any(not pd.api.types.is_numeric_dtype(covariate_frame[column]) or covariate_frame[column].nunique() < 2 for column in covariates):
            return {"status": "blocked", "reasons": ["Cox 协变量必须为无缺失且有变异的预先定义数值变量；分类变量须先声明编码方案。"], "diagnostics": diagnostic, "recommendations": []}
        power_ok, reason, power = external_power_gate(args)
        if not power_ok:
            return {"status": "needs-confirmation", "missing": [reason or "Cox 功效审查未通过"], "diagnostics": diagnostic, "recommendations": []}
        diagnostic.update({"covariates": covariates, "required_events": required_events})
        return {"status": "eligible", "recommendations": [{"method_id": "cox-model", "evidence": "time-to-event contract, censoring, proportional-hazards, events-per-covariate, and external power gates pass"}], "diagnostics": diagnostic, "power": power}
    return {"status": "eligible", "recommendations": [{"method_id": "kaplan-meier", "evidence": "time-to-event data; duration/event contract, censoring review, and event-count gate pass"}], "diagnostics": diagnostic, "caution": "Kaplan-Meier 依赖非信息性删失；组间比较或 Cox 回归另需比例风险、协变量与事件数适配器。"}


def decide_predict(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    raw_predictors = [value.strip() for value in (args.predictor_columns or "").split(",") if value.strip()]
    absent = require_columns(frame, [args.value_column, *raw_predictors]) if raw_predictors else "需要 --predictor-columns"
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("leakage_review", "训练/验证数据泄漏审查结果"), ("preprocessing_review", "仅在训练折内拟合预处理的审查结果")])
    if args.validation_plan == "unknown":
        missing.append("与数据生成机制匹配的验证方案（独立测试、嵌套交叉验证或时间外推）")
    if args.minimum_rows_per_feature is None:
        missing.append("预先声明的每特征最低有效样本数及其依据")
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    if args.minimum_rows_per_feature <= 0:
        return {"status": "blocked", "reasons": ["每特征最低有效样本数必须为正数。"], "recommendations": []}
    if len(frame) < args.minimum_rows_per_feature * (len(raw_predictors) + 1):
        return {"status": "blocked", "reasons": ["样本量低于用户预先声明的预测开发资格下限；请减少特征或扩大数据。"], "recommendations": []}
    if any(not pd.api.types.is_numeric_dtype(frame[column]) for column in raw_predictors):
        return {"status": "blocked", "reasons": ["当前严格预测资格审查仅接受已定义编码和缺失处理的数值预测变量。"], "recommendations": []}
    return {"status": "eligible-development", "recommendations": [], "development_eligibility": {"outcome": args.value_column, "predictors": raw_predictors, "validation_plan": args.validation_plan, "rows": int(len(frame))}, "caution": "这不是模型性能或统计推荐；训练、调参、校准与最终独立测试必须在独立管线中完成。"}


def decide_cluster(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    columns = [value.strip() for value in (args.predictor_columns or "").split(",") if value.strip()]
    absent = require_columns(frame, columns) if columns else "需要 --predictor-columns"
    if absent:
        return {"status": "blocked", "reasons": [absent], "recommendations": []}
    missing = review_result(args, need_power=False, labels=[("scaling_review", "特征尺度/距离度量审查结果"), ("stability_review", "聚类稳定性与重采样评估计划")])
    if missing:
        return {"status": "needs-confirmation", "missing": missing, "recommendations": []}
    subset = frame[columns].replace([np.inf, -np.inf], np.nan)
    if subset.isna().any(axis=None):
        return {"status": "blocked", "reasons": ["聚类特征存在缺失；必须预先定义仅基于训练/分析样本的处理策略。"], "recommendations": []}
    if len(columns) < 2 or len(subset) < max(20, 5 * len(columns)):
        return {"status": "blocked", "reasons": ["聚类至少需要两个数值特征，且当前样本不足以进行稳定性审查。"], "recommendations": []}
    if any(not pd.api.types.is_numeric_dtype(subset[column]) or subset[column].nunique() < 2 for column in columns):
        return {"status": "blocked", "reasons": ["聚类特征必须均为有变异的数值变量。"], "recommendations": []}
    if args.cluster_shape == "spherical":
        method_id, evidence = "kmeans", "predeclared approximately spherical/equal-scale clusters; scaling and stability reviews confirmed"
    elif args.cluster_shape == "nested":
        method_id, evidence = "hierarchical-clustering", "predeclared nested structure; scaling and stability reviews confirmed"
    else:
        return {"status": "needs-confirmation", "missing": ["聚类结构假设（spherical 或 nested）；不能根据可视化直觉自动选择算法。"], "recommendations": []}
    return {"status": "eligible", "recommendations": [{"method_id": method_id, "evidence": evidence}], "diagnostics": {"rows_used": int(len(subset)), "features": columns}, "caution": "聚类标签是探索性结果；需报告稳定性、距离度量、标准化与簇数选择，不可直接当作真实类别。"}


def decide_power(frame: pd.DataFrame, args: argparse.Namespace) -> dict:
    if args.design == "independent" and args.outcome == "continuous":
        absent = require_columns(frame, [args.value_column, args.group_column])
        if absent:
            return {"status": "blocked", "reasons": [absent], "recommendations": []}
        diagnostic = group_diagnostics(frame, args.value_column, args.group_column, args.alpha)
        if len(diagnostic["groups"]) not in {2}:
            return {"status": "needs-confirmation", "missing": ["单因素 ANOVA 功效适配器需要三个及以上组的均衡/不均衡设计说明。"], "recommendations": []}
        ok, power, reason = power_gate(diagnostic, args)
        return {"status": "eligible" if ok else "blocked", "recommendations": [{"method_id": "power-two-sample-t", "evidence": "declared effect, alpha, target power, and current allocation"}] if ok else [], "power": power, "reasons": [] if ok else [reason or "功效门未通过"]}
    if args.design == "paired" and args.outcome == "continuous":
        if args.minimum_effect_size is None or args.target_power is None or args.minimum_effect_size <= 0 or not 0 < args.target_power < 1:
            return {"status": "needs-confirmation", "missing": ["配对 Cohen dz、目标功效，以及完整配对数"], "recommendations": []}
        if not args.subject_column:
            return {"status": "needs-confirmation", "missing": ["受试者 ID 列，以计算完整配对数"], "recommendations": []}
        paired = decide_paired(frame, args)
        if "power" not in paired:
            return {"status": paired["status"], "missing": paired.get("missing", paired.get("reasons", [])), "recommendations": []}
        return {"status": "eligible", "recommendations": [{"method_id": "power-paired-t", "evidence": "declared paired effect, alpha, target power, and complete-pair count"}], "power": paired["power"]}
    if args.design == "independent" and args.outcome == "binary":
        binary = decide_binary(frame, args)
        if "power" not in binary:
            return {"status": binary["status"], "missing": binary.get("missing", binary.get("reasons", [])), "recommendations": []}
        return {"status": "eligible", "recommendations": [{"method_id": "power-two-proportion", "evidence": "declared target proportions, alpha, target power, and current allocation"}], "power": binary["power"]}
    return {"status": "needs-confirmation", "missing": ["当前功效适配器支持独立连续双组、配对连续和独立二元双组；其他设计需要方法特异实现。"], "recommendations": []}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path); parser.add_argument("--prompt", required=True); parser.add_argument("--sheet")
    parser.add_argument("--need-statistics", choices=["yes", "no", "unspecified"], default="unspecified")
    parser.add_argument("--intent", choices=["compare", "describe", "association", "predict", "cluster", "survival", "power", "unspecified"], default="unspecified")
    parser.add_argument("--outcome", choices=["continuous", "ordinal", "binary", "time-to-event", "unspecified"], default="unspecified")
    parser.add_argument("--design", choices=["independent", "paired", "repeated", "unspecified"], default="unspecified")
    parser.add_argument("--value-column"); parser.add_argument("--group-column"); parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--experimental-unit")
    parser.add_argument("--independence-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--missingness-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--outlier-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--rank-shape-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--pairing-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--symmetry-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--sphericity-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--linearity-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--residual-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--model-specification-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--separation-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--ordinal-order-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--proportional-odds-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--component-selection-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--class-balance-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--covariance-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--factorial-balance-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--censoring-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--proportional-hazards-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--leakage-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--preprocessing-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--scaling-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--stability-review", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--subject-column"); parser.add_argument("--predictor-column"); parser.add_argument("--predictor-columns"); parser.add_argument("--class-column"); parser.add_argument("--factor-columns")
    parser.add_argument("--duration-column"); parser.add_argument("--event-column"); parser.add_argument("--event-value"); parser.add_argument("--covariate-columns")
    parser.add_argument("--survival-model", choices=["kaplan-meier", "cox"], default="kaplan-meier")
    parser.add_argument("--events-per-covariate", type=float)
    parser.add_argument("--events-per-predictor", type=float); parser.add_argument("--minimum-category-count", type=int); parser.add_argument("--minimum-class-count", type=int)
    parser.add_argument("--minimum-events", type=int); parser.add_argument("--planned-proportions")
    parser.add_argument("--validation-plan", choices=["independent-test", "nested-cv", "temporal-holdout", "unknown"], default="unknown")
    parser.add_argument("--minimum-rows-per-feature", type=int)
    parser.add_argument("--cluster-shape", choices=["spherical", "nested", "unknown"], default="unknown")
    parser.add_argument("--model-type", choices=["auto", "linear", "logistic", "ordinal", "pls", "discriminant"], default="auto")
    parser.add_argument("--minimum-effect-size", type=float)
    parser.add_argument("--target-power", type=float)
    parser.add_argument("--power-assessment", choices=REVIEW_CHOICES, default="unknown")
    parser.add_argument("--achieved-power", type=float)
    args = parser.parse_args()
    if args.need_statistics == "unspecified":
        print(json.dumps({"status": "needs-user-choice", "question": "是否需要统计方法？若需要，请说明研究目的、结果变量类型，以及独立/配对/重复测量设计。"}, ensure_ascii=False)); return
    if args.need_statistics == "no":
        print(json.dumps({"status": "not-requested", "recommendations": []}, ensure_ascii=False)); return
    if not 0 < args.alpha < 1:
        print(json.dumps({"status": "blocked", "reasons": ["alpha 必须在 (0, 1) 内。"], "recommendations": []}, ensure_ascii=False)); return
    frame = load_table(args.data, args.sheet); profile = table_profile(frame)
    packet = {"version": 2, "prompt": args.prompt, "profile": profile, "formula_loaded": False}
    missing = need_confirmation(args)
    if missing:
        packet.update({"status": "needs-confirmation", "missing": missing, "recommendations": []})
    elif args.intent == "compare":
        packet.update(decide_compare(frame, args, profile))
    elif args.intent == "association":
        if args.predictor_columns:
            if args.outcome == "binary":
                packet.update(decide_binary_regression(frame, args))
            elif args.outcome == "ordinal":
                packet.update(decide_ordinal_regression(frame, args))
            else:
                packet.update(decide_regression(frame, args))
        else:
            packet.update(decide_association(frame, args))
    elif args.intent == "survival":
        packet.update(decide_survival(frame, args))
    elif args.intent == "predict":
        if args.model_type == "pls":
            packet.update(decide_pls(frame, args))
        elif args.model_type == "discriminant":
            packet.update(decide_discriminant(frame, args))
        elif args.model_type == "logistic":
            packet.update(decide_binary_regression(frame, args))
        elif args.model_type == "ordinal":
            packet.update(decide_ordinal_regression(frame, args))
        elif args.model_type == "linear":
            packet.update(decide_regression(frame, args))
        else:
            packet.update(decide_predict(frame, args))
    elif args.intent == "cluster":
        packet.update(decide_cluster(frame, args))
    elif args.intent == "power":
        packet.update(decide_power(frame, args))
    else:
        packet.update({"status": "needs-confirmation", "missing": [f"{args.intent} 的严格适配器尚未实现；不自动推荐统计方法。"], "recommendations": []})
    print(json.dumps(packet, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
