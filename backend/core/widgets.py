import json
from django_json_widget.widgets import JSONEditorWidget

class SafeJSONEditorWidget(JSONEditorWidget):
    """
    A JSONEditorWidget that handles invalid JSON strings and empty values gracefully.
    Prevents the Django admin from crashing on malformed data.
    """
    def format_value(self, value):
        if value is None or value == "" or (isinstance(value, str) and not value.strip()):
            return []
        try:
            if isinstance(value, str):
                return json.loads(value)
            return value
        except (ValueError, TypeError, json.JSONDecodeError):
            # Fallback to empty list if parsing fails
            return []
