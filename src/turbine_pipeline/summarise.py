"""Summary statistics for cleaned turbine measurements."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def calculate_summary(cleaned_df: DataFrame, start_time: str, end_time: str) -> DataFrame:
    """
    Calculate power-output statistics for each turbine.

    Args:
        cleaned_df (DataFrame): Spark DataFrame containing cleaned turbine data
        start_time (str): The start time for filtering the data
        end_time (str): The end time for filtering the data

    Returns:
        DataFrame: Spark DataFrame containing summary statistics for each turbine
    """

    # Calculate expected power outputs for each turbine outside the defined period
    expected_stats_df = cleaned_df.filter(
        (F.col("timestamp") < start_time) | (F.col("timestamp") >= end_time)
    ).groupBy("turbine_id").agg(
        F.avg("power_output").alias("overall_average_power_output"),
        F.stddev("power_output").alias("overall_power_output_stddev"),
    ).withColumn(
        "lower_anomaly_threshold",
        F.col("overall_average_power_output") - 2*F.col("overall_power_output_stddev")
    ).withColumn(
        "upper_anomaly_threshold",
        F.col("overall_average_power_output") + 2*F.col("overall_power_output_stddev")
    )

    # Create df with time period of interest
    filtered_df = cleaned_df.filter(
        (F.col("timestamp") >= start_time)
        & (F.col("timestamp") < end_time)
    )

    # Calculate average power output for each turbine during the defined period
    window_stats_df = filtered_df.groupBy("turbine_id").agg(
        F.avg("power_output").alias("period_avg_output"),
        F.min("power_output").alias("period_min_output"),
        F.max("power_output").alias("period_max_output"),
    )

    # Create summary df
    summary_df = window_stats_df.join(
        expected_stats_df,
        on="turbine_id",
        how="left"
    ).withColumn(
        "under_anomaly_threshold",
        F.col("period_avg_output") < F.col("lower_anomaly_threshold")
    ).withColumn(
        "over_anomaly_threshold",
        F.col("period_avg_output") > F.col("upper_anomaly_threshold")
    ).select(
        "turbine_id",
        "period_min_output",
        "period_max_output",
        "period_avg_output",
        "under_anomaly_threshold",
        "over_anomaly_threshold"
    )

    return summary_df