import typer


app = typer.Typer()


@app.callback()
def main():
    """
    Laser program generator
    """


@app.command()
# def generate_program(pattern: str):
# TODO: remove default when done testing
def generate_program(
    pattern: str = typer.Argument(
        """
    X....
    .XX..
    ..XX.
    ....X
    """
    ),
):
    """
    Given a desired output pattern as a string, this command generates a program to be executed by the laser cutter
    """
    cleaned_pattern = pattern.strip().replace(" ", "").casefold().upper()
    pattern_substrings = cleaned_pattern.split("\n")

    validate_input(cleaned_pattern)

    # typer.echo("Welcome!\n")
    # typer.echo(
    #     "This program accepts a desired pattern as a string\n"
    #     "Input Example:\n"
    #     """
    #     ..XXX..
    #     XX...XX
    #     ..XXX..
    #     \n"""
    # )

    # typer.echo(f"You provided the following pattern:\n {pattern}")

    # pattern_confirmed = typer.confirm("Is this your desired pattern?\n")
    # if not pattern_confirmed:
    #     typer.echo("Aborting due to unconfirmed output pattern")
    #     raise typer.Exit(code=1)

    # # * function to parse the pattern string
    # # * this function will determin cut mark coordinates and store them

    # typer.echo("program exiting without errors")
    raise typer.Exit()


#  ======== helper functions ===========================


def validate_input(pattern):
    validate_characters(cleaned_pattern)
    validate_grid(pattern_substrings)


def validate_characters(cleaned_pattern):
    ALLOWED_INPUT_CHARACTERS = set({"\n", ".", "X"})
    unique_char = set(cleaned_pattern)
    invalid_char = unique_char.difference(ALLOWED_INPUT_CHARACTERS)
    if invalid_char:
        typer.echo(f"The following invalid characters were found: {invalid_char}")
        typer.echo("Now aborting. Please try again without invalid characters")
        raise typer.Exit(code=1)


def validate_and_prep_grid(pattern_substrings):
    row_count = 0
    expected_columns = None
    for line in pattern_substrings:
        row_count += 1
        columns_in_line = len(line)
        if not expected_columns:
            expected_columns = columns_in_line
            continue
        if expected_columns != columns_in_line:
            typer.echo(
                f"first row of grid has {expected_columns} columns but this row only has {columns_in_line}. This program requires all rows to have the same number of columns. Please fix your input. Now aborting"
            )
            raise typer.Exit(code=1)

    typer.echo(f"grid is {expected_columns}x{row_count}")
