# SongRecommenderSystem

## Introduction

Our project aims to develop a song recommendation system. We analyze a song and evaluate its main features and want to find the most compatible one among other songs and recommend it to the user.

[Youtube link](https://youtu.be/vyuFLFT_kqg)

## Requirements

* Python 3
* Pandas
* Numpy
* Spotipy
* dotenv

## Installation

```bash
pip install numpy, pandas, spotipy
```

```bash
# optional package to read from .env file
# client_id and client_secret can be mannually set in the code
pip install python-dotenv
```

## Usage

1. After getting cliend_id and client_secret from [Spotify Dashboard](https://developer.spotify.com/), edit `data/getdata.py` and set them to the related fields.

1. Then edit the playlists as you want in `data/playlist_urls.txt` file. Each line should contain a playlist url.

1. Then, run the following command to get the track details.

     ```bash
    cd data
    python getdata.py
    ```

1. Now `data/data.csv` file should be created. You can use this file in the notebook.

1. Run `notebook.ipynb` and enjoy!

## References

* [Spotify API](https://developer.spotify.com/documentation/web-api/)
* [Spotipy docs](https://spotipy.readthedocs.io/en/2.18.0/)
* [Spotify for Developers](https://developer.spotify.com/)

## Disclaimer

This project is for educational purposes only. We do not own any of the data used in this project nor commercially use the data. All rights reserved to their respective owners.
