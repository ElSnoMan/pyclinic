import os
import click
from rich.console import Console
from pyclinic import postman

# TODO: Select theme
console = Console(theme=None)


@click.group()
@click.version_option()
def cli():
    """The pyclinic CLI."""
    pass


@cli.command()
@click.option("-i", "--input-file")
def generate_models(input_file):
    """Generate Pydantic Model files given the Postman Collection input file.

    Args:
        input_file (str): The path to the input file. This is relative to where this command is being executed.

    Outputs:
        The path(s) to the generated models.
    """
    if not os.path.exists(input_file):
        console.print(
            f":pile_of_poo: [bold red]No file found at the given path:[/bold red] [i yellow]{input_file}[/i yellow]"
        )
        exit(1)

    # TODO: Add try/catch for other possible errors
    collection = postman.load_postman_collection_from_file(input_file)
    folders = postman.map_response_bodies_to_folders(collection)
    written_path = postman.write_collection_models_to_files(folders)
    console.print(":smiley: SUCCESS!", style="bold green")
    console.print("Models written to:", list(set(written_path)))
