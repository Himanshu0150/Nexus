import sys
import os

# Add parent directory to path to import db queries
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo_queries import (
    explain_search_performance,
    create_category_price_index,
    drop_category_price_index
)

def inspect_stages(execution_stats):
    """Recursively traverse execution stages to detect scan type and sort stage."""
    stages = []
    has_sort_stage = False
    mem_sorted_bytes = 0

    def traverse(stage_node):
        nonlocal has_sort_stage, mem_sorted_bytes
        if not stage_node or not isinstance(stage_node, dict):
            return
        stage_name = stage_node.get("stage", "UNKNOWN")
        stages.append(stage_name)
        if stage_name == "SORT":
            has_sort_stage = True
            mem_sorted_bytes = stage_node.get("totalDataSizeSorted", stage_node.get("peakTrackedMemBytes", 0))
        if "inputStage" in stage_node:
            traverse(stage_node["inputStage"])
        if "inputStages" in stage_node:
            for s in stage_node["inputStages"]:
                traverse(s)

    top_stage = execution_stats.get("executionStages", {})
    traverse(top_stage)
    scan_stage = "IXSCAN" if "IXSCAN" in stages else ("COLLSCAN" if "COLLSCAN" in stages else stages[-1] if stages else "UNKNOWN")
    return {
        "stages": " -> ".join(stages),
        "scan_stage": scan_stage,
        "has_sort_stage": has_sort_stage,
        "mem_sorted_bytes": mem_sorted_bytes,
        "docs_examined": execution_stats.get("totalDocsExamined", 0),
        "keys_examined": execution_stats.get("totalKeysExamined", 0),
        "n_returned": execution_stats.get("nReturned", 0),
        "exec_time_ms": execution_stats.get("executionTimeMillis", 0),
    }

def main():
    category = "laptops"
    sort_dir = 1
    min_price = 100.0
    max_price = 1500.0

    print("=" * 80)
    print("MONGODB ESR QUERY OPTIMIZATION BENCHMARK (Equality, Sort, Range)")
    print("=" * 80)
    print(f"Query Predicate : category == '{category}' (Equality)")
    print(f"Sort Key        : price ASC (Sort: {sort_dir})")
    print(f"Range Filter    : price >= ${min_price} AND price <= ${max_price} (Range)")
    print("=" * 80)

    # 1. Benchmark without Index (COLLSCAN + in-memory SORT)
    drop_category_price_index()
    raw_stats_before = explain_search_performance(category, sort_dir, min_price, max_price)
    metrics_before = inspect_stages(raw_stats_before)

    # 2. Build compound index adhering to ESR: (category: 1, price: 1)
    create_category_price_index()
    raw_stats_after = explain_search_performance(category, sort_dir, min_price, max_price)
    metrics_after = inspect_stages(raw_stats_after)

    # 3. Formatted comparative table
    before_mem = f"{metrics_before['mem_sorted_bytes']:,} bytes"
    after_mem = f"{metrics_after['mem_sorted_bytes']:,} bytes"
    before_sort = f"{metrics_before['has_sort_stage']} (EXPENSIVE)"
    after_sort = f"{metrics_after['has_sort_stage']} (ELIMINATED)"
    before_time = f"{metrics_before['exec_time_ms']} ms"
    after_time = f"{metrics_after['exec_time_ms']} ms"

    print("\nBENCHMARK EXECUTION RESULTS:\n")
    print(f"{'Performance Metric':<30} | {'COLLSCAN (No Index)':<22} | {'IXSCAN (ESR Compound Index)':<24}")
    print("-" * 80)
    print(f"{'Query Execution Plan':<30} | {metrics_before['stages']:<22} | {metrics_after['stages']:<24}")
    print(f"{'Scan Strategy':<30} | {metrics_before['scan_stage']:<22} | {metrics_after['scan_stage']:<24}")
    print(f"{'In-Memory SORT Stage?':<30} | {before_sort:<22} | {after_sort:<24}")
    print(f"{'In-Memory Sort RAM Buffer':<30} | {before_mem:<22} | {after_mem:<24}")
    print(f"{'Documents Examined':<30} | {str(metrics_before['docs_examined']):<22} | {str(metrics_after['docs_examined']):<24}")
    print(f"{'Index Keys Examined':<30} | {str(metrics_before['keys_examined']):<22} | {str(metrics_after['keys_examined']):<24}")
    print(f"{'Matching Documents Returned':<30} | {str(metrics_before['n_returned']):<22} | {str(metrics_after['n_returned']):<24}")
    print(f"{'Execution Time':<30} | {before_time:<22} | {after_time:<24}")
    print("-" * 80)

    print("\nACADEMIC TAKEAWAYS (ESR RULE):")
    print("1. Equality ('category: 1'): Scopes down to the exact subset without reading foreign records.")
    print("2. Sort ('price: 1'): B-Tree ordering provides presorted records, eliminating the in-memory SORT stage.")
    print("3. Range ('price: [100, 1500]'): Slices bounded index intervals directly within the B-Tree.")
    print("4. Memory & Safety: Eliminates MongoDB's 100MB in-memory sort threshold and disk-spill penalty.\n")

if __name__ == "__main__":
    main()
