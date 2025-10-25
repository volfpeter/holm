::: holm.App
    options:
        show_root_heading: true

::: holm.Metadata
    options:
        show_root_heading: true
        filters:
            - "!__init__"
            - "!_metadata"

::: holm.ErrorHandlerMapping
    options:
        show_root_heading: true

::: holm.without_layout
    options:
        show_root_heading: true
        filters:
            - "!component"
