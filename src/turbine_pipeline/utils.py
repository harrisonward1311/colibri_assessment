from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

def create_spark_session():
    """
    Reusable function for creating a SparkSession object

    Returns:
        SparkSession object
    """

    return (
        SparkSession.builder
        .appName("TurbinePipeline")
        .getOrCreate()
    )


def write_csv_file(data_df: DataFrame, path: Path | str, mode: str = "overwrite") -> None:
    """
    Write a Spark DataFrame to a headered CSV output directory.

    Args:
        data_df (DataFrame): Spark DataFrame to write       
        output_path (Path | str): Directory to write the output
        mode (str): Write mode, default is "overwrite"
    """
    data_df.write.mode(mode).option("header", True).csv(str(path))