# Toontown: Archipelago
Welcome to the repository of the Archipelago version of the Toontown!

This source is built on the foundation of Toontown Offline's Toontown School House's source code.
Toontown School House is a course dedicated to teaching members of the Toontown community how to develop for the game. For more information, head over to [this](https://www.reddit.com/r/Toontown/comments/doszgg/toontown_school_house_learn_to_develop_for/) Reddit post.

This repository is a version of Toontown that is compatible with [Archipelago's multi-world multi-game randomizer](https://archipelago.gg)!
This version of toontown makes modifications to the base game to not only to provide support for Archipelago, but also introduce 
gameplay tweaks to make the experience quicker, more satisfying, and more solo friendly. This game also has support for hosting
and joining mini-servers if you still wish to play with friends! This game is a **fully remote** Archipelago game, which means
that however you want to set up your slots for gameplay, it should work as you would expect. This means the following ways to play are supported:
- Playing alone on a slot
- Playing with friends on the same server with unique slots
- Playing with friends on the same server sharing one slot
- Multi-tooning 2-4 toons that all share a slot (and share progression)
- Multi-tooning 2-4 toons that all have unique slots
- Playing with 2 other friends who are also multi-tooning 4 toons and all sharing the same slot

The possibilities really are endless and you can play the game however you want, just make sure you set up your 
Archipelago rooms to accommodate that.


# Source Code
This source code is based on a March 2019 fork of Toontown Offline v1.0.0.0 used for Toontown School House. 
It has been stripped of all Toontown Offline exclusive features, save one. The brand new Magic Words system made for 
Toontown Offline has been left alone, and upgraded to the most recent build. This feature will allow users to easily navigate around Toontown without any hassle.

On top of that, this source code has also been updated to Python 3, utilizing a more modern version of Panda3D. 

Credits:
* [The Toontown Offline Team](https://ttoffline.com) for the foundation of this codebase (Toontown Schoolhouse)
* [The Corporate Clash Crew](https://corporateclash.net) for toon models, some various textures, and assistance with implementing v1.2.8 craning
* Polygon for making the Corporate Clash toon models
* [Open Toontown](https://github.com/open-toontown) for providing a great reference for a Toontown codebase ported to Python 3
* Toontown Infinite for Bossbot HQ suit paths
* [Astron](https://github.com/Astron/Astron)
* [Panda3D](https://github.com/panda3d/panda3d)  (More specifically, [Astron's fork of Panda3D](https://github.com/Astron/panda3d))  
* [libpandadna](https://github.com/loblao/libpandadna)
* [libotp-movement](https://github.com/jwcotejr/libotp-movement)
* [libotp-nametags](https://github.com/loblao/libotp-nametags)
* [Ben Briggs](https://www.youtube.com/@benbriggsmusic) for the dripstinct music.
* Reverse-engineered Toontown Online client/server source code is property of The Walt Disney Company.


# Panda3D
This source code requires a specific version of Panda3D to run. It can be installed by downloading the launcher below:

### Windows
- For 64 bit machines (You probably want this one!): [Panda3D SDK (Python 3.9 x86_64)](https://mega.nz/file/uAMxEKqL#yQfS9UPpYHzKYDR5vq-LF5gxxLa6HUmxLUp65uzneVo)
- For 32 bit machines: [Panda3D SDK (Python 3.9 x86)](https://mega.nz/file/6UsARa7R#pg5KgxW0NgkHEl_k0fK6NbBK8LfdEcDGZ6NsVeWwDKM)

If you are on a non-Windows operating system, please refer to the [Panda3D SDK setup portion of Open Toontown's setup guide](https://github.com/open-toontown/open-toontown/blob/develop/README.md#setup). Those steps should also work for this source. You can use the following links to be taken to the respective operating system quickly:
- [MacOS 10.9+](https://github.com/open-toontown/open-toontown/blob/develop/README.md#macos-109)
- [Linux](https://github.com/open-toontown/open-toontown/blob/develop/README.md#linux-building-your-own)

**NOTE:** If you install Panda3D in any other way that WAS NOT the 64 bit install listed above, you will need to pay extra
attention to the `PPTYHON_PATH` step of this guide!

# Running the Source

### PPYTHON_PATH

If you installed Panda3D using the very first link (64 Bit version of Panda3D for Windows), you can probably skip this step.
If you get an issue that relates to `The system cannot find the path specified`, then this is probably where your issue lies.

First, navigate to the `PPYTHON_PATH` file in the root directory and open it. Make sure that the path to your Panda3D 
install is present. If you left default options while running the 64 bit Panda3D installer for Windows, it should be `"C:/Panda3D-1.11.0-x64/python/ppython.exe"` 
in almost all cases.

For those who installed Panda3D via other means (32 bit version of Panda3D, other operating systems, different versions, etc.),
you **must** verify that the path present in `PPTYHON_PATH` matches the install location of where you installed Panda3D.

## Starting a Server/District

The following steps relate to the server side of the game. If you are playing single player and/or hosting a server for
yourself and friends, this part of the guide applies to you. If you are **only joining a friend who says they are hosting
a game**, then you can skip to the `Starting the Game` part of this guide!

Once you have done all the proper setup covered in this README, you can now navigate to the `win32` folder in the root directory.
Once you are there, you need to run the `.bat` files present in the following order:
- `start_astron_server.bat`
- `start_uberdog_server.bat`
- `start_ai_server.bat`

Assuming that no errors occur, you are now running a Toontown: Archipelago mini-server!

These are the three processes that are crucial for running a Toontown Server. If you want a TLDR on what each process
does, UberDOG is meant for handling global services like login, cross district communication, etc. AI(s) is/are each separate 
"district" in game, and is where most server side code is handled. Astron is the communication interface for the two and 
game clients.


## Starting The Game/Joining a Mini-Server

Once you have done all the proper setup covered in this README, you can now navigate to the win32 folder in the root 
directory. Once you are there, you need to run either of the following .bat files **(BUT ONLY ONE!)**:

- `start_game.bat` *Runs the game client, and assumes you are playing on `localhost` w/ username `dev`*
- `join_server.bat` *Runs the game client, but presents the option to input a Toontown: Archipelago gameserver IP and username*

If you are playing solo and/or hosting the server yourself, it does not matter which one you use. But if you are joining
someone else's mini-server, use `join_server.bat` and input the IP you were given and a random username. 
Usernames are essentially your "login" as there is no true account management system in an offline source.

The game should start up and you should be good to start playing!


## Common Issues/FAQ

### What the heck is an archipelago?

You should probably check out [this website](https://archipelago.gg/faq/en/) first.

### What is a check? What is a seed? Your what is in logic???? Why do you keep saying you are BK'd... What is this language you guys are speaking!?!?!

Randomizers have established a bit of common terms for various things that are common to pretty much most randomizer 
supported games. Archipelago is no exception, and even provide a neat [glossary](https://archipelago.gg/glossary/en/) you can use to reference certain
terms if this is your first experience with a randomizer or Archipelago.

### I set up the server and everything is running fine. I can connect to my own server but my friends can't. Why?

If you are hosting a Mini-Server, you **must** port forward to allow incoming connections on port `7198`.
There are two ways to accomplish this:

- Port forward the port `7198` in your router's settings.
- Use a third party program (such as Hamachi) to emulate a LAN connection over the internet.

As router settings are wildly different, I cannot provide a tutorial on how to do this on this README for your specific
router. However, the process is pretty straight forward assuming you have access to your router's settings. 
You should be able to figure it out with a bit of research on Google.


### I launched the game and I am getting the error: The system cannot find the path specified

You did not do the `PPYTHON_PATH` step correctly from before. Double check that Panda3D is installed at the directory
located in `PPYTHON_PATH` and try again.


### I logged in and I have no gags and can't access the Toon HQ.... why can't I play?

This game is specifically designed to only work properly when you are connected to an Archipelago game. If you want to
play the game as intended, please generate an Archipelago seed or join an Archipelago room with others.

If you are a developer or just want to play around with the source, you have access to use commands. Check your 
book and look at the spellbook page to see what you can do. `~maxtoon` will put your toon in a state where you can do 
anything in the game with no restrictions.


### I was playing and my game crashed :(

Toontown: Archipelago is currently in an early alpha build so many issues are expected to be present. If you found a
crash/bug, feel free to [create an Issue](https://github.com/DevvyDont/toontown-archipelago/issues/new) on the GitHub page for the repository. Developers/contributors
use this as a "todo list". If you choose to do this, try and be as descriptive as possible on what caused the crash, and 
any sort of possible steps that can be taken to reproduce it.


### I was playing and the district reset :(

Similarly to a game crash, sometimes the district can crash. Follow the same steps as the previous point.


### I was given an Archipelago room link and my game works fine, how do I connect to the multiworld and play?

When in game, you first need to type (in Toontown's chat) `!slot <SLOT NAME>` where you replace `<SLOT NAME>` with 
whatever your slot is in the Multiworld room. Once you have done this, you can then type `!connect <AP SERVER IP>`
to play! The AP Server IP is usually listed at the top where it says "You can type /connect (AP SERVER IP) in your client...".


### I want to Play Toontown: Archipelago in my friend's multiworld, and they are asking for my .apworld file. What the heck is that??

.apworld files are what tell Archipelago what items a game has and what locations it can check. They are essentially just zip files
of the source code for seed generation. All you need to do, is go to the `apworld/` folder, and run `make_apworld.bat`. This will 
generate the .apworld file you need to give to your friend who is generating an AP seed.


### Okay now they are asking for my YAML??? HELP!!!!

Archipelago uses .YAML files to define player settings and slot names for the game they want to play. In the `apworld/`
directory, you will see an `EXAMPLE_TOONTOWN.yaml` file. Go ahead and make a copy of this, and edit its name to whatever
you want.
(It is typical AP etiquette to name the file after your online alias and the game you are playing. e.g. `devvydont-tt.yaml`).
Now, edit the file and change the `name` field at the bottom. Replace `PUTTOONNAMEHERE` with what you would like your slot
name (and toon name!) to be. You can also change any other settings present here as well to affect how your run will play out.


### I wanna host an Archipelago game!

As a warning, if you are not familiar with running unofficial Archipelago games and generating seeds for them, this 
may be extremely difficult and daunting for you, but I will try my best to break it down here. If you are an Archipelago 
veteran, then refer to the previous two FAQ. These will tell you how to get ahold of the .apworld file and an example YAML.

Toontown is currently (and probably will be for a long time) an unofficial Archipelago game. For the forseeable future,
it will be a lengthy process to generate AP games with Toontown in them.

When generating an Archipelago game, you need to follow the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en)
and install all the prerequisites there before continuing. This guide should tell you everything you need to know about
generating, configuring, and hosting Archipelago games. The only thing this guide will not explain to you, is how to 
add unsupported games to your generator. To accomplish this, generate the `toontown.apworld` file (see above) and place
it in `lib/worlds/` directory in your Archipelago install. You can reach the Archipelago install by clicking `Browse Files`
on the Archipelago launcher.

If you have any difficulties with this step, you can ask for help in the [Toontown: Archipelago Discord](https://discord.gg/GRjQZBsrJK).
You can also refer to the [official Archipelago Discord](https://discord.gg/8Z65BR2), where you can find a guide to installing/generating seeds that include
unsupported/unofficial games.