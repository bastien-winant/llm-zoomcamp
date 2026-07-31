"""Load Logfire records and metrics into DuckDB via the Query API."""

from typing import Any, Optional

import dlt
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="logfire")
def logfire_source(
    read_token: str = dlt.secrets.value,
    base_url: str = dlt.config.value,
    min_timestamp: Optional[str] = None,
    row_limit: int = 100,
) -> Any:
    """Load Logfire ``records`` (spans/logs) and ``metrics`` tables.

    Args:
        read_token: Logfire read token. Auto-loaded from secrets.toml.
        base_url: Region base URL (EU/US). Auto-loaded from config.toml.
        min_timestamp: ISO8601 lower bound. Filters ``start_timestamp`` for
            records and ``recorded_timestamp`` for metrics. Defaults to 24h ago.
        row_limit: Max rows per query (API default 100, max 10_000).

    Examples:
        pipeline.run(logfire_source())
        pipeline.run(logfire_source().with_resources("metrics"))
        pipeline.run(logfire_source(min_timestamp="2026-07-01T00:00:00Z", row_limit=500))
    """
    if min_timestamp is None:
        min_timestamp = pendulum.now("UTC").subtract(hours=24).to_iso8601_string()

    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "auth": {
                "type": "bearer",
                "token": read_token,
            },
        },
        "resources": [
            {
                "name": "records",
                "primary_key": ["trace_id", "span_id"],
                "write_disposition": "replace",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "paginator": "single_page",
                    "json": {
                        "sql": "SELECT * FROM records",
                        "min_timestamp": min_timestamp,
                        "limit": row_limit,
                    },
                    "data_selector": "data",
                },
            },
            {
                "name": "metrics",
                "write_disposition": "replace",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "paginator": "single_page",
                    "json": {
                        "sql": "SELECT * FROM metrics",
                        "min_timestamp": min_timestamp,
                        "limit": row_limit,
                    },
                    "data_selector": "data",
                },
            },
        ],
    }
    yield from rest_api_resources(config)


def load_logfire() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="logfire",
        destination="duckdb",
        dataset_name="logfire_data",
        dev_mode=True,
    )
    load_info = pipeline.run(logfire_source().add_limit(1))
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    load_logfire()
