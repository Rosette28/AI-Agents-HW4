# httpie/downloads.py

## Role

Implements `--download` mode: `Download`/`ProgressReporterThread` manage the
file write + progress bar. **Sets `Accept-Encoding: None` on the request
headers to disable gzip** - this `None` is what crashes
[[httpie.sessions]]'s `Session.update_headers` for Bug #3 (see [[hot]]).

**Navigation:** [[index]] | [[hot]]

## Classes

- `ContentRangeError`
- `Download`
  - `__init__`
  - `chunk_downloaded`
  - `failed`
  - `finish`
  - `interrupted`
  - `pre_request`
  - `start`
- `ProgressReporterThread`
  - `__init__`
  - `report_speed`
  - `run`
  - `stop`
  - `sum_up`
- `Status`
  - `__init__`
  - `chunk_downloaded`
  - `finished`
  - `has_finished`
  - `started`

## Top-Level Functions

- `filename_from_content_disposition`
- `filename_from_url`
- `get_unique_filename`
- `parse_content_range`

## Imports

- [[httpie.compat]]
- [[httpie.models]]
- [[httpie.output.streams]]
- [[httpie.utils]]

## Imported By

- [[httpie.core]]
