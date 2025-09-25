from htmy import Component, html

# Static metadata
metadata = {"title": "Index page"}


async def page() -> Component:
    """Async page that returns a component sequence."""
    return (html.div(html.h1("Index page")),)


rendered_page = """
<!DOCTYPE html><html >
<head >
<title >Index page</title>
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
<h1 >Index page</h1>
</div>
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()
