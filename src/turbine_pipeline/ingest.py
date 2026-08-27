from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import input_file_name
from pyspark.sql.types import (
	DoubleType,
	IntegerType,
	StructField,
	StructType,
	TimestampType,
)

TURBINE_SCHEMA = StructType(
	[
		StructField("timestamp", TimestampType(), nullable=False),
		StructField("turbine_id", IntegerType(), nullable=False),
		StructField("wind_speed", DoubleType(), nullable=True),
		StructField("wind_direction", DoubleType(), nullable=True),
		StructField("power_output", DoubleType(), nullable=True),
	]
)

def ingest_csvs(spark: SparkSession, input_dir: Path | str) -> DataFrame:
	"""
	Read all turbine CSVs from input directory into one DataFrame.
	
    Args:
        spark (SparkSession): SparkSession object
		input_dir (Path | str): Directory containing CSV files
		
	Returns:
        DataFrame: Spark DataFrame containing all turbine data
	"""

	input_path = Path(input_dir)

    # Get CSV files in the directory
	csv_files = input_path.glob("*.csv")

    # Read CSV files into Spark DF
	data_df = (
		spark.read.option("header", True)
		.option("mode", "PERMISSIVE") # Allows malformed data to be skipped
		.schema(TURBINE_SCHEMA)
		.csv([str(path) for path in csv_files])
		.withColumn("source_file", input_file_name())
	)
	
	return data_df
