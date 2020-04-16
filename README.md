# argosSpotifyExtension

This is a simple Spotify extension that displays the currently playing/paused song with artist, album and title.
There are also some simple controls to pause/play, go to next or previous song and to exit spotify.
If spotify isn't running, "Spotify is not running" is displayed together with a button to start Spotify.

![Spotify extension screenshot running](https://i.imgur.com/QwXCofR.png)
![Spotify extension screenshot not running](https://i.imgur.com/Re7fPg7.png)

To edit the text, change the string variable `finalString` in the script to your liking. To change the shortening threshold, change the variable `maxDisplayLength` to your desired length. To change the color of the Artist, Album and Title in the menu, change the variable `detailColor`.

This is all done using python and [Mopidy](https://docs.mopidy.com/en/latest/), and their [Spotify extension](https://github.com/mopidy/mopidy-spotify). It should be included when installing Spotify (at least I can't remember installing it separately), but should you need to install it for some reason, [it can be found here](https://docs.mopidy.com/en/latest/installation/debian/#installing-extensions). The script uses the python module psutil, install it using `pip install psutil`. You also need python-dbus, install it using `sudo apt install python-dbus`.

To easily keep up-to-date with new versions, simply make a hard link from spotifyExtension.py to your Argos folder, i.e. `ln spotifyExtension.py ~/.config/argos/spotify.1l.1s.py`. Then you can just `git pull` this repository to update.

**Note:** Your personal `finalString`, `maxDisplayLength` and `detailColor` will be overwritten when you do a `git pull`.