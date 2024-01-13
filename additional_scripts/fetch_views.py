import argparse
import json
import os
from pathlib import Path
from typing import TypedDict

from google.analytics import data_v1beta
from google.oauth2 import service_account


class PathData(TypedDict):
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


def fetch_data(
    client: data_v1beta.BetaAnalyticsDataClient,
    property_id: str = "",
) -> dict[str, PathData]:
    """
    Fetch some data from GA4.
    See: https://ga-dev-tools.google/ga4/query-explorer/
    """
    response: data_v1beta.RunReportRequest = client.run_report(
        {
            "property": f"properties/{property_id or os.environ['GC_PROPERTY_ID']}",
            "dimensions": [{"name": "pageTitle"}],
            "metrics": [{"name": "screenPageViews"}, {"name": "totalUsers"}],
            "date_ranges": [{"start_date": "2019-01-01", "end_date": "today"}],
        }
    )
    metrics = [header.name for header in response.metric_headers]
    result: dict[str, PathData] = {}
    for row in response.rows:
        if len(row.dimension_values) != 1:
            raise ValueError(
                f"Received non-single dimensioned row: {row.dimension_values}"
            )
        path = row.dimension_values[0].value
        dummy: PathData = {"views": 0, "total_users": 0}
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-file", "-o", type=Path, required=True)
    parser.add_argument("--credential", "-c", type=Path, default=None)
    namespace = parser.parse_args()

    client = (
        get_client()
        if namespace.credential is None
        else data_v1beta.BetaAnalyticsDataClient(
            credentials=service_account.Credentials.from_service_account_file(
                namespace.credential
            )
        )
    )
    result = fetch_data(client)
    with open(namespace.json_file, "w") as file:
        json.dump(result, file)
