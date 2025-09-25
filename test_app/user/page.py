from htmy import ComponentType, html


def metadata(page_variant: str = "default") -> dict[str, str]:
    return {"title": f"Users page | {page_variant}"}


def page(page_variant: str = "default") -> dict[str, ComponentType]:
    return {
        "main": html.ul(
            html.li("User 1"),
            html.li("User 2"),
            html.li("User 3"),
        ),
        "footer": html.div(
            html.p("Footer content"),
        ),
    }


rendered_page_dense_layout_grid = """
<!DOCTYPE html><html >
<head >
<title >Users page | dense</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body class="container-fluid">
<header class="container">
<p >Root layout header</p>
</header>
<main class="container">
<div >
<p >user layout, variant: grid</p>
<div >
Main content:
</div>
<ul >
<li >User 1</li>
<li >User 2</li>
<li >User 3</li>
</ul>
<div >
footer
</div>
<div >
<p >Footer content</p>
</div>
</div>
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()
