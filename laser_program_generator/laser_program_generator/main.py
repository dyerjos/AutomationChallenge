import typer


app = typer.Typer()


@app.callback()
def main():
    """
    Laser program generator
    """


@app.command()
def generate_program(pattern: str):
    """
    Given a desired output pattern as a string, this command generates a program to be executed by the laser cutter
    """

    typer.echo("Welcome!\n")
    typer.echo(
        "This program accepts a desired pattern as a string\n"
        "Input Example:\n"
        """
        ..XXX..
        XX...XX
        ..XXX..
        \n"""
    )

    typer.echo(f"You provided the following pattern:\n {pattern}")

    pattern_confirmed = typer.confirm("Is this your desired pattern?\n")
    if not pattern_confirmed:
        typer.echo("Aborting due to unconfirmed output pattern")
        raise typer.Abort()
