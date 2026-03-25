from src.ingest.live_source_connector import ExampleConnector


def test_example_connector_returns_records():
    connector = ExampleConnector()

    records = connector.fetch_job_postings()

    assert len(records) >= 1
    assert records[0].source == "example_live_source"
    assert records[0].title is not None
