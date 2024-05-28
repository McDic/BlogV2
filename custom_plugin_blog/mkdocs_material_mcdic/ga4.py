import json
import os
from datetime import date
from pathlib import Path
from typing import TypedDict

from google.analytics import data_v1beta
from google.oauth2 import service_account


class ViewDataValue(TypedDict):
    """
    Misc data of path, measured by GA4.
    """

    views: int
    total_users: int


def get_client(
    project_id: str | None = None,
    private_key_id: str | None = None,
    private_key: str | None = None,
    client_email: str | None = None,
    client_id: str | None = None,
    client_x509_cert_url: str | None = None,
):
    credentials = service_account.Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": project_id or os.environ["GC_PROJECT_ID"],
            "private_key_id": private_key_id or os.environ["GC_PRIVATE_KEY_ID"],
            "private_key": private_key or os.environ["GC_PRIVATE_KEY"],
            "client_email": client_email or os.environ["GC_CLIENT_EMAIL"],
            "client_id": client_id or os.environ["GC_CLIENT_ID"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": client_x509_cert_url
            or os.environ["GC_CLIENT_X509_CERT_URL"],
            "universe_domain": "googleapis.com",
        },
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    return data_v1beta.BetaAnalyticsDataClient(credentials=credentials)


def fetch_ga4_data(
    client: data_v1beta.BetaAnalyticsDataClient,
    property_id: str = "",
    start_date: date = date(2019, 1, 1),
) -> dict[str, ViewDataValue]:
    """
    Fetch some data from GA4.
    See: https://ga-dev-tools.google/ga4/query-explorer/
    """
    response: data_v1beta.RunReportRequest = client.run_report(
        {
            "property": f"properties/{property_id or os.environ['GC_PROPERTY_ID']}",
            "dimensions": [{"name": "pageTitle"}],
            "metrics": [{"name": "screenPageViews"}, {"name": "totalUsers"}],
            "date_ranges": [
                {"start_date": start_date.isoformat(), "end_date": "today"}
            ],
        }
    )
    metrics = [header.name for header in response.metric_headers]
    result: dict[str, ViewDataValue] = {}
    for row in response.rows:
        if len(row.dimension_values) != 1:
            raise ValueError(
                f"Received non-single dimensioned row: {row.dimension_values}"
            )
        path = row.dimension_values[0].value
        dummy: ViewDataValue = {"views": 0, "total_users": 0}
        for metric, metric_value in zip(metrics, row.metric_values):
            match metric:
                case "screenPageViews":
                    dummy["views"] = int(metric_value.value)
                case "totalUsers":
                    dummy["total_users"] = int(metric_value.value)
                case e:
                    raise ValueError(f"Invalid metric {e}")
        result[path] = dummy
    return result


def parse_ga4_cache(report_path: Path | str) -> dict[str, ViewDataValue]:
    """
    Yield values from run report.
    Used https://ga-dev-tools.google/ga4/query-explorer/.
    """
    with open(report_path) as raw_file:
        obj = json.load(raw_file)
    assert obj["dimensionHeaders"] == [{"name": "pageTitle"}]
    metrics: list[str] = [header["name"] for header in obj["metricHeaders"]]
    result: dict[str, ViewDataValue] = {}

    for row in obj["rows"]:
        dimension_values = row["dimensionValues"]
        metric_values = row["metricValues"]
        assert len(dimension_values) == 1
        title = dimension_values[0]["value"]
        dummy: ViewDataValue = {"total_users": 0, "views": 0}

        for metric, metric_value in zip(metrics, metric_values, strict=True):
            match metric:
                case "screenPageViews":
                    dummy["views"] = int(metric_value["value"])
                case "totalUsers":
                    dummy["total_users"] = int(metric_value["value"])
                case e:
                    raise ValueError(f"Invalid metric {e}")
        result[title] = dummy

    return result
