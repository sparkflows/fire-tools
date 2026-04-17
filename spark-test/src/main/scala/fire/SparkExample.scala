package fire

import fire.output.OutputCustomMetrics
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import scala.util.Try

object SparkExample {

  case class Config(
                     postBackUrl: Option[String] = None,
                     inputPath: String = "",
                     jobId: Option[String] = None,
                     enableCustomMetrics: Boolean = false
                   )

  def parseArgs(args: Array[String]): Config = {

    val map = args.sliding(2, 2).collect {
      case Array("--postBackUrl", value)        => ("postBackUrl", value)
      case Array("--inputPath", value)          => ("inputPath", value)
      case Array("--jobId", value)              => ("jobId", value)
      case Array("--enableCustomMetrics", value)=> ("enableCustomMetrics", value)
    }.toMap

    Config(
      postBackUrl = map.get("postBackUrl"),
      inputPath   = map.getOrElse("inputPath", ""),
      jobId       = map.get("jobId"),
      enableCustomMetrics = map
        .get("enableCustomMetrics")
        .map(_.toBoolean)   // converts "true"/"false"
        .getOrElse(false)
    )
  }


  def main(args: Array[String]): Unit = {

    val config = parseArgs(args)

    require(config.inputPath.nonEmpty, "--inputPath is required")

    println(s"Input Path: ${config.inputPath}")
    println(s"PostBack URL: ${config.postBackUrl.getOrElse("Not provided")}")
    println(s"Job ID: ${config.jobId.getOrElse("Not provided")}")
    println(s"Custom Metrics Enabled: ${config.enableCustomMetrics}")


    // Initialize SparkSession
    val spark = SparkSession.builder()
      .appName("Spark Example")
      .getOrCreate()


    // Read CSV
    val df = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(config.inputPath)


    // Aggregate (sum of amount by category)
    val aggDF = df.groupBy("category")
      .agg(sum("amount").alias("total_amount"))


    // Save as Parquet
    aggDF.write
      .mode("overwrite")
      .parquet("data/output_parquet")


  if(config.enableCustomMetrics){

    val outputMetrics = new OutputCustomMetrics()
    outputMetrics.customFields.put("region", "us-east-1") // String
    outputMetrics.customFields.put("retryCount", Integer.valueOf(3)) // Integer
    outputMetrics.customFields.put("isSpilled", java.lang.Boolean.TRUE) // Boolean
    outputMetrics.customFields.put("latencyP99",  java.lang.Double.valueOf(245.7)) //Double
    outputMetrics.customFields.put("throughput", java.lang.Long.valueOf(9800L) ) // Long, type-validated
    println("++==++")
    println(outputMetrics.toJSON)
    println("++==++")

    val postBackUrl = config.postBackUrl.getOrElse("Not provided")
    val jobId = config.jobId.getOrElse("Not provided")
    if(postBackUrl != "Not provided" && jobId !="Not provided" ){
      println("++Post the metrics back to sparkflows++")

      println("++==++")
    }
  }

  // Stop the SparkSession
  spark.stop()
  }
}
