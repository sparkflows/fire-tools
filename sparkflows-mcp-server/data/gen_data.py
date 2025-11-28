import json
import os
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd

# ------------------------------------------------------------
# Adjust this if your project is in a different location
# ------------------------------------------------------------
BASE_DIR = Path("/Users/dhruv/Documents/Dev/sparkflows/mcp/fire-tools/sparkflows-mcp-server")
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REQ_PATH = DATA_DIR / "part-00000-278-requests.snappy.parquet"
RES_PATH = DATA_DIR / "part-00000-278-responses.snappy.parquet"
CONFIG_PATH = DATA_DIR / "extraction_config_278_example.json"


def make_requests_df(n_rows: int = 50) -> pd.DataFrame:
    rows = []
    start_time = datetime(2024, 1, 1, 12, 0, 0)

    payload_schema_versions = ["005010X215", "005010X216", "005010X217"]
    market_bases = ["ARK", "IMN", "OTHER"]

    for i in range(1, n_rows + 1):
        # Alternate event types IN / OUT
        event_type = "IN" if i % 2 == 1 else "OUT"
        # Alternate event_source suffixes
        if i % 3 == 0:
            event_source = "SomeService-GatewayRequest"
        else:
            event_source = "SomeService-PayerInteractionRequest"

        msg_domain = "PA"
        payload_format = "X12"
        market_base = market_bases[i % len(market_bases)]
        payload_schema_version = payload_schema_versions[i % len(payload_schema_versions)]

        # Every 10th record has trace_id starting with e2e- (to test filter)
        trace_prefix = "e2e-" if i % 10 == 0 else "trc-"
        trace_id = f"{trace_prefix}{i:04d}"

        event_time = start_time + timedelta(minutes=i)

        batch = f"batch_{1 + (i // 10)}"  # simple batch grouping

        rows.append(
            {
                "batch": batch,
                "trace_id": trace_id,
                "event_time": event_time,
                # "Metadata" flattened:
                "metadata_event_source": event_source,
                "metadata_msg_domain": msg_domain,
                "metadata_payload_format": payload_format,
                "metadata_event_type": event_type,
                "metadata_market_base": market_base,
                "metadata_payload_schema_version": payload_schema_version,
                # some payload columns
                "payload_raw": f"REQUEST_PAYLOAD_{i}",
            }
        )

    return pd.DataFrame(rows)


def make_responses_df(n_rows: int = 50) -> pd.DataFrame:
    rows = []
    start_time = datetime(2024, 1, 1, 12, 30, 0)

    payload_schema_versions = ["005010X215", "005010X216", "005010X217"]
    market_bases = ["ARK", "IMN", "OTHER"]

    for i in range(1, n_rows + 1):
        # Keep same trace_ids as requests to simulate pairs
        # (responses are slightly later in time)
        # Here we use only "IN"/"OUT" on the response side same way,
        # though in real 278 you might encode this differently.
        event_type = "IN" if i % 2 == 1 else "OUT"

        if i % 3 == 0:
            event_source = "SomeService-GatewayResponse"
        else:
            event_source = "SomeService-PayerInteractionResponse"

        msg_domain = "PA"
        payload_format = "X12"
        market_base = market_bases[i % len(market_bases)]
        payload_schema_version = payload_schema_versions[i % len(payload_schema_versions)]

        trace_prefix = "e2e-" if i % 10 == 0 else "trc-"
        trace_id = f"{trace_prefix}{i:04d}"

        event_time = start_time + timedelta(minutes=i)

        batch = f"batch_{1 + (i // 10)}"

        rows.append(
            {
                "batch": batch,
                "trace_id": trace_id,
                "event_time": event_time,
                "metadata_event_source": event_source,
                "metadata_msg_domain": msg_domain,
                "metadata_payload_format": payload_format,
                "metadata_event_type": event_type,
                "metadata_market_base": market_base,
                "metadata_payload_schema_version": payload_schema_version,
                "payload_raw": f"RESPONSE_PAYLOAD_{i}",
            }
        )

    return pd.DataFrame(rows)


