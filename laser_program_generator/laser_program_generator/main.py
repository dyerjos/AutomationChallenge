import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Laser Program Generator
    """


@app.command()
def generate_program():
    """
    Given a desired output pattern, this command generates a program to be executed by the laser cutter
    """
    typer.echo("Generating machine program!")
