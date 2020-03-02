# BenfordSpotify
# Program to check for Benford's Law specifically in datasets from spotify
# Firstly using data from billboard-200.db (sourced from https://components.one/datasets/billboard-200/)
import json
import requests #https://curl.trillworks.com/#python converts curl to python
import webbrowser
from benford import *

BILLBOARD_DB = "billboard-200.db"

def testAllBillboard():
    albumLengths = readDB(BILLBOARD_DB, "albums", 6)
    albumLengthsBenford = calculateBenford(observationsUsed(albumLengths))
    compare(albumLengths, albumLengthsBenford)
    for i in range(5,13):
        actual = readDB(BILLBOARD_DB, "acoustic_features", i)
        expected = calculateBenford(observationsUsed(actual))
        compare(actual, expected)

def testBenfordBase10vs16():
    print(calculateBenford(10000));
    print(calculateBenford(10000, 16));

def getCustomSpotifyDigitCount():
    if input("Open web browser to get token? (y/n): ") == "y":
        webbrowser.open("https://developer.spotify.com/console/get-current-user-playlists/?limit=&offset=")
    token = input("Token: ")
    userID = "116138018"

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token}
    params = (('limit', '100'))

    # only gets the first 20 playlists
    response = requests.get('https://api.spotify.com/v1/users/116138018/playlists', headers=headers)
    responseJSON = response.json()
    playlists = responseJSON["items"]

    leadingDigitCount = {"1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0, "error" : 0}

    for i, playlist in enumerate(playlists):
        tempTracksURL = playlist["tracks"]["href"]
        tempPlaylistLength = playlist["tracks"]["total"]

        print(("Playlist %s import progress: " % (i)), end="")

        for offset in range(0, tempPlaylistLength, 100):
            response = requests.get(tempTracksURL
                +"?fields=items(track(duration_ms%2Cpopularity%2Ctrack_number))&limit=100&offset="+str(offset), headers=headers)
            tempTracksJSON = response.json()["items"]

            for tempTracks in tempTracksJSON:
                leadingDigitCount[str(firstNonZeroDigit(str(tempTracks["track"]["duration_ms"])))] += 1
                leadingDigitCount[str(firstNonZeroDigit(str(tempTracks["track"]["popularity"])))] += 1
                leadingDigitCount[str(firstNonZeroDigit(str(tempTracks["track"]["track_number"])))] += 1

            print("+", end="")
        print()

    return leadingDigitCount

def getCustomSpotifyScaleInvariance():
    if input("Open web browser to get token? (y/n): ") == "y":
        webbrowser.open("https://developer.spotify.com/console/get-current-user-playlists/?limit=&offset=")
    token = input("Token: ")
    userID = "116138018"

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token}
    params = (('limit', '100'))

    # only gets the first 20 playlists
    response = requests.get('https://api.spotify.com/v1/users/116138018/playlists', headers=headers)
    responseJSON = response.json()
    playlists = responseJSON["items"]

    leadingDigitCount = {"1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0, "error" : 0}

    for i, playlist in enumerate(playlists):
        tempTracksURL = playlist["tracks"]["href"]
        tempPlaylistLength = playlist["tracks"]["total"]

        print(("Playlist %s import progress: " % (i)), end="")

        for offset in range(0, tempPlaylistLength, 100):
            response = requests.get(tempTracksURL
                +"?fields=items(track(duration_ms%2Cpopularity%2Ctrack_number))&limit=100&offset="+str(offset), headers=headers)
            tempTracksJSON = response.json()["items"]

            for tempTracks in tempTracksJSON:
                leadingDigitCount[str(firstNonZeroDigit(str(tempTracks["track"]["duration_ms"]/60)))] += 1

            print("+", end="")
        print()

    return leadingDigitCount

def testCustomSpotifyScaleInvariance():
    actual = getCustomSpotifyScaleInvariance()
    n = observationsUsed(actual)
    print("Total Custom Spotify Observations = %s" % (n))
    expected = calculateBenford(n)
    compare(actual, expected)

def testCustomSpotify():
    actual = getCustomSpotifyDigitCount()
    n = observationsUsed(actual)
    print("Total Custom Spotify Observations = %s" % (n))
    expected = calculateBenford(n)
    compare(actual, expected)

def testALL():
    #Custom spotify checks
    actual = getCustomSpotifyDigitCount()
    n_temp = observationsUsed(actual)
    n = n_temp
    print("Total Custom Spotify Observations = %s" % (n_temp))

    #Billboard spotify checks
    #'albums' table
    actualTemp = readDB(BILLBOARD_DB, "albums", 6)
    n_temp = observationsUsed(actualTemp)
    n += n_temp
    actual = mergeDictionaries(actual, actualTemp)
    print("'albums' Table Observations = %s" % (n_temp))

    #'acoustic_features' table
    for i in range(5,13):
        actualTemp = readDB(BILLBOARD_DB, "acoustic_features", i)
        n_temp = observationsUsed(actualTemp)
        n += n_temp
        actual = mergeDictionaries(actual, actualTemp)
        print("'acoustic_features' table Observations %s = %s" % (i, n_temp))

    #Finalise
    print("Total Observations = %s" % (n))
    expected = calculateBenford(n)
    compare(actual, expected)

#testAllBillboard()
#testCustomSpotify()
testCustomSpotifyScaleInvariance()
#testALL()
