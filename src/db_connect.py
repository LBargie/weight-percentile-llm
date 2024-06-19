import duckdb
from scipy.stats import norm


# Compute the cumulative distribution function (CDF) of a standard normal distribution
# Equivalent to pnorm(x) in R
def lms_perc(quant: float, lamb: float, mu: float, sigma: float) -> float:
    result = (((quant / mu) ** lamb) - 1) / (lamb * sigma)
    return round(norm.cdf(result, loc=0, scale=1) * 100)


def db_con(path: str = ":memory:", **kwargs) -> duckdb.DuckDBPyConnection:
    """Connect to a DuckDB file or default to in-memory"""
    conn = duckdb.connect(path, **kwargs)

    conn.create_function("lms_percentile", lms_perc)

    return conn