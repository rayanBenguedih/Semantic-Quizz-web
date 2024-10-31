# Semantic-Music-quiz

## Installation

To launch the application, you'll need a `.env` file containing:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=your_redirect_uri
```

Then, use the python `venv` to install the requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
make
```

## Starting

To start the program, use this command:

```bash
./quiz
```

## BACK-END

The back-end is responsible of two things:

- fetching 20 random artists from your library
- generating questions about a chosen artist

### Fetching artists

To fetch 20 random artists from your library, use this function from `fetch.py`:

```python
print(getTwentyRandomArtists())

>> ['LANDMVRKS', 'Heaven Shall Burn', 'Eminem', 'Daft Punk', 'Æther Realm', 'Confetti', 'Mick Gordon', 'Sakis Tolis', 'Behemoth', 'Nic D', 'Thousand Sun Sky', 'Carameii', 'Poésie Zéro', 'Ghost', 'DaveerCode', 'Alcest', 'I Built the Sky', 'Lindemann', 'Tess', 'Motionless In White']
```

Then you can ask your user to select one of them.

### Generating questions about a chosen artist

To generate questions about a chosen artist <b>from the `getTwentyRandomArtists` function</b>, use the `generateQuestions` function:

```python
generateQuestions("artist_name")

>> [
  {
    "question": str,
    'validAnswer': str,
    'wrongAnswers': str[]
  }
]
```
