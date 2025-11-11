"""Command-line interface."""

import typer


app: typer.Typer = typer.Typer()


@app.command(name="dmi-palette")
def main() -> None:
    """DMI Palette."""


if __name__ == "__main__":
    app()  # pragma: no cover
