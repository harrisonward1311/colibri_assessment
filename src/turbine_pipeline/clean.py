from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


OUTLIER_COLUMNS = ["wind_speed"]


def remove_duplicates(data_df: DataFrame) -> DataFrame:
    """
    Keep one measurement per turbine and timestamp.
    """
    return data_df.dropDuplicates(["timestamp", "turbine_id"])


def remove_null_rows(data_df: DataFrame) -> DataFrame:
    """
    Remove rows containing at least one null value.
    """
    return data_df.dropna(how="any")


def detect_outliers(data_df: DataFrame) -> DataFrame:
    """
    Add a combined per-turbine IQR outlier flag.

    Args:
        data_df (DataFrame): Spark DataFrame containing turbine data
    
    Returns:
        DataFrame: Spark DataFrame with an additional ``is_outlier`` column
    """

    turbine_window = Window.partitionBy("turbine_id")
    flagged_df = data_df
    outlier_flags = []

    # Use Interquartile Range (IQR) method to detect outliers for each column
    # Outlier defined as < Q1 - 1.5 * IQR or > Q3 + 1.5 * IQR
    for column in OUTLIER_COLUMNS:

        first_quartile = F.percentile_approx(
            F.col(column), 0.25, 10000
        ).over(turbine_window)

        third_quartile = F.percentile_approx(
            F.col(column), 0.75, 10000
        ).over(turbine_window)

        interquartile_range = third_quartile - first_quartile

        is_outlier = (
                (F.col(column) < first_quartile - 1.5 * interquartile_range)
                | (F.col(column) > third_quartile + 1.5 * interquartile_range)
            )
        
        outlier_flags.append(is_outlier)

    return flagged_df.withColumn("is_outlier", F.array_contains(F.array(*outlier_flags), True))

def clean_data(data_df: DataFrame) -> DataFrame:
    """
    Clean the turbine data.
    """
    cleaned_df = remove_duplicates(data_df)
    cleaned_df = remove_null_rows(cleaned_df)
    cleaned_df = detect_outliers(cleaned_df)
    return cleaned_df.filter(~F.col("is_outlier")).drop("is_outlier")