from pyclinic.postman import Postman
from tests import utils


def test_folder_help():
    PATH = utils.build_example_path("deckofcards.postman_collection.json")
    runner = Postman(PATH)
    assert runner.Root.help() == ["create_shuffled_deck", "draw_cards", "reshuffle_deck", "list_cards_in_piles"]
    assert runner.Folder1.help() == ["reshuffle_deck"]
    assert runner.Folder11.help() == ["draw_cards"]
    assert runner.Folder2.help() == ["list_cards_in_piles"]


def test_runner_show_folders():
    PATH = utils.build_example_path("big-petstore.postman_collection.json")
    runner = Postman(PATH)
    runner.show_folders()


def test_runner_show_variables():
    GLOBAL_PATH = utils.WORKSPACE_GLOBAL_VARIABLES_PATH
    ENV_PATH = utils.BOOKSTORE_ENV_VARIABLES_PATH
    COLLECTION_PATH = utils.build_example_path(utils.BOOKSTORE_PATH)

    user_variables = {"USERNAME": "Carlos Kidman", "SHOW": "ME THE MONEY"}
    runner = Postman(COLLECTION_PATH, ENV_PATH, GLOBAL_PATH, user_variables)
    runner.show_variables()
