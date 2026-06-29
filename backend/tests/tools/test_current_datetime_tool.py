from datetime import datetime

from app.tools.current_datetime_tool import CurrentDateTimeTool


def test_run_returns_an_iso_formatted_utc_timestamp():

    result = CurrentDateTimeTool().run()

    assert datetime.fromisoformat(result).utcoffset().total_seconds() == 0
