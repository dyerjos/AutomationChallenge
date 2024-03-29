import math
import random

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
    Given a desired output pattern as a string,
    this command generates a program to be executed by the laser cutter
    """
    cleaned_pattern = pattern.strip().replace(" ", "").casefold().upper()
    pattern_substrings = cleaned_pattern.split("\n")

    typer.echo("Welcome!\n")

    validate_input(cleaned_pattern)
    validate_grid(pattern_substrings)

    typer.echo(
        "This program accepts a pattern as a string\n"
        "Input Example:\n"
        """
        ..XXX..
        XX...XX
        ..XXX..
        \n"""
    )

    typer.echo(f"You provided the following pattern:\n {pattern}")

    pattern_confirmed = typer.confirm("Is this pattern correct?\n")
    if not pattern_confirmed:
        typer.echo("Aborting due to unconfirmed output pattern")
        raise typer.Exit(code=1)

    cut_coordinates = get_cut_coordinates(pattern_substrings)

    laser_instructions = get_laser_instructions(cut_coordinates)

    for line in laser_instructions:
        typer.echo(line)

    raise typer.Exit()


@app.command()
def generate_blank_grid(rows: int, columns: int):
    """
    Given a row length and a column length, this command generates a blank grid as a string
    """
    typer.echo(f"rows needed: {rows}")
    typer.echo(f"columns needed: {columns}")
    pattern_string = ""
    for row in range(rows):
        for col in range(columns):
            pattern_string += "."
        pattern_string += "\n"

    typer.echo(pattern_string)
    raise typer.Exit()


@app.command()
def generate_random_grid_pattern(rows: int, columns: int, cuts: int):
    """
    Given a row length, a column length and desired number of cuts,
    this command generates a random grid as a string
    """
    typer.echo(f"rows needed: {rows}")
    typer.echo(f"columns needed: {columns}")
    typer.echo(f"cuts needed: {cuts}")
    total_units = rows * columns
    typer.echo(f"total_units: {total_units}\n")
    if cuts > total_units:
        typer.echo("There are more cuts than spaces in this grid. Now exiting.")
        typer.Exit(code=1)
    blank_spaces = total_units - cuts
    char_pool = blank_spaces * ["."] + cuts * ["X"]
    random.shuffle(char_pool)

    pattern_string = ""
    for row in range(rows):
        for col in range(columns):
            pattern_string += char_pool.pop()
        pattern_string += "\n"

    typer.echo(pattern_string)
    raise typer.Exit()


#  ======== validation functions ===========================


def validate_input(cleaned_pattern):
    ALLOWED_INPUT_CHARACTERS = set({"\n", ".", "X"})
    unique_char = set(cleaned_pattern)
    invalid_char = unique_char.difference(ALLOWED_INPUT_CHARACTERS)
    if invalid_char:
        typer.echo(f"The following invalid characters were found: {invalid_char}")
        typer.echo("Now aborting. Please try again without invalid characters")
        raise typer.Exit(code=1)


def validate_grid(pattern_substrings):
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


#  ======== grid processing functions ===========================


def get_cut_coordinates(pattern_strings):
    cut_coordinates = []
    x = 0.00
    y = 0.00
    for row in pattern_strings:
        for char in row:
            if char == "X":
                cut_coordinates.append([x, y])
            x += 1.00
        y += 1.00  # go to next row in grid
        x = 0.00  # each row begins at 0 for x coordinate

    if not cut_coordinates:
        typer.echo("There are no marks to cut so you are done. Now exiting.")
        raise typer.Exit()
    typer.echo(f"{len(cut_coordinates)} cuts found in pattern\n")

    return cut_coordinates


def get_laser_instructions(cut_coordinates):
    machine_instructions = []
    run_time = 0.0
    laser_coordinate = [0.0, 0.0]
    laser_active = False
    target = None
    distance_to_target = None

    def ensure_laser_active(run_time, laser_active):
        if not laser_active:
            machine_instructions.append("M01")
            run_time += 1.0
            laser_active = True
        return run_time, laser_active

    def ensure_laser_inactive(run_time, laser_active):
        if laser_active:
            machine_instructions.append("M01")
            run_time += 1.0
            laser_active = False
        return run_time, laser_active

    def coordinate_is_cut(laser_coordinate):
        cut_coordinates.remove(laser_coordinate)
        target = None
        return target

    def shut_off_sequence(run_time, laser_active):
        run_time, laser_active = ensure_laser_inactive(run_time, laser_active)
        laser_resting_coordinate = [0.0, 0.0]
        distance_to_origin = math.dist(laser_coordinate, laser_resting_coordinate)
        run_time, _, laser_active = move_laser_to_target(
            distance_to_origin, laser_resting_coordinate, run_time, laser_active
        )
        return run_time, laser_active

    def get_next_target(cut_coordinates, laser_coordinate):
        next_target = None
        best_distance_to_laser = None
        for cut_coordinate in cut_coordinates:
            distance_to_laser = math.dist(laser_coordinate, cut_coordinate)
            if not next_target or distance_to_laser < best_distance_to_laser:
                next_target = cut_coordinate
                best_distance_to_laser = distance_to_laser
        return next_target, best_distance_to_laser

    def move_laser_to_target(distance_to_target, target, run_time, laser_active):
        if distance_to_target > 1.0:
            run_time, laser_active = ensure_laser_inactive(run_time, laser_active)
        run_time += distance_to_target
        new_laser_coordinate = target
        machine_instructions.append(f"G01 X{target[0]}0 Y{target[1]}0")
        return run_time, new_laser_coordinate, laser_active

    while cut_coordinates:
        if laser_coordinate in cut_coordinates:
            run_time, laser_active = ensure_laser_active(run_time, laser_active)
            target = coordinate_is_cut(laser_coordinate)
        else:
            if not target:
                target, distance_to_target = get_next_target(
                    cut_coordinates, laser_coordinate
                )
            run_time, laser_coordinate, laser_active = move_laser_to_target(
                distance_to_target, target, run_time, laser_active
            )

    run_time, laser_active = shut_off_sequence(run_time, laser_active)
    typer.echo(f"Runtime of program: {run_time:.3f}\n")
    return machine_instructions
