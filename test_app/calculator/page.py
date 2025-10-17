metadata = {"title": "Calculator"}


def page() -> str:
    return "Calculator"


def handle_submit() -> str:
    return "Calculator, submit handler"


rendered_page = """
<!DOCTYPE html><html >
<head >
<title >Calculator</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body class="container-fluid">
<header class="container">
<p >Root layout header</p>
</header>
<main class="container">
Calculator
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()

rendered_submit_handler = """
<!DOCTYPE html><html >
<head >
<title >Calculator</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body class="container-fluid">
<header class="container">
<p >Root layout header</p>
</header>
<main class="container">
Calculator, submit handler
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()
