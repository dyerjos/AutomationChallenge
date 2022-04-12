import typer


app = typer.Typer()


@app.command()
def generate_program(pattern: str):
    """
    Given a desired output pattern, this command generates a program to be executed by the laser cutter
    """
    typer.echo("Generating machine program!")
