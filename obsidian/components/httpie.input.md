# httpie/input.py

## Classes

- `AuthCredentials`
  - `_getpass`
  - `has_password`
  - `prompt_password`
- `AuthCredentialsArgType`
  - `__call__`
- `DataDict`
  - `items`
- `HTTPieArgumentParser`
  - `__init__`
  - `_apply_config`
  - `_apply_no_options`
  - `_body_from_file`
  - `_guess_method`
  - `_parse_items`
  - `_print_message`
  - `_process_auth`
  - `_process_output_options`
  - `_process_pretty_options`
  - `_setup_standard_streams`
  - `_validate_download_options`
  - `parse_args`
- `KeyValue`
  - `__eq__`
  - `__init__`
  - `__repr__`
- `KeyValueArgType`
  - `__call__`
  - `__init__`
- `ParamsDict`
- `ParseError`
- `RequestItemsDict`
  - `__setitem__`
- `SessionNameValidator`
  - `__call__`
  - `__init__`

## Top-Level Functions

- `get_content_type`
- `parse_items`
- `readable_file_arg`

## Imports

- [[httpie.compat]]
- [[httpie.sessions]]
- [[httpie.utils]]

## Imported By

- [[httpie.cli]]
- [[httpie.output.streams]]
