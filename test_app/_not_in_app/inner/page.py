def page() -> str:
    return (
        "This must not be included in the app because it's in an excluded package: "
        "there's a parent package whose name starts with an _ and does not end with _ "
        "(so no path parameter)."
    )
