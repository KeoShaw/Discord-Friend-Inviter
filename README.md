# Discord Friend Inviter

# Installation and Use
1. Install Python 3.5.4

2. Install the Discord.py API, found at (https://github.com/Rapptz/discord.py). To easily install, use "python -m pip install -U discord.py" from the command line on Windows.

3. Download/clone this repository into whatever directory you require

4. Create a bot and retrieve its token from the Discord dev website. Paste the token into bot.txt

5. Populate the other text files. Formats:
  -Friends.txt: [Discord user ID],[List of game commands, e.g. +csgo, +dota,etc.] Each friend is on a new line. Friends receive invites (owners can be on this list)
  -commands.txt: [command],[full game name] each command is on a new line
  -owner.txt: [owner ID] Can be multiple owners on new lines. Owners are the only ones able to issue invite commands (+csgo, etc.)
  -server.txt: [server ID] The ID of the server, can only be one.
  
  6. Use python to run friend inviter.py
