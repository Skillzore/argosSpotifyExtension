#!/usr/bin/env python3

# This is a simple Spotify extension that displays the currently playing/paused song with artist and title. There are also some simple controls to pause/play, go to next or previous song and to exit spotify. To kill_spotify the spotify application, a separate python script is used. If spotify isn"t running, "Spotify is not running" is displayed together with a button to start Spotify.
# To easily keep up-to-date with new versions, simply make a hard link from spotifyExtension.py to your Argos folder, i.e. "ln spotifyExtension.py ~/.config/argos/spotify.1l.1s.py".
#
# ![Spotify extension screenshot running](https://i.imgur.com/QwXCofR.png)
# ![Spotify extension screenshot not running](https://i.imgur.com/Re7fPg7.png)
# Made by [Skillzore](https://github.com/Skillzore)

import dbus
import psutil

maxDisplayLength = 20
detailColor = "#1DB954" # Spotify green
startUri = "spotify:track:3sXHMpriGlbFhMdJT6tzao"

# Check if process name is running
def is_spotify_running():
    for proc in psutil.process_iter():
        if(proc.name() == "spotify" and proc.status() != psutil.STATUS_ZOMBIE):
            return True

# Kill spotify process
def kill_spotify():
    for proc in psutil.process_iter():
        if proc.name() == "spotify":
            proc.kill()

# Shorten strings longer than maxDisplayLength to maxDisplayLength and add ... after
def maybe_shorten(string):
    if(len(string) > maxDisplayLength):
        return string[:maxDisplayLength] + "..."
    else:
        return string

# Replace special characters in string with the corresponding html entity number
def clean_special_chars(string):
    return string.replace("&","&#38;").replace("|","&#124;")
    
# Main - Build menu item
def main():
    if(is_spotify_running()):
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
        metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        playback_status = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
    
        if(len(metadata["xesam:artist"]) > 0 and len(playback_status) > 0):
            artist = clean_special_chars(metadata["xesam:artist"][0])
            album = clean_special_chars(metadata["xesam:album"])
            title = clean_special_chars(metadata["xesam:title"])
    
            final_artist = maybe_shorten(artist)
            final_album = maybe_shorten(album)
            final_title = maybe_shorten(title)
    
            # Edit this string to change the display
            final_string = playback_status + ": " + final_artist + " &#124; " + final_album + " &#124; " + final_title
    
            print(final_string + " | iconName=spotify")
    
            print("---")
    
            # Print full details in menu
            set_color = " | color=" + detailColor
            print("Artist: " + artist + set_color)
            print("Album: " + album + set_color)
            print("Title: " + title + set_color)
    
            print("---")
    
            # show play or pause button depending on current status
            if(playback_status == "Paused" or playback_status == "Stopped"):
                print("Play | iconName=media-playback-start bash='dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play' terminal=false")
            else:
                print("Pause | iconName=media-playback-pause bash='dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause' terminal=false")
    
            # next button
            print("Next | iconName=media-skip-forward bash='dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next' terminal=false")
        
            # previous buton
            print("Previous | iconName=media-skip-backward bash='dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous' terminal=false")
        
            # exit spotify
            print('''Exit Spotify | iconName=application-exit bash='cd ~/git/argosSpotifyExtension && python3 -c "from spotifyExtension import kill_spotify; kill_spotify()"' terminal=true''')
        
        else:
            print("Nothing is playing | iconName=spotify")
            print("---")
            print("Start playing music! | iconName=media-playback-start bash='dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:" + startUri + "' terminal=false")
            print('''Exit Spotify | iconName=application-exit bash='cd ~/git/argosSpotifyExtension && python3 -c "from spotifyExtension import kill_spotify; kill_spotify()"' terminal=true''')
     
    else:
        print("Spotify is not running | iconName=spotify")
        print("---")
        print("Start Spotify | iconName=spotify bash='spotify U%' terminal=false")
    
if __name__ == '__main__':
    main()
