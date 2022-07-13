import requests
import eyed3
from eyed3.id3.frames import ImageFrame
import glob
import ntpath
import urllib.request

dir = "Ce PC\Redmi Note 9S\Internal shared storage\snaptube\download\SnapTube Audio"

def GetSongInfo(name):
    print("getting the song info")
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q": name, "type": "tracks", "offset": "0", "limit": "1", "numberOfTopResults": "1"}

    headers = {
        "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    storage = response.json()

    data = storage['tracks']['items'][0]['data']

    trackid = data['id']

    title = data['name']

    albumInfo_ = data['albumOfTrack']

    CoverArt = albumInfo_["coverArt"]["sources"][2]

    url = "https://spotify23.p.rapidapi.com/tracks/"

    querystring = {"ids": trackid}

    headers = {
        "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    storage = response.json()

    if storage != {}:

        infolist = storage['tracks'][0]

        albuminfo = infolist['album']

        albumname = albuminfo['name']

        print(f'Album: {albumname}')
        tracknum = infolist['track_number']
        print(f'Track number: {tracknum}')
        artistlist = infolist['artists']

        Artist = artistlist[0]

        return[title, Artist, albumname, CoverArt]

    else:
        exit(404)

def GetImage(link):
    print("getting the coverArt")
    imgURL = link
    image = urllib.request.urlretrieve(imgURL, "C:/Users/HP/Desktop/TempFolder")
    return image


def ChangeTheInfo(file, infolist):
    print("changing the metadata")
    title = infolist[0]
    Artist = infolist[1]
    Album = infolist[2]
    imagelink = infolist[3]
    image = GetImage(imagelink)

    auxfile = eyed3.load(file)
    auxfile.initTag()
    auxfile.tag.title = title
    auxfile.tag.artist = Artist
    auxfile.tag.album = Album
    auxfile.tag.images.set(ImageFrame.FRONT_COVER, open(image, 'rb').read(), 'image/png')
    auxfile.tag.save()


def start():
    print("starting...")
    filesList = glob.glob(r"")
    print(filesList)
    for file in filesList:
        fileName = ntpath.basename(file)
        bannedwords = ["\\", ".mp3", "(", ")", "[", '"', "]" "audio", "official audio", "officialaudio", "official video", "offcialaudio", 'feat', "ft.", "&", "ft", "visualizer", "lyrics", "lyrics video", "lyricsvideo", "official music video", "officialmusicvideo", "official lyric video", "officiallyricvideo", 'visualizer']
        fileName = fileName.replace(bannedwords, "")
        info = GetSongInfo(fileName)
        ChangeTheInfo(file, info)

start()
