def page() -> str:
    return "This page has no metadata."


rendered_page = """
<!DOCTYPE html><html >
<head >
<title >App</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body class="container-fluid">
<header class="container">
<p >Root layout header</p>
</header>
<main class="container">
This page has no metadata.
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()
