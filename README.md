# Toontown: Archipelago
Welcome to the repository of the Archipelago version of the Toontown School House source code!

Toontown School House is a course dedicated to teaching members of the Toontown community how to develop for the game. For more information, head over to [this](https://www.reddit.com/r/Toontown/comments/doszgg/toontown_school_house_learn_to_develop_for/) Reddit post.

This repository is a version of Toontown that is compatible with [Archipelago's multi-world multi-game randomizer](https://archipelago.gg)!
This version of toontown makes modifications to the base game to not only to provide support for Archipelago, but also introduce 
gameplay tweaks to make the experience quicker, more satisfying, and more solo friendly. This game also has support for hosting
and joining mini-servers if you still wish to play with friends, however the details on accomplishing this will not be covered here.
If you are playing this way, just make sure that every player has their own unique player slot when generating an Archipelago game.


# Source Code
This source code is based on a March 2019 fork of Toontown Offline v1.0.0.0 used for Toontown School House. It has been stripped of all Toontown Offline exclusive features, save one. The brand new Magic Words system made for Toontown Offline has been left alone, and upgraded to the most recent build. This feature will allow users to easily navigate around Toontown without any hassle.

On top of that, this source code has also been updated to Python 3, utilizing a more modern version of Panda3D. 

Credits:
* [The Toontown Offline Team](https://ttoffline.com) for the foundation of this codebase (Toontown Schoolhouse)
* [The Corporate Clash Crew](https://corporateclash.net) for toon models, some various textures, and assistance with implementing v1.2.8 craning
* [Open Toontown](https://github.com/open-toontown) for providing a great reference for a Toontown codebase ported to Python 3
* Toontown Infinite for Bossbot HQ suit paths
* [Astron](https://github.com/Astron/Astron)
* [Panda3D](https://github.com/panda3d/panda3d)  (to be redirected to the version of Panda3D this source supports [click here](https://github.com/Astron/panda3d))  
* [libpandadna](https://github.com/loblao/libpandadna)
* [libotp-movement](https://github.com/jwcotejr/libotp-movement)
* [libotp-nametags](https://github.com/loblao/libotp-nametags)
* Reverse-engineered Toontown Online client/server source code is property of The Walt Disney Company.


# Panda3D
This source code requires a specific version of Panda3D to run. It can be installed by downloading the launcher below:

### Windows
- [Panda3D SDK (Python 3.9 x86)](https://mega.nz/file/6UsARa7R#pg5KgxW0NgkHEl_k0fK6NbBK8LfdEcDGZ6NsVeWwDKM)
- [Panda3D SDK (Python 3.9 x86_64)](https://mega.nz/file/uAMxEKqL#yQfS9UPpYHzKYDR5vq-LF5gxxLa6HUmxLUp65uzneVo)

If you are on a non-Windows operating system, please refer to the [Panda3D SDK setup portion of Open Toontown's setup guide](https://github.com/open-toontown/open-toontown/blob/develop/README.md#setup). Those steps should also work for this source. You can use the following links to be taken to the respective operating system quickly:
- [MacOS 10.9+](https://github.com/open-toontown/open-toontown/blob/develop/README.md#macos-109)
- [Linux](https://github.com/open-toontown/open-toontown/blob/develop/README.md#linux-building-your-own)


# Libuv 
This source code requires libuv.dll in the astrond folder to run. Here are links to the 32 bit dll and 64 bit dll.

- [Libuv.dll (32-bit)](https://cdn.discordapp.com/attachments/638485243560460309/640339222682664973/libuv.dll)
- [Libuv.dll(64-bit)](https://cdn.discordapp.com/attachments/638485243560460309/640339153346887696/libuv.dll)


After downloading the file just drop it in the astron folder.

# Running the Source

First, navigate to the `PPYTHON_PATH` file in the root directory and open it. Make sure that the path to your Panda3D install is present. If you left default options while running the Panda3D installer, it should be `"C:/Panda3D-1.11.0-x64/python/ppython.exe"
` in almost all cases.

Once you have done all the proper setup covered in this README, you can now navigate to the `win32` folder in the root directory.
Once you are there, you need to run the `.bat` files present in the following order:
- `start_astron_server.bat`
- `start_uberdog_server.bat`
- `start_ai_server.bat`
- `start_game.bat`

The game should start up and you should be good to start playing!

**NOTE:** If you are playing with someone who is hosting a server, you only need to run `join_server.bat` and enter their IP when prompted.
If you are hosting a server, you will need to port forward (default port is `7199`) via your router to allow people to connect to you.
