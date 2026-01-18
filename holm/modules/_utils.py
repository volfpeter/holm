from fasthx.htmy import CurrentRequest
from htmy import Context

from holm.module_options._metadata import Metadata


def default_text_processor(text: str, context: Context) -> str:
    """
    Default text processor for `Snippet` and `MD` components.

    Supported keys:
        metadata: The `Metadata` instance from the `htmy` context.
        request: The current FastAPI `Request` from the `htmy` context.

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
