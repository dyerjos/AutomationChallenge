from typer.testing import CliRunner

from laser_program_generator.main import app

runner = CliRunner()


test_case_one = {
    "pattern": """
    ..XXX..
    XX...XX
    ..XXX..
    """,
    "run_time": 21.952,
}
test_case_two = {
    "pattern": """
    ....X....
    ..XXXXX..
    .........
    ..XXXXX..
    ....X....
    """,
    "run_time": 29.728,
}
test_case_three = {
    "pattern": """
    ......XXX
    ........X
    X...X...X
    X........
    XXX......
    """,
    "run_time": 29.903,
}


def test_unconfirmed_output():
    result = runner.invoke(app, ["generate-program", "x"], input="n")
    assert result.exit_code == 1
    assert "Aborting due to unconfirmed output pattern" in result.stdout


# TODO: test all functions of main.py
# TODO: test generate_program() against the 3 provided test cases
