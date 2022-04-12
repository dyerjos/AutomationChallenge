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

    # * function to validate the input as being a valid string
    # * function should also make sure that each row and column has the same number of elements
    # * exit early if not valid input
    # * might as well determine grid dimensions here as well

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

    # * function to parse the pattern string
    # * this function will determin cut mark coordinates and store them
