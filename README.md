# Welcome to the PyClinic

Pyclinic is a library to make it easier and faster to get your Service Testing up and running!

Currently, PyClinic can integrate with Postman users so you can export a Postman Collection and use it to automatically generate python functions!

You can also genereate Pydantic Models by using the CLI:

```bash
pyclinic generate-models --input <postman_collection_path>
```

> 💡 This allows you to quickly write automation to work with many endpoints or even write automated tests against those endpoints!

## Simple Example

1. Export your Postman Collection (as `example.postman_collection.json`, for example)

2. Make an instance of `Postman` and pass in the file path to your JSON file

   ```python
   from pyclinic.postman import Postman

   runner = Postman("example.postman_collection.json")
   ```

3. Then call the endpoint function!

   ```python
   runner.Pets.list_all_pets()
   ```

## In-depth Example

When you instantiate `Postman()`, it converts the Postman Collection JSON and turns each request to an executable function!

Take this [Deck of Cards API Collection](https://github.com/ElSnoMan/pyclinic/blob/main/tests/examples/deckofcards.postman_collection.json) example. Here is what the folder structure looks like in Postman:

- Root
  - ↪️ Create shuffled deck
  - 📂 Folder 1
    - ↪ Reshuffle Deck
    - 📂 Folder 1.1
      - ↪️ Draw Cards
  - 📂 Folder 2
    - ↪️ List Cards in Piles

1. Make an instance of Postman

   ```python
   from pyclinic.postman import Postman

   runner = Postman("deckofcards.postman_collection.json")
   ```

2. To call the `Create shuffle deck` endpoint at the Collection Root, you would use

   ```python
   response = runner.Root.create_shuffled_deck()
   ```

3. Then do what you need with the Response!

   > 💡 pyclinic uses the `requests` library to make requests and to work with responses!

   ```python
   assert response.ok
   print(response.json())

   """
   Output:
   {
       "success": true,
       "deck_id": "3p40paa87x90",
       "shuffled": true,
       "remaining": 52
   }
   """
   ```

4. If you want to call the `Draw Cards` item under `Folder 1 > Folder 1.1`, then use:

   ```python
   response = runner.Folder11.draw_cards()
   ```

   > 💡 All folders in the Postman Collection are flattened, so you don't have to do `runner.Folder1.Folder11.draw_cards()`

### Normalizing Folder Names and Function Names

Observe how, in the last example with `runner.Folder11.draw_cards()`, each Postman item name is turned into Pythonic syntax:

- Folders are turned into classes, so `Folder 1` turns into `Folder1`
- Requests are turned into functions, so `Draw Cards` turns into `draw_cards`

### Work with them like normal functions

```python
def test_deckofcards_multiple_calls():
    runner = Postman("deckofcards.postman_collection.json")

    create_response = runner.Root.create_shuffled_deck()
    deck_id = create_response.json().get("deck_id")

    response = runner.Folder11.draw_cards({"deck_id": deck_id})
    assert response.ok
    assert len(response.json()["cards"]) == 2, "Should draw two cards from deck"
```

## Setup and Contribute

💡 Use `Poetry` as the package manager to take advantage of the `pyproject.toml` at the Workspace Root

> ⚠️ Python version 3.9 or higher is required

1. Clone/Fork this repo and open it in your favorite editor (VS Code, Pycharm, etc)

2. Open the Integrated Terminal and use Poetry to install all dependencies

   ```bash
   # this also creates the virtual environment automatically
   poetry install
   ```

3. Configure your IDE

   - Select Interpreter - Gives you autocomplete, intellisense, etc
   - Configure Tests - We use `pytest` instead of the default `unittest` library
   - Any other settings. This project uses a Formatter (`black`) and Linter (`flake8`)

4. That's it! Run the tests to see it all work

   ```bash
   poetry run poe test
   ```

5. Make your changes, then submit a Pull Request (PR) for review. This automatically triggers a pipeline that lints and runs tests. Once the pipeline is green, a **Maintainer** will review your PR! 😄

> Shoutout to @sudomaze from Twitch 💪🏽🐍
