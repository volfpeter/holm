from dataclasses import dataclass

from htmy import Component, Context, html


async def metadata(id: str) -> dict[str, str]:
    return {
        "title": f"User {id}",
    }


@dataclass(frozen=True, slots=True, kw_only=True)
class page:
    """The generated `__init__()` method can be used as a FastAPI dependency."""

    id: str
    page_variant: str = "default"

    async def htmy(self, _: Context) -> Component:
        return html.div(
            html.h1(f"User {self.id}"),
            html.p(f"This is the user page for {self.id}."),
            html.p(f"Requested page variant is {self.page_variant}."),
        )


rendered_page_dense_layout_grid_eric = """
<!DOCTYPE html><html >
<head >
<title >User eric</title>
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
<div >
<h1 >User eric</h1>
<p >This is the user page for eric.</p>
<p >Requested page variant is dense.</p>
</div>
<div >
footer
</div>
<div >
<p >footer for user ID eric, added by layout</p>
</div>
</div>
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()
