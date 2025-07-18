from pyspark.sql import SparkSession
from pyspark.sql.functions import col
spark = SparkSession.builder \
    .appName("EmployeeDataAnalysis") \
    .master("local[*]") \
    .getOrCreate()
df = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv("employees.csv")
print("Original Data:")
df.show()
print("Schema:")
df.printSchema()
print("Average Salary by Department:")
df.groupBy("Department").avg("Salary").show()
df = df.withColumn("Bonus", col("Salary") * 0.10)
print("With Bonus Column:")
df.show()
print("High Earners (Salary > 70000):")
df.filter(col("Salary") > 70000).show()
spark.stop()