def write_parquet_files():
    df_req = make_requests_df()
    df_res = make_responses_df()

    # You need pyarrow or fastparquet installed for this:
    # pip install pyarrow
    df_req.to_parquet(REQ_PATH, index=False)
    df_res.to_parquet(RES_PATH, index=False)

    print(f"Wrote requests parquet to: {REQ_PATH}")
    print(f"Wrote responses parquet to: {RES_PATH}")


def build_extraction_config() -> dict:
    """
    Example extraction config that describes:
    - aliases inReq, outReq, inRes, outRes
    - filters on metadata_* fields
    - a SQL string for dedupe/join logic
    """

    config = {
        "version": 1,
        "description": "Example 278 extraction config for synthetic request/response parquet files.",
        "sources": {
            "inReq": {
                "alias": "inReq",
                "path": str(REQ_PATH),
                "batch_column": "batch",
                "metadata_prefix": "metadata_",
                "filters": {
                    "event_source_suffix": ["GatewayRequest", "PayerInteractionRequest"],
                    "msg_domain": "PA",
                    "payload_format": "X12",
                    "event_type": "IN",
                    "market_base_in": ["ARK", "IMN"],
                    "payload_schema_version_in": ["005010X215", "005010X216", "005010X217"],
                    "trace_id_not_like": "e2e-%",
                },
            },
            "outReq": {
                "alias": "outReq",
                "path": str(REQ_PATH),
                "batch_column": "batch",
                "metadata_prefix": "metadata_",
                "filters": {
                    "event_source_suffix": ["GatewayRequest", "PayerInteractionRequest"],
                    "msg_domain": "PA",
                    "payload_format": "X12",
                    "event_type": "OUT",
                    "market_base_in": ["ARK", "IMN"],
                    "payload_schema_version_in": ["005010X215", "005010X216", "005010X217"],
                    "trace_id_not_like": "e2e-%",
                },
            },
            "inRes": {
                "alias": "inRes",
                "path": str(RES_PATH),
                "batch_column": "batch",
                "metadata_prefix": "metadata_",
                "filters": {
                    "event_source_suffix": ["GatewayResponse", "PayerInteractionResponse"],
                    "msg_domain": "PA",
                    "payload_format": "X12",
                    "event_type": "IN",
                    "market_base_in": ["ARK", "IMN"],
                    "payload_schema_version_in": ["005010X215", "005010X216", "005010X217"],
                    "trace_id_not_like": "e2e-%",
                },
            },
            "outRes": {
                "alias": "outRes",
                "path": str(RES_PATH),
                "batch_column": "batch",
                "metadata_prefix": "metadata_",
                "filters": {
                    "event_source_suffix": ["GatewayResponse", "PayerInteractionResponse"],
                    "msg_domain": "PA",
                    "payload_format": "X12",
                    "event_type": "OUT",
                    "market_base_in": ["ARK", "IMN"],
                    "payload_schema_version_in": ["005010X215", "005010X216", "005010X217"],
                    "trace_id_not_like": "e2e-%",
                },
            },
        },
        "dedupe_and_join": {
            "primary_key": "trace_id",
            "timestamp_column": "event_time",
            "target_batch_param": "target_batch",     # e.g. 'batch_3'
            "previous_batch_param": "previous_batch", # e.g. 'batch_2'
            "sql": """
WITH inReq_filtered AS (
  SELECT *
  FROM inReq
  WHERE
    (metadata_event_source LIKE '%GatewayRequest'
     OR metadata_event_source LIKE '%PayerInteractionRequest')
    AND metadata_msg_domain = 'PA'
    AND metadata_payload_format = 'X12'
    AND metadata_event_type = 'IN'
    AND metadata_market_base IN ('ARK', 'IMN')
    AND metadata_payload_schema_version IN ('005010X215', '005010X216', '005010X217')
    AND trace_id NOT LIKE 'e2e-%'
),
outReq_filtered AS (
  SELECT *
  FROM outReq
  WHERE
    (metadata_event_source LIKE '%GatewayRequest'
     OR metadata_event_source LIKE '%PayerInteractionRequest')
    AND metadata_msg_domain = 'PA'
    AND metadata_payload_format = 'X12'
    AND metadata_event_type = 'OUT'
    AND metadata_market_base IN ('ARK', 'IMN')
    AND metadata_payload_schema_version IN ('005010X215', '005010X216', '005010X217')
    AND trace_id NOT LIKE 'e2e-%'
),
inRes_filtered AS (
  SELECT *
  FROM inRes
  WHERE
    (metadata_event_source LIKE '%GatewayResponse'
     OR metadata_event_source LIKE '%PayerInteractionResponse')
    AND metadata_msg_domain = 'PA'
    AND metadata_payload_format = 'X12'
    AND metadata_event_type = 'IN'
    AND metadata_market_base IN ('ARK', 'IMN')
    AND metadata_payload_schema_version IN ('005010X215', '005010X216', '005010X217')
    AND trace_id NOT LIKE 'e2e-%'
),
outRes_filtered AS (
  SELECT *
  FROM outRes
  WHERE
    (metadata_event_source LIKE '%GatewayResponse'
     OR metadata_event_source LIKE '%PayerInteractionResponse')
    AND metadata_msg_domain = 'PA'
    AND metadata_payload_format = 'X12'
    AND metadata_event_type = 'OUT'
    AND metadata_market_base IN ('ARK', 'IMN')
    AND metadata_payload_schema_version IN ('005010X215', '005010X216', '005010X217')
    AND trace_id NOT LIKE 'e2e-%'
),
inReq_dedup AS (
  SELECT *
  FROM inReq_filtered
  QUALIFY ROW_NUMBER() OVER (PARTITION BY trace_id ORDER BY event_time DESC) = 1
),
outReq_dedup AS (
  SELECT *
  FROM outReq_filtered
  QUALIFY ROW_NUMBER() OVER (PARTITION BY trace_id ORDER BY event_time DESC) = 1
),
inRes_dedup AS (
  SELECT *
  FROM inRes_filtered
  QUALIFY ROW_NUMBER() OVER (PARTITION BY trace_id ORDER BY event_time DESC) = 1
),
outRes_dedup AS (
  SELECT *
  FROM outRes_filtered
  QUALIFY ROW_NUMBER() OVER (PARTITION BY trace_id ORDER BY event_time DESC) = 1
)
SELECT
  COALESCE(inReq_dedup.batch, 'null')     AS inReq_batch,
  COALESCE(outReq_dedup.batch, 'null')    AS outReq_batch,
  COALESCE(inRes_dedup.batch, 'null')     AS inRes_batch,
  COALESCE(outRes_dedup.batch, 'null')    AS outRes_batch,
  inReq_dedup.trace_id,
  inReq_dedup.event_time                  AS inReq_event_time,
  outReq_dedup.event_time                 AS outReq_event_time,
  inRes_dedup.event_time                  AS inRes_event_time,
  outRes_dedup.event_time                 AS outRes_event_time,
  inReq_dedup.payload_raw                 AS inReq_payload,
  outReq_dedup.payload_raw                AS outReq_payload,
  inRes_dedup.payload_raw                 AS inRes_payload,
  outRes_dedup.payload_raw                AS outRes_payload
FROM inReq_dedup
LEFT JOIN outReq_dedup
  ON inReq_dedup.trace_id = outReq_dedup.trace_id
LEFT JOIN inRes_dedup
  ON inReq_dedup.trace_id = inRes_dedup.trace_id
LEFT JOIN outRes_dedup
  ON inReq_dedup.trace_id = outRes_dedup.trace_id
WHERE
  inReq_dedup.batch = :target_batch
  AND inReq_dedup.batch > :previous_batch
            """.strip(),
        },
        "null_handling": {
            "batch_columns": [
                "inReq_batch",
                "outReq_batch",
                "inRes_batch",
                "outRes_batch",
            ],
            "null_fill_value": "null"
        }
    }

    return config


def write_config_file():
    config = build_extraction_config()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"Wrote extraction config JSON to: {CONFIG_PATH}")


if __name__ == "__main__":
    write_parquet_files()
    # write_config_file()
