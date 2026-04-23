package fire

import fire.output.OutputCustomMetrics
import org.apache.log4j.Logger
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import com.fasterxml.jackson.databind.ObjectMapper

import java.io.{BufferedReader, DataOutputStream, InputStreamReader}
import java.net.{HttpURLConnection, URL}
import java.util
import scala.util.Try

object SparkExample {

  val logger: Logger = Logger.getLogger(SparkExample.getClass)

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

    logger.info(s"Input Path: ${config.inputPath}")
    logger.info(s"PostBack URL: ${config.postBackUrl.getOrElse("Not provided")}")
    logger.info(s"Job ID: ${config.jobId.getOrElse("Not provided")}")
    logger.info(s"Custom Metrics Enabled: ${config.enableCustomMetrics}")

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

    aggDF.show(false)

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
        logger.info("++Post the metrics back to sparkflows++")

        val APIUrl = postBackUrl.replace("messageFromSparkJob", "metricsFromPipelineJob")

        println("++**++**++")
        println(APIUrl)
        val metricsJson =
          if (outputMetrics != null) outputMetrics.toJSON
          else "{}"

        // Build JSON payload safely
        val payload = new util.HashMap[String, String]()
        payload.put("jobId", jobId)
        payload.put("message", metricsJson)

        val mapper = new ObjectMapper()
        val apiBody = mapper.writeValueAsString(payload)


        println("++==++")
        println(apiBody)
        val connection = new URL(APIUrl).openConnection().asInstanceOf[HttpURLConnection]

        try {
          connection.setRequestMethod("POST")
          connection.setRequestProperty("accept", "*/*")
          connection.setRequestProperty("Content-Type", "application/json")
          connection.setDoOutput(true)

          // Write request body
          val outputStream = new DataOutputStream(connection.getOutputStream)
          outputStream.writeBytes(apiBody)
          outputStream.flush()
          outputStream.close()

          // Read response
          val statusCode = connection.getResponseCode
          val reader = new BufferedReader(new InputStreamReader(connection.getInputStream))
          val responseBody = Iterator.continually(reader.readLine())
            .takeWhile(_ != null)
            .mkString("\n")
          reader.close()

          println(s"Status Code: $statusCode")
          println(s"Response Body: $responseBody")

        } finally {
        connection.disconnect()
        }
      }
    }

    // Stop the SparkSession
    spark.stop()
  }
}
