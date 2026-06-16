def explain() -> str:
    return """
Root Cause:

Session.update_headers()
calls value.decode('utf8')
without verifying that value is not None.

downloads.py sets:

Accept-Encoding = None

This value propagates through:

downloads.py
-> client.py::get_response()
-> Session.update_headers()

which causes:

AttributeError:
'NoneType' object has no attribute 'decode'
"""