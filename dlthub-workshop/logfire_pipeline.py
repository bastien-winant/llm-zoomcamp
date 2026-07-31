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
    """Load span/log rows from the Logfire Query API (`records` table).

    Args:
        read_token: Logfire read token. Auto-loaded from secrets.toml.
        base_url: API base URL (US or EU). Auto-loaded from config.toml.
        min_timestamp: ISO8601 lower bound for `start_timestamp`. Defaults to 24h ago.
        row_limit: Max rows per query (API max 10_000). Defaults to 100.

    Examples:
        pipeline.run(logfire_source())
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
                "primary_key": "span_id",
                "write_disposition": "replace",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "data_selector": "data",
                    "paginator": "single_page",
                    "json": {
                        "sql": f"SELECT * FROM records LIMIT {row_limit}",
                        "min_timestamp": min_timestamp,
                        "limit": row_limit,
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_logfire_records() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="logfire",
        destination="duckdb",
        dataset_name="logfire_data",
        dev_mode=True,
    )

    load_info = pipeline.run(logfire_source().add_limit(1))
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    load_logfire_records()
