from pathlib import Path

from utils import create_spark_session, write_csv_file

from ingest import ingest_csvs
from clean import clean_data
from summarise import calculate_summary

input_csvs_dir = Path("data/raw_data")
spark = create_spark_session()

try:
	data_df = ingest_csvs(spark, input_csvs_dir)

	cleaned_df = clean_data(data_df)
	write_csv_file(cleaned_df, Path("data/cleaned_data"))

	summary_df = calculate_summary(cleaned_df, "2022-03-01 00:00:00", "2022-03-02 00:00:00",)
	write_csv_file(summary_df, Path("output/summary"))
finally:
	spark.stop()