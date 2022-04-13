from typer.testing import CliRunner

from laser_program_generator.main import (
    app,
    get_cut_coordinates,
    get_laser_instructions,
)

runner = CliRunner()


test_case_one = {
    "pattern": """
    ..XXX..
    XX...XX
    ..XXX..
    """,
    "ideal_runtime": 21.952,
    "pattern_substrings": ["..XXX..", "XX...XX", "..XXX.."],
    "cut_coordinates": [
        [2.0, 0.0],
        [3.0, 0.0],
        [4.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
        [5.0, 1.0],
        [6.0, 1.0],
        [2.0, 2.0],
        [3.0, 2.0],
        [4.0, 2.0],
    ],
}
test_case_two = {
    "pattern": """
    ....X....
    ..XXXXX..
    .........
    ..XXXXX..
    ....X....
    """,
    "ideal_runtime": 29.728,
}
test_case_three = {
    "pattern": """
    ......XXX
    ........X
    X...X...X
    X........
    XXX......
    """,
    "ideal_runtime": 29.903,
}
pattern_with_invalid_characters = {
    "pattern": """
    .m....XXX
    ...9....X
    X...O...X
    X....3...
    XXX......
    """,
}
pattern_with_invalid_grid = {
    "pattern": """
    ......XXX
    ..
    X...X...X
    X....
    XXX......
    """,
}


def test_pattern_one():
    result = runner.invoke(
        app, ["generate-program", test_case_one["pattern"]], input="y"
    )
    assert result.exit_code == 0
    assert "Runtime of program: 22.893" in result.stdout


def test_pattern_two():
    result = runner.invoke(
        app, ["generate-program", test_case_two["pattern"]], input="y"
    )
    assert result.exit_code == 0
    assert "Runtime of program: 29.543" in result.stdout


def test_pattern_three():
    result = runner.invoke(
        app, ["generate-program", test_case_three["pattern"]], input="y"
    )
    assert result.exit_code == 0
    assert "Runtime of program: 29.903" in result.stdout


def test_unconfirmed_output():
    result = runner.invoke(app, ["generate-program", "x"], input="n")
    assert result.exit_code == 1
    assert "Aborting due to unconfirmed output pattern" in result.stdout


def test_input_validation():
    result = runner.invoke(
        app, ["generate-program", pattern_with_invalid_characters["pattern"]], input="y"
    )
    assert result.exit_code == 1
    assert "The following invalid characters were found:" in result.stdout


def test_grid_validation():
    result = runner.invoke(
        app, ["generate-program", pattern_with_invalid_grid["pattern"]], input="y"
    )
    assert result.exit_code == 1
    assert "first row of grid has 9 columns but this row only has 2" in result.stdout


def test_get_cut_coordinates():
    assert (
        get_cut_coordinates(test_case_one["pattern_substrings"])
        == test_case_one["cut_coordinates"]
    )
