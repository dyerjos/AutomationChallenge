from typer.testing import CliRunner

from laser_program_generator import main

runner = CliRunner()

# TODO: figure out why tests can't run (AttributeError: module 'laser_program_generator.main' has no attribute '_add_completion')


def test_app():
    result = runner.invoke(
        main,
        [
            """
        ..XXX..
        XX...XX
        ..XXX..
        """
        ],
    )

    assert result.exit_code == 0


# TODO: test all functions of main.py
# TODO: test generate_program() against the 3 provided test cases
