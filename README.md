# Welcome to the PyClinic

PyClinic is a library to make it easier and faster to get your Service Testing up and running!

- [Quickstart](#quickstart)
- [OpenApi3 Demo (Swagger 2 is identical)](#openapi3-demo-notebook)
- [In-Depth Postman Example](#in-depth-postman-example)
- [Automated Test Example](#automated-test-example)
- [Working with Postman Variables](#working-with-postman-variables)
- [Setup and Contribute](#setup-and-contribute)

PyClinic supports Postman Collections and OpenAPI3 Spec files and can auto-generate functions using just the file!

> 💡 This allows you to quickly write automation to work with many endpoints or even write automated tests against those endpoints!

---

## Quickstart

1. Export your Collection from Postman (as `example.postman_collection.json`, for example)

2. Install PyClinic with your preferred Package Manager

   ```bash
   pip install pyclinic
   ```

3. Make an instance of `Postman` and pass in the file path to your JSON file.

   > 💡 You will see the instance commonly referred to as `runner`

   ```python
   from pyclinic.postman import Postman

   runner = Postman("example.postman_collection.json")
   ```

4. Then call the endpoint function and do something with the response!

   ```python
   response = runner.Pets.list_all_pets()
   assert response.ok
   print(response.json())
   ```

5. The process is the same for a Swagger2 or OpenApi3 Spec File, but you use the `Swagger` or `OpenApi` class instead

   ```python
   from pyclinic.openapi import OpenApi

   runner = OpenApi("path-to-spec-file.yml")
   response = runner.Pets.list_all_pets()
   assert response.ok
   print(response.json())
   ```

---

## OpenApi3 Demo Notebook (Swagger2 experience is identical)

> Open our [demo_openapi3_runner.ipynb](./demo_openapi3_runner.ipynb) for a Jupyter Notebook experience of how to use PyClinic.

## In-Depth Postman Example

> Open our [demo_postman_runner.ipynb](./demo_postman_runner.ipynb) for a Jupyter Notebook experience of how to use PyClinic.

When you instantiate `Postman()`, it converts the Postman Collection JSON and turns each request into an executable function.

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

2. To call the `Create shuffle deck` function at the Collection Root, you would use

   ```python
   response = runner.Root.create_shuffled_deck()
   ```

3. Then do what you need with the Response!

   > 💡 pyclinic uses the `requests` library to make requests and to work with responses!

   ```python
   assert response.ok
   print(response.json())

   """ Output:
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

5. You can see all folders and functions that can be used with the `show_folders` function

   ```python
   runner.show_folders()
   ```

   ```python
   # or use .help() to see which functions belong to a folder
   runner.Folder1.help()
   ```

### Folder Names and Function Names are normalized

Observe how, in the last example with `runner.Folder11.draw_cards()`, each Postman item name is turned into Pythonic syntax:

- Folders are turned into classes, so `Folder 1` turns into `Folder1`
- Requests are turned into functions, so `Draw Cards` turns into `draw_cards`

---

## Automated Test Example

```python
def test_deckofcards_multiple_calls():
    runner = Postman("deckofcards.postman_collection.json")

    create_response = runner.Root.create_shuffled_deck()
    deck_id = create_response.json().get("deck_id")

    response = runner.Folder11.draw_cards({"deck_id": deck_id})
    assert response.ok
    assert len(response.json()["cards"]) == 2, "Should draw two cards from deck"
```

## Working with Postman Variables

Postman has 3 layers of Variables, but we've added a 4th:

1. Global
2. Environment
3. Collection
4. User

`Collection Variables` come as part of your collection when you export it. However, `Global` and `Environment` variables must be exported separately.

When instantiating a Postman runner, you can pass in the paths to these exported Variables files to include them.

```python
def test_runner_show_variables():
   user_variables = {"USERNAME": "Carlos Kidman", "SHOW": "ME THE MONEY"}
   runner = Postman(COLLECTION_PATH, ENV_PATH, GLOBAL_PATH, user_variables)
   runner.show_variables()

   """ Output:
   {
    'NAME': {'value': 'CARLOS KIDMAN', 'enabled': True},
    'BASE_URL': {'value': 'https://demoqa.com', 'enabled': True},
    'USER_ID': {'value': '', 'enabled': True},
    'USERNAME': {'value': 'Carlos Kidman', 'enabled': True},
    'PASSWORD': {'value': '', 'enabled': True},
    'TOKEN': {'value': '', 'enabled': True},
    'SHOW': {'value': 'ME THE MONEY', 'enabled': True}
   }
   """
```

> NOTE: User Variables are defined as a flat dictionary with the key-value pairs you want. These will override values if they already exist, or add them if they don't.

You can use the `.show_variables()` method to display the variables that the Postman runner has been instantiated with.

Finally, you can use the `.help()` method on the executable function to see the raw request dictionary that is being used. This is extremely helpful when needing more details about the request function you're dealing with.

```python
runner = Postman("bookstore.postman_collection.json")
runner.Account.create_user.help()

""" Output:
{
    'method': 'POST',
    'url': 'https://demoqa.com/Account/v1/User',
    'data': {'userName': '{{$randomFullName}}', 'password': 'P@$$w0rd'},
    'headers': {}
}
"""
```

## TIPS

Instantiate the Postman runner at the top of the file and use the show methods to display info. This way you can see the folders and the variables that you have at the beginning of the program or test run:

```python
from pyclinic.postman import Postman


runner = Postman(BOOKSTORE_PATH, BOOKSTORE_ENV_VARIABLES_PATH)
runner.show_folders()
runner.show_variables()

def create_user(credentials: Dict) -> Dict:
    response = runner.Account.create_user(data=credentials)
    return response.json()

...
```

---

## Setup and Contribute

💡 Use `Poetry` as the package manager to take advantage of the `pyproject.toml` at the Workspace Root

> ⚠️ Python version 3.7 or higher is required

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

---

### Twitch Shoutouts 💪🏽🐍

I have been building this entirely while streaming on Twitch!
Come check it out every weekday at 12:00pm MST at https://twitch.tv/carloskidman

- **_`@sudomaze`_** - amazing feedback, humor, and searching skills
- **_`@vernkofford`_** - OG subscriber and friend
