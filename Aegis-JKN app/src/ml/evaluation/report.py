import json
import os
from datetime import datetime
from typing import Dict, Any
import numpy as np

def generate_report(results: Dict[str, Any], output_dir: str = "reports/evaluation"):
    """
    Generate automated report in JSON and HTML formats.

    Args:
        results: Evaluation results dictionary
        output_dir: Directory to save reports
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Save JSON report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(output_dir, f"eval_report_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)

    # 2. Save HTML report
    html_path = os.path.join(output_dir, f"eval_report_{timestamp}.html")
    html_content = _generate_html(results)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {"json_report": json_path, "html_report": html_path}

def _generate_html(results: Dict[str, Any]) -> str:
    """Internal helper to render results into a basic HTML page"""

    # Helper to format metrics
    def fmt(val):
        return f"{val:.4f}" if isinstance(val, (float, np.float64)) else str(val)

    # Main Metrics Table
    metrics_html = ""
    if "main_metrics" in results:
        metrics_html = "<h2>Main Metrics</h2><table border='1'><tr><th>Metric</th><th>Value</th></tr>"
        for k, v in results["main_metrics"].items():
            metrics_html += f"<tr><td>{k}</td><td>{fmt(v)}</td></tr>"
        metrics_html += "</table>"

    # Baselines Table
    baselines_html = ""
    if "baseline_comparison" in results:
        baselines_html = "<h2>Baseline Comparison</h2><table border='1'><tr><th>Model</th><th>ROC-AUC</th><th>AUPRC</th></tr>"
        for model, m in results["baseline_comparison"].items():
            if "error" in m:
                baselines_html += f"<tr><td>{model}</td><td colspan='2'>Error: {m['error']}</td></tr>"
            else:
                baselines_html += f"<tr><td>{model}</td><td>{fmt(m['roc_auc'])}</td><td>{fmt(m['auprc'])}</td></tr>"
        baselines_html += "</table>"

    # Robustness Tables
    robustness_html = ""
    if "robustness" in results:
        rob = results["robustness"]

        # Masking
        if "masking" in rob:
            masking = rob["masking"]["mask_results"]
            masking_html = "<h2>Masking Robustness</h2><table border='1'><tr><th>Mask Ratio</th><th>ROC-AUC</th><th>AUPRC</th><th>Rel. Degradation (AUC)</th></tr>"
            for ratio, m in masking.items():
                masking_html += f"<tr><td>{ratio}</td><td>{fmt(m['roc_auc_mean'])}</td><td>{fmt(m['auprc_mean'])}</td><td>{fmt(m['roc_auc_rel_degradation'])}%</td></tr>"
            masking_html += "</table>"
            robustness_html += masking_html

        # Camouflage
        if "camouflage" in rob:
            cam = rob["camouflage"]["camouflage_only"]
            cam_html = "<h2>Camouflage Detection</h2><table border='1'><tr><th>Metric</th><th>Value</th></tr>"
            cam_html += f"<tr><td>Detection Rate</td><td>{fmt(cam['detection_rate'])}</td></tr>"
            cam_html += f"<tr><td>ROC-AUC</td><td>{fmt(cam['roc_auc'])}</td></tr>"
            cam_html += f"<tr><td>AUPRC</td><td>{fmt(cam['auprc'])}</td></tr>"
            cam_html += "</table>"
            robustness_html += cam_html

    return f"""
    <html>
    <head>
        <title>Aegis-JKN Evaluation Report</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; background: #f4f7f6; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            table {{ border-collapse: collapse; width: 100%; max-width: 800px; margin-bottom: 20px; background: white; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Aegis-JKN ML Evaluation Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        {metrics_html}
        {baselines_html}
        {robustness_html}
    </body>
    </html>
    """
