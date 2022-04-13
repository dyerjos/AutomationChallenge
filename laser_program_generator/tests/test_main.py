from typer.testing import CliRunner

from laser_program_generator.main import app

runner = CliRunner()


test_pattern_one = """
    ..XXX..
    XX...XX
    ..XXX..
    """


def test_app():
    result = runner.invoke(app, ["generate-program", test_pattern_one], input="y")
    assert result.exit_code == 0


# TODO: test all functions of main.py
# TODO: test generate_program() against the 3 provided test cases
