from fasthx.htmy import CurrentRequest
from htmy import Context

from holm.module_options._metadata import Metadata


def default_text_processor(text: str, context: Context) -> str:
    """
    Default text processor for `Snippet` and `MD` components, that internally uses
    `str.format()` to format `text`.

    The standard `str.format()` syntax and escaping rules must be used in `text`,
    see the [documentation](https://docs.python.org/3/library/string.html#format-string-syntax)
    for more information.

    Supported replacement field in `text`:

    - `metadata`: The `Metadata` instance from the `htmy` context, which implements the
      `Mapping` protocol, so you can access its items using the `[]` operator. Example text:
      `<title>"{metadata[title]}"</title>`.
    - `request`: The current FastAPI `Request` from the `htmy` context. Example text:
      `<base href="{request.url.origin}/">`.

    Arguments:
        text: The text to process.
        context: The `htmy` context.

    Returns:
        The formatted text.
    """
    metadata = Metadata.from_context(context)
    request = CurrentRequest.from_context(context)
    return text.format(
        metadata=metadata,
        request=request,
    )
