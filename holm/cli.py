"""holm command-line interface."""

import importlib.resources
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Literal, TypeAlias, cast

import typer
from rich.prompt import Prompt

from . import __version__

_JsManager: TypeAlias = Literal["npm", "pnpm", "bun"]

_JS_MANAGERS: tuple[_JsManager, ...] = ("bun", "pnpm", "npm")

_JS_RUNNER: dict[_JsManager, str] = {"npm": "npx", "pnpm": "pnpm dlx", "bun": "bunx"}


class Tokens:
    project_name = "__holm_name__"
    js_runner = "__holm_js_runner__"

    @classmethod
    def render(cls, text: str, *, project_name: str, js_runner: str) -> str:
        return text.replace(cls.project_name, project_name).replace(cls.js_runner, js_runner)


app = typer.Typer(
    name="holm", no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]}
)


@app.command()
def version() -> None:
    """Print the holm version."""
    typer.echo(f"holm {__version__}")


@app.command()
def new(
    name: Annotated[str | None, typer.Argument(help="Project name; directory to create under cwd.")] = None,
    js: Annotated[_JsManager | None, typer.Option("--js", help="JavaScript package manager.")] = None,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Accept defaults without prompting.")] = False,
) -> None:
    """Scaffold a new holm application."""
    _new(name=name, js=js, yes=yes)


def _fail(message: str) -> None:
    typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(1)


def _resolve_name(name: str | None, *, is_tty: bool, yes: bool) -> str:
    if name is None:
        if not is_tty:
            _fail("NAME is required when stdin is not a TTY; there is no default name.")
        if yes:
            _fail("--yes requires NAME; there is no default name.")
        name = typer.prompt("Project name")
    if not name or "/" in name or name in (".", ".."):
        _fail("NAME must be a single path segment: non-empty, no '/', not '.' or '..'.")
    return name


def _resolve_js(js: _JsManager | None, *, is_tty: bool, yes: bool) -> _JsManager:
    if js is not None:
        return js
    if is_tty and not yes:
        choice: str = Prompt.ask(
            "JavaScript package manager",
            choices=list(_JS_MANAGERS),
            default="bun",
            case_sensitive=False,
        )
        return cast("_JsManager", choice)
    typer.echo("JavaScript package manager: bun (default)")
    return "bun"


def _require_tools(js: _JsManager) -> None:
    missing = [tool for tool in ("uv", "git", js) if shutil.which(tool) is None]
    if missing:
        _fail(f"required tool(s) not found on PATH: {', '.join(missing)}")


def _resolve_target(name: str) -> Path:
    target = Path.cwd() / name
    if target.exists():
        if target.is_file():
            _fail(f"{target} exists and is a file.")
        if any(target.iterdir()):
            _fail(f"{target} exists and is not empty.")
    return target


def _new(name: str | None, js: _JsManager | None, yes: bool) -> None:
    is_tty = sys.stdin.isatty()
    project_name = _resolve_name(name, is_tty=is_tty, yes=yes)
    js_manager = _resolve_js(js, is_tty=is_tty, yes=yes)
    _require_tools(js_manager)
    target = _resolve_target(project_name)
    js_runner = _JS_RUNNER[js_manager]
    _copy_templates(target, project_name=project_name, js_runner=js_runner)

    _run(["git", "init"], cwd=target)
    _run(
        [
            "uv",
            "add",
            "fastapi[standard]",
            "holm",
            "htmy[all]",
            "pydantic-settings",
        ],
        cwd=target,
    )
    _run(["uv", "add", "--dev", "mypy", "poethepoet", "ruff", "watchfiles", "honcho"], cwd=target)
    _run(
        [
            js_manager,
            "add",
            "-D",
            "tailwindcss",
            "@tailwindcss/cli",
            "esbuild",
            "basecoat-css",
            "htmx.org@4.0.0-beta6",
        ],
        cwd=target,
    )
    _run(["uvx", "htmui", "init", "--force"], cwd=target)
    _build_css(target, js_runner, "static/app.css", minify=True)
    _build_js(target, js_runner, "static/app.js", minify=True)
    _run(["uv", "run", "poe", "format-fix"], cwd=target)
    _run(["uv", "run", "poe", "lint-fix"], cwd=target)
    _run(["uv", "run", "poe", "check"], cwd=target)

    typer.echo(
        f"""Created {project_name}.

  cd {project_name}
  uv run poe start          # http://localhost:5100"""
    )


def _template_dir() -> Path:
    return cast("Path", importlib.resources.files("holm") / "templates")


def _copy_templates(target: Path, *, project_name: str, js_runner: str) -> None:
    source = _template_dir()
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if ".ruff_cache" in path.relative_to(source).parts:
            continue
        dest = target / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            Tokens.render(path.read_text(encoding="utf-8"), project_name=project_name, js_runner=js_runner)
        )


def _build_css(target: Path, js_runner: str, output: str, *, minify: bool) -> None:
    args = [*js_runner.split(), "@tailwindcss/cli", "-i", "css/app.css", "-o", output]
    if minify:
        args.append("--minify")
    _run(args, cwd=target)


def _build_js(target: Path, js_runner: str, output: str, *, minify: bool) -> None:
    args = [*js_runner.split(), "esbuild", "js/app.js", "--bundle", f"--outfile={output}"]
    if minify:
        args.append("--minify")
    _run(args, cwd=target)


def _run(args: list[str], cwd: Path) -> None:
    typer.echo(f"$ {' '.join(args)}")
    try:
        subprocess.run(args, cwd=cwd, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        _fail(f"command failed with exit code {e.returncode}: {' '.join(args)}")
