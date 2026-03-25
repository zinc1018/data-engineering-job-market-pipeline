from unittest.mock import MagicMock, patch

from src.ingest.ingestion_logging import log_ingestion_run


def test_log_ingestion_run_inserts_expected_fields():
    log_entry = {
        "source_type": "greenhouse",
        "board_tokens": ["airtable"],
        "record_count": 51,
        "output_path": "data/raw/greenhouse_job_postings.json",
        "fetched_at": "2026-03-25T12:00:00+00:00",
        "status": "success",
    }

    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    with patch("src.ingest.ingestion_logging.get_connection", return_value=mock_connection):
        log_ingestion_run(log_entry)

    assert mock_cursor.execute.call_count == 1
    args, _ = mock_cursor.execute.call_args
    assert "INSERT INTO raw.ingestion_runs" in args[0]
    assert args[1][0] == "greenhouse"
