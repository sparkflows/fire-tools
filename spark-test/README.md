# Spark Example Job

## Overview
This Spark job reads a CSV file, aggregates data by category (sum of amount),
and saves the result as Parquet. Optionally, it sends custom metrics back to
the Sparkflows UI via a postback URL.

---

## Arguments

| Argument               | Required | Description                                      |
|------------------------|----------|--------------------------------------------------|
| `--inputPath`          | Yes      | Path to the input CSV file                       |
| `--postBackUrl`        | No       | Sparkflows postback URL to send metrics          |
| `--jobId`              | No       | Pipeline Job ID from Sparkflows                  |
| `--enableCustomMetrics`| No       | Enable sending custom metrics (default: `false`) |

---

## Input CSV Format

The input CSV must contain at least the following columns:

| Column     | Type   | Description          |
|------------|--------|----------------------|
| `category` | String | Category of the item |
| `amount`   | Double | Amount value         |

---

## Example 1: Without Custom Metrics

Basic run — reads CSV, aggregates, and saves as Parquet. No metrics are sent back.

```bash
spark-submit \
  --class fire.SparkExample \
  --master yarn \
  spark-example.jar \
  --inputPath hdfs:///data/input/transactions.csv
```

---

## Example 2: With Custom Metrics + PostBack to Sparkflows UI

Reads CSV, aggregates, saves as Parquet, and sends custom metrics back to the
Sparkflows UI using the provided `--postBackUrl` and `--jobId`.

```bash
spark-submit \
  --class fire.SparkExample \
  --master yarn \
  spark-example.jar \
  --inputPath hdfs:///data/input/transactions.csv \
  --enableCustomMetrics true \
  --postBackUrl http://<sparkflows-host>:8080/messageFromSparkJob \
  --jobId 09267a18-7d81-4d94-9a7f-f93320690ebf
```

> **Note:** The job internally replaces `messageFromSparkJob` with
> `metricsFromPipelineJob` in the URL before posting metrics.

---

## Custom Metrics Sent to Sparkflows UI

When `--enableCustomMetrics true` is provided along with a valid `--postBackUrl`
and `--jobId`, the following custom metrics are posted:

| Metric       | Type    | Example Value |
|--------------|---------|---------------|
| `region`     | String  | `us-east-1`   |
| `retryCount` | Integer | `3`           |
| `isSpilled`  | Boolean | `true`        |
| `latencyP99` | Double  | `245.7`       |
| `throughput` | Long    | `9800`        |

### API Endpoint Called

POST http://<sparkflows-host>:8080/metricsFromPipelineJob

### Request Payload Example

```json
{
  "jobId": "09267a18-7d81-4d94-9a7f-f93320690ebf",
  "message": "{\"customFields\":{\"region\":\"us-east-1\",\"retryCount\":3,\"isSpilled\":true,\"latencyP99\":245.7,\"throughput\":9800},\"id\":0,\"name\":\"\",\"type\":\"custom-metrics\",\"time\":\"2026-04-17 08:52:53\",\"resultType\":99,\"visibility\":\"EXPANDED\",\"tabId\":\"\"}"
}
```

---

## Output

- Aggregated Parquet files saved to: `data/output_parquet/`
- Console output shows aggregated results via `aggDF.show()`
- If metrics enabled, HTTP status code and response body are printed to logs

---

## Notes

- `--postBackUrl` and `--jobId` must **both** be provided for metrics to be posted
- If either is missing, metrics collection is skipped even if `--enableCustomMetrics true`
- Metrics are posted **after** the Spark job completes aggregation
  
