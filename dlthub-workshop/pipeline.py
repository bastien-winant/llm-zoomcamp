from datetime import datetime
from zoneinfo import ZoneInfo

import dlt
from logfire.query_client import AsyncLogfireQueryClient


@dlt.resource
async def metrics(
    read_token=dlt.secrets.value,
    batch_size: int = 1000,
    min_timestamp=dlt.sources.incremental(
        "created_at",
        initial_value=datetime(1970, 1, 1, tzinfo=ZoneInfo("UTC")),
    ),
):
    """Fetches rows from the Logfire `metrics` table incrementally.

    `metrics` contains pre-aggregated numerical data. It is more efficient than
    querying `records` for time-series aggregations but has no dedicated Logfire UI.

    Args:
        read_token (str): Logfire read API token, loaded from `secrets.toml`.
        batch_size (int): Maximum number of rows returned per query.
        min_timestamp: Incremental cursor on `created_at`; only rows newer than
            the last pipeline run are fetched.

    Yields:
        pyarrow.Table: A batch of metric rows as an Arrow table.
    """
    async with AsyncLogfireQueryClient(read_token=read_token) as client:
        batch = await client.query_arrow(
            sql=f"SELECT * FROM metrics LIMIT {batch_size}",
            min_timestamp=min_timestamp.start_value,
        )
        yield batch.to_pylist()


@dlt.resource
async def records(
    read_token=dlt.secrets.value,
    batch_size: int = 1000,
    min_timestamp=dlt.sources.incremental(
        "created_at",
        initial_value=datetime(1970, 1, 1, tzinfo=ZoneInfo("UTC")),
    ),
):
    """Fetches rows from the Logfire `records` table incrementally.

    Each row is a span or a log (a span with no duration). Spans sharing the same
    `trace_id` form a trace, structured as a tree. This is the primary table shown
    in the Logfire Live View and the one most queries should target.

    Note: `records` excludes pending spans. The full table including pending spans
    is `records_all`, but it is not needed for most use cases.

    Args:
        read_token (str): Logfire read API token, loaded from `secrets.toml`.
        batch_size (int): Maximum number of rows returned per query.
        min_timestamp: Incremental cursor on `created_at`; only rows newer than
            the last pipeline run are fetched.

    Yields:
        pyarrow.Table: A batch of span/log rows as an Arrow table.
    """
    async with AsyncLogfireQueryClient(read_token=read_token) as client:
        batch = await client.query_arrow(
            sql=f"SELECT * FROM records LIMIT {batch_size}",
            min_timestamp=min_timestamp.start_value,
        )
        yield batch.to_pylist()


@dlt.source
def logfire_source():
    """Returns all Logfire resources (metrics and records) as a dlt source."""
    return [metrics, records]


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="logfire",
        destination="duckdb",
    )
    pipeline.run(logfire_source)