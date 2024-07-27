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

The possibilities really are endless, and you can play the game however you want. 
Just make sure you set up your Archipelago rooms to accommodate that!


# Source Code
This source code is based on a March 2019 fork of Toontown Offline v1.0.0.0 used for Toontown School House. 
It has been stripped of all Toontown Offline exclusive features, save one. The brand new Magic Words system made for 
Toontown Offline has been left alone, and upgraded to the most recent build. This feature will allow users to easily navigate around Toontown without any hassle.

On top of that, this source code has also been updated to Python 3, utilizing a more modern version of Panda3D. 

Credits:
* [The Toontown Offline Team](https://ttoffline.com) for the foundation of this codebase (Toontown Schoolhouse)
* [The Corporate Clash Crew](https://corporateclash.net) for toon models, some various textures, and assistance with implementing v1.2.8 craning
* Polygon for making the Corporate Clash toon models
* [Open Toontown](https://github.com/open-toontown) for providing a great reference for a Toontown codebase ported to Python 3 and the HD Mickey Font
* Toontown Infinite for Bossbot HQ suit paths
* [Astron](https://github.com/Astron/Astron)
* [Panda3D](https://github.com/panda3d/panda3d)  (More specifically, [Open Toontown's fork of Panda3D](https://github.com/open-toontown/panda3d))
* [libotp-nametags](https://github.com/loblao/libotp-nametags)
* [Ben Briggs](https://www.youtube.com/@benbriggsmusic) for the dripstinct music.
* Reverse-engineered Toontown Online client/server source code is property of The Walt Disney Company.

# Getting Started

At this time, Windows is the only supported platform. For other platforms, please see [Running From Source.](#running-from-source)

### Windows

To play Toontown: Archipelago, you will need to run a server.
If someone else is running a server, skip steps 3 and 4.

1. Download `TTAP.zip` from [here.](https://github.com/toontown-archipelago/toontown-archipelago/releases/latest)
2. Extract the ZIP to a folder of your choice.
3. Open the folder and run `start_servers.bat`. This will make some windows appear, do not close these during gameplay!
4. If you're looking to play with friends, see [here.](#i-set-up-the-server-and-everything-is-running-fine-i-can-connect-to-my-own-server-but-my-friends-cant-why)
5. To start the game, run `start_client.bat`. This will open a window that will help you set up your client.
6. Where it says "Username", enter a name unique to you. You should enter this same name everytime you play. Then press enter.
7. Where it says "Server IP", enter the IP address of the server. Then press enter. If you're running the server locally, just press enter without typing anything.
8. Enjoy Toontown: Archipelago!
9. For Archipelago randomizer specific setup check the [FAQ section.](#common-issuesfaq),

If you need more assistance, try following the video tutorial [here.](https://youtu.be/TJTC7A5OFTE)

### Docker (Linux Server)

Before starting, please ensure you have Docker and Docker Compose installed.
You can find out how to install them [here.](https://docs.docker.com/engine/install/)

1. Download the `Source Code (ZIP)` from [here.](https://github.com/toontown-archipelago/toontown-archipelago/releases/latest)
2. Extract the ZIP to a folder of your choice.
3. Using `cd`, navigate to the `launch/docker` directory.
4. Start the server using `docker compose up`. This may take a while.
5. Press `Control+C` to stop the server.

# Running from source

## Panda3D
This source code requires a specific version of Panda3D to run.

### Windows

Please download the latest engine build from [here.](https://github.com/toontown-archipelago/panda3d/releases/latest)

### Other

At this time Toontown: Archipelago only supports Windows.
To run on other platforms you will need to build the engine. 
This is an advanced use-case and is unsupported.
To get started, please see the build instructions [here.](https://github.com/toontown-archipelago/panda3d)

## Starting the game

Once Panda3D is installed, please find your systems launch directory.
- Windows: `win32`
- Mac: `darwin`
- Linux: `linux`

Then run the following scripts in order:
- `start_astron_server`
- `start_uberdog_server`
- `start_ai_server`
- `start_game`

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
of the source code for seed generation. The .apworld file is available on the releases page. If you are running from source,
go to the `apworld/` folder, and run `make_apworld.bat`. This will generate the .apworld file you need to give to your friend who is generating an AP seed.


### Okay now they are asking for my YAML??? HELP!!!!

Archipelago uses .YAML files to define player settings and slot names for the game they want to play. If you're downloading from the releases
page, the yaml is available from download there. If you are running from source, you should look in the `apworld/` directory,
you will see an `EXAMPLE_TOONTOWN.yaml` file. Go ahead and make a copy of this, and edit its name to whatever you want.
(It is typical AP etiquette to name the file after your online alias and the game you are playing. e.g. `devvydont-tt.yaml`).
Now, edit the file and change the `name` field at the top. Replace `PUTTOONNAMEHERE` with what you would like your slot
name (and toon name!) to be. You can also change any other settings present here as well to affect how your run will play out.


### I wanna host an Archipelago game!

As a warning, if you are not familiar with running unofficial Archipelago games and generating seeds for them, this 
may be extremely difficult and daunting for you, but I will try my best to break it down here. If you are an Archipelago 
veteran, then refer to the previous two FAQ. These will tell you how to get ahold of the .apworld file and an example YAML.

Toontown is currently not (and never will be) an unofficial Archipelago game, due to the nature of the status of Toontown as a whole.
As a result, generating seeds with Toontown in them may be a bit difficult. The [video tutorial](https://youtu.be/TJTC7A5OFTE) however,
does go over these steps if you are confused.

When generating an Archipelago game, you need to follow the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en)
and install all the prerequisites there before continuing. This guide should tell you everything you need to know about
generating, configuring, and hosting Archipelago games. The only thing this guide will not explain to you, is how to 
add unsupported games to your generator. To accomplish this, generate the `toontown.apworld` file (see above) and place
it in `lib/worlds/` directory in your Archipelago install. You can reach the Archipelago install by clicking `Browse Files`
on the Archipelago launcher.

If you have any difficulties with this step, you can ask for help in the [Toontown: Archipelago Discord](https://discord.gg/GRjQZBsrJK).
You can also refer to the [official Archipelago Discord](https://discord.gg/8Z65BR2), where you can find a guide to installing/generating seeds that include
unsupported/unofficial games.