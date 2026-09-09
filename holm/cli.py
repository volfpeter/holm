"""holm command-line interface."""

import importlib.resources
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Literal, TypeAlias, cast

import typer
from rich.prompt import Prompt

from . import __version__

_JsManager: TypeAlias = Literal["npm", "pnpm", "bun"]

_NAME_PATTERN = re.compile(r"[a-z][a-z0-9_-]*")

_NAME_RULES = (
    "must start with a lowercase letter, and may only contain lowercase letters, digits, '-', and '_'"
)

_JS_MANAGERS: tuple[_JsManager, ...] = ("bun", "pnpm", "npm")

_JS_RUNNER: dict[_JsManager, str] = {"npm": "npx", "pnpm": "pnpm dlx", "bun": "bunx"}

_JS_BUNDLER: dict[_JsManager, str] = {
    "npm": "npx esbuild --bundle",
    "pnpm": "pnpm dlx esbuild --bundle",
    "bun": "bun build",
}


class Tokens:
    project_name = "__holm_name__"
    js_runner = "__holm_js_runner__"
    js_bundler = "__holm_js_bundler__"

    @classmethod
    def render(cls, text: str, *, project_name: str, js_runner: str, js_bundler: str) -> str:
        return (
            text.replace(cls.project_name, project_name)
            .replace(cls.js_runner, js_runner)
            .replace(cls.js_bundler, js_bundler)
        )


app = typer.Typer(
    name="holm", no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]}
)

skill_app = typer.Typer(no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]})
app.add_typer(skill_app, name="skill", help="Manage agent skills.")


@skill_app.command("add")
def skill_add(
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing skill.")] = False,
) -> None:
    """Add the holm-web agent skill to the current project."""
    _add_skill(Path.cwd(), force=force)


@app.command()
def version() -> None:
    """Print the holm version."""
    typer.echo(f"holm {__version__}")


@app.command()
def new(
    name: Annotated[str | None, typer.Argument(help="Project name; directory to create under cwd.")] = None,
    js: Annotated[
        _JsManager | None,
        typer.Option("--js", help="JavaScript package manager: bun, pnpm, or npm (default: bun)."),
    ] = None,
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Accept defaults without prompting; NAME is required.")
    ] = False,
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
        while not _is_valid_name(name):
            typer.echo(f"Error: project name {_NAME_RULES}.", err=True)
            name = typer.prompt("Project name")
    if not _is_valid_name(name):
        _fail(f"NAME {_NAME_RULES}.")
    return name


def _is_valid_name(name: str) -> bool:
    return _NAME_PATTERN.fullmatch(name) is not None


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
    js_bundler = _JS_BUNDLER[js_manager]
    try:
        _scaffold(
            target,
            project_name=project_name,
            js_manager=js_manager,
            js_runner=js_runner,
            js_bundler=js_bundler,
        )
    except typer.Exit:
        typer.echo(f"\nThe incomplete project was left in {target}.", err=True)
        raise

    typer.echo(
        f"""Created {project_name}.

  cd {project_name}
  uv run poe start          # http://localhost:5000"""
    )


def _scaffold(
    target: Path, *, project_name: str, js_manager: _JsManager, js_runner: str, js_bundler: str
) -> None:
    _copy_templates(target, project_name=project_name, js_runner=js_runner, js_bundler=js_bundler)
    _add_skill(target, force=False)

    _run(["git", "init"], cwd=target)
    _run(["uv", "add", "fastapi[standard]", "holm", "htmy[all]", "pydantic-settings"], cwd=target)
    _run(["uv", "add", "--dev", "mypy", "poethepoet", "ruff", "watchfiles", "honcho"], cwd=target)
    _run(
        [
            js_manager,
            "add",
            "-D",
            "tailwindcss@^4",
            "@tailwindcss/cli@^4",
            "basecoat-css@^1",
            "htmx.org@^4",
            *([] if js_manager == "bun" else ["esbuild"]),
        ],
        cwd=target,
    )
    _run(["uvx", "htmui", "init", "--force"], cwd=target)
    _build_css(target, js_runner, "static/app.css")
    _build_js(target, js_bundler, "static/app.js")
    _run(["uv", "run", "poe", "format-fix"], cwd=target)
    _run(["uv", "run", "poe", "lint-fix"], cwd=target)
    _run(["uv", "run", "poe", "check"], cwd=target)


def _resource_dir() -> Path:
    return cast("Path", importlib.resources.files("holm") / "resources")


def _copy_templates(target: Path, *, project_name: str, js_runner: str, js_bundler: str) -> None:
    source = _resource_dir() / "app_template"
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if ".ruff_cache" in path.relative_to(source).parts:
            continue
        dest = target / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            Tokens.render(
                path.read_text(encoding="utf-8"),
                project_name=project_name,
                js_runner=js_runner,
                js_bundler=js_bundler,
            )
        )


def _add_skill(target: Path, *, force: bool) -> None:
    source = _resource_dir() / "skills" / "holm-web"
    dest = target / ".agents" / "skills" / "holm-web"
    if dest.exists():
        if not force:
            _fail(f"{dest} already exists, use --force to overwrite.")
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def _build_css(target: Path, js_runner: str, output: str) -> None:
    _run(
        [*js_runner.split(), "@tailwindcss/cli", "-i", "assets/app.css", "-o", output, "--minify"],
        cwd=target,
    )


def _build_js(target: Path, js_bundler: str, output: str) -> None:
    _run([*js_bundler.split(), "assets/app.js", f"--outfile={output}", "--minify"], cwd=target)


def _run(args: list[str], cwd: Path) -> None:
    typer.echo(f"$ {' '.join(args)}")
    try:
        subprocess.run(args, cwd=cwd, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        _fail(f"command failed with exit code {e.returncode}: {' '.join(args)}")
