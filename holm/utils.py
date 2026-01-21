from collections.abc import Mapping
from typing import Any

from fasthx.htmy import CurrentRequest
from htmy import Component, Context, Slots, Snippet, Text, is_component_type
from htmy.typing import TextProcessor

from holm.module_options._metadata import Metadata
from holm.modules._layout import Layout


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


def snippet_to_layout(
    content: str,
    *,
    text_processor: TextProcessor = default_text_processor,
    default_slot_mapping: Mapping[str, Component] | None = None,
) -> Layout:
    """
    Converts the given string to a `Layout`.

    The created layout function internally uses a `Snippet` component with `Slots` for rendering.

    The slot handling logic depends on the "props" object the layout receives from the page or
    layout it directly wraps:

    - If "props" is a `Mapping` (and not an `htmy` `Component`), then it must map slot keys to
      the corresponding `htmy` components, and it is used directly as the slots definition
      of `Snippet`. This means `<!-- slot[key] -->` placeholders in `content` are replaced
      with the corresponding components from this mapping during rendering.
    - Otherwise the props object is assumed to be an `htmy` `Component` and it is assigned to the
      `children` slot, meaning the `<!-- slot[children] -->` placeholder in `content` is replaced
      with this component during rendering.

    The default text processor is `holm.utils.default_text_processor()`. It gives you access to
    the page `Metadata` and the current FastAPI `Request` through the `metadata` and `request`
    replacement field names. See its documentation for more details.

    Arguments:
        content: The string to convert.
        text_processor: The text processor for `Snippet` to pre-format `content`.
        default_slot_mapping: Default slots that should always be available in the layout during rendering.

    Returns:
        A `Layout` that renders the given string.
    """
    # Avoid doing the str to Text conversion on every request in the layout.
    text = Text(content)

    def layout(props: Any) -> Snippet:
        slot_mapping: Mapping[str, Component]
        if isinstance(props, Mapping) and not is_component_type(props):
            slot_mapping = props
        else:
            slot_mapping = {"children": props}

        return Snippet(
            text,
            Slots(
                slot_mapping
                if default_slot_mapping is None
                else {
                    **default_slot_mapping,
                    **slot_mapping,
                }
            ),
            text_processor=text_processor,
        )

    return layout
