# -*- coding: utf-8 -*-
import requests
import json
from random import randint, random
import os
from dotenv import load_dotenv

from lib import getAlbumReleaseYear, getRandomAlbumName

# load .env values
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Spotipy object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-top-read"))


# Global variables
band_objects = []
selected_artist = None
selected_artist_albums = []
questions = None


# Gets twenty bands from your spotify profile
def getTwentyRandomArtists():
    global band_objects
    band_list = []
    band_objects = sp.current_user_top_artists(limit=20, offset=randint(0, 32))

    if band_objects is None or band_objects  == []:
        print("Error getting artists")
        return None

    for artist in band_objects['items']:
        band_list.append(artist["name"])

    band_objects = band_objects['items']
    return band_list


# Get full artist object from name
def getArtistItemByName(name: str = ""):
    global band_objects

    if name == "":
        print("Error: empty band name")
        return {"error": "Empty band name"}

    if band_objects is None or band_objects == []:
        print(f"Error: the band '{name}' was not in the list.")
        return {'error': f"the band {name} was not in the list"}

    band_item = None
    for band in band_objects:
        if band['name'] == name:
            band_item = band
            break

    if band_item is None:
        print(f"Error: The band '{name}' was not in the list.")
        return {'error': f"the band {name} was not in the list"}

    return band_item


# Fetch information from band
def fetchInfoFromBand(name: str = ""):
    global band_objects, selected_artist, selected_artist_albums
    if name == "":
        print("Error: empty band name")
        return {"error": "Empty band name"}

    band_item = getArtistItemByName(name)
    selected_artist = sp.artist(band_item['id'])
    result = sp.artist_albums(band_item['id'])

    if result is None:
        print("Warning: couldn't get albums")
        return None

    selected_artist_albums = result['items']
    return {'message': 'success'}


# generate questions about release dates of albums
def qReleaseDate(number: int):
    global selected_artist_albums, questions

    for i in range(0, number - 1):
        album = getRandomAlbumName(selected_artist_albums)
        questions.append(getAlbumReleaseYear(
            selected_artist_albums, album
        ))


# Get an album name from a related artist
def getAnotherAlbumFromArtist(artist):
    newArtist = sp.artist_related_artists(artist['id'])
    artistIndex = randint(0, len(newArtist['artists']) - 1)
    newAlbums = sp.artist_albums(newArtist['artists'][artistIndex]['id'])

    if len(newAlbums) == 0:
        return newAlbums['items'][0]['name']

    albumIndex = randint(0, len(newAlbums) - 1)

    if albumIndex == -1 or len(newAlbums['items']) <= albumIndex:
        return newAlbums['items'][0]['name']

    return newAlbums['items'][albumIndex]['name']


# generate questiosn about which songs are in which album
def qSongsOfAlbums(number: int):
    global selected_artist_albums, questions

    for i in range(0, number - 1):
        index = randint(0, len(selected_artist_albums) - 1)
        album = sp.album(selected_artist_albums[index]['id'])['tracks']
        songIndex = randint(0, len(album['items']) - 1)

        name = album['items'][songIndex]['name']
        question = f"Which album is the song '{name}' part of ?"
        answer = selected_artist_albums[index]['name']
        propositions = []

        for j in range(0, 3):
            k = randint(0, len(selected_artist_albums) - 1)
            if k == index or k == -1 or len(selected_artist_albums) == 0:
                propositions.append(
                    getAnotherAlbumFromArtist(selected_artist)
                )
            propositions.append(selected_artist_albums[k]['name'])

        questions.append({
            'question': question,
            'validAnswer': answer,
            'wrongAnswers': propositions[:3]
        })


# generates a single question about the genre of the artist
def qGenreOfArtist():
    global selected_artist, questions
    question = f"Give one genre of {selected_artist['name']}"

    if not selected_artist['genres']:
        return False

    genres = sp.recommendation_genre_seeds()['genres']
    new_genres = []

    for i in range(0, 3):
        new_genres.append(genres[randint(0, len(genres) - 1)])

    answer = selected_artist['genres'][0]
    questions.append({
        'question': question,
        'validAnswer': answer,
        'wrongAnswers': new_genres
    })


def deleteDuplicateQuestions():
    new_questions_strings = []
    new_questions = []
    for i in range(len(questions)):
        currentQuestion = questions[i]
        currentQuestionStr = currentQuestion["question"]
        if currentQuestionStr not in new_questions_strings:
            new_questions_strings.append(currentQuestionStr)
            new_questions.append(questions[i])
    return new_questions


def modifyDuplicateAnswers(newQuestions):
    for i in range(len(newQuestions)):
        validAnswer = newQuestions[i]["validAnswer"]
        wrongAnswers = newQuestions[i]["wrongAnswers"]
        for answer in wrongAnswers:
            if answer == validAnswer:
                print(f"dupplicate wrong answer: {answer}")
        wrongAnswers = ["I don't know" if s == validAnswer else s for s in wrongAnswers]

        if len(wrongAnswers) >= 3:
            if wrongAnswers[0] == wrongAnswers[1] or wrongAnswers[0] == wrongAnswers[2]:
                wrongAnswers[0] = "I don't know"
            elif wrongAnswers[1] == wrongAnswers[2]:
                wrongAnswers[1] = "I don't know"
        newQuestions[i]["wrongAnswers"] = wrongAnswers

    return newQuestions


# Generates a set of questions about the selected_artist
def generateQuestions(
    name: str = "",
    releaseDateQuestions: int = 5,
    songsOfAlbumQuestions: int = 9
):
    global selected_artist, artist_albums, questions
    questions = []

    if name == "":
        print("Error: empty band")
        return {'error': 'Empty band'}

    fetchInfoFromBand(name)

    qReleaseDate(releaseDateQuestions)
    qSongsOfAlbums(songsOfAlbumQuestions)
    if not qGenreOfArtist():
        qSongsOfAlbums(1)

    new_questions = deleteDuplicateQuestions()
    new_questions = modifyDuplicateAnswers(new_questions)

    return new_questions[:20]

# Main
# artists = getTwentyRandomArtists()
# print(artists)
# if artists is None:
#     print("Error: Artists is None")
#     exit(84)
# questions = generateQuestions(artists[0])
# print(json.dumps(questions, indent=2))
