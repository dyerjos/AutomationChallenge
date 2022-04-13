from typer.testing import CliRunner

from laser_program_generator.main import app

runner = CliRunner()


test_case_one = {
    "pattern": """
    ..XXX..
    XX...XX
    ..XXX..
    """,
    "ideal_runtime": 21.952,
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


def test_unconfirmed_output():
    result = runner.invoke(app, ["generate-program", "x"], input="n")
    assert result.exit_code == 1
    assert "Aborting due to unconfirmed output pattern" in result.stdout


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


# TODO: test all functions of main.py
# TODO: test generate_program() against the 3 provided test cases
