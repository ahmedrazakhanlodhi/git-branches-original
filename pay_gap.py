"""
Gender Pay Gap Analysis
"""

import polars as pl

FILENAME = "earnings.csv"


def get_top_pay_disparities(top_n):
    """
    Calculate gender pay gaps and return top N countries with highest disparities.

    Args:
        top_n: Number of top results to return

    Returns:
        List of tuples: [(country, pay_gap_percentage), ...]
        Sorted by pay_gap_percentage descending
    """
    df = pl.read_csv(FILENAME, encoding="utf8")

    # pick USD normalized data, only M & F
    filtered = df.filter(pl.col("classif1.label") == "Currency: U.S. dollars").filter(
        pl.col("sex.label").is_in(["Male", "Female"])
    )

    # group by country and sex, calculate average earnings
    country_sex_avg = filtered.group_by(["area", "sex.label"]).agg(
        pl.col("obs_value").mean().alias("avg_earnings")
    )

    # pivot to get M & F in same table
    pivoted = country_sex_avg.pivot(values="avg_earnings", index="area", on="sex.label")

    # calculate pay gap
    results = (
        pivoted.with_columns(
            [
                (((pl.col("Male") - pl.col("Female")) / pl.col("Male")) * 100).alias(
                    "pay_gap_percentage"
                )
            ]
        )
        .select(["area", "pay_gap_percentage"])
        .sort("pay_gap_percentage", descending=True)
        .head(top_n)
    )

    return list(results.iter_rows())


if __name__ == "__main__":
    top_disparities = get_top_pay_disparities(10)

    print(f"{'Country':<40} {'Pay Gap %':>10}")
    print("-" * 50)

    for country, gap in top_disparities:
        print(f"{country:<40} {gap:>10.2f}%")
