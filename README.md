# StarCraft 2 Audio Build Order Reader

This project takes in a build order and reads it using text-to-speech based
on the timestamps included in the build order itself. Each line of the build
order must be a timestamp in the form `M?M:SS`.

This does not work without timestamps.

Note that SC2's game speed is not super stable and can drift in either
direction, and so it's possible for the times at which build order items
are read out to drift with respect to the in-game clock. The most reliable
thing seems to be to rewind from replay, therefore it's recommended to
rewind from replay even if starting from the very beginning. When rewinding
from replay, it seems pretty consistent that 1 in-game second is equal to 1.02
real seconds, and this scaling factor is currently hard-coded in.

# Requirements and Running the Application

This project requires Python 3. Install the necessary requirements using `pip3 install -r requirements.txt`.

`./main.py <build_file.txt>`

The application takes the following command line arguments:

`--shorthand`: Whether to abbreviate the names of units/buildings to common
shorthand (eg. "Barracks" -> "Rax")

`--time`: Timestamp to forward to in game. Useful when rewinding from a replay
by simply entering what the in-game clock shows.

# Tips and Tricks

1. There is a built-in 5-second delay. Start the python script and line up
   the 3-second timer before the game starts to sync the two up
2. Feel free to add in actions that aren't strictly build items in your build order file. Spreading creep, dropping mules, or moving out your army are great candidates for reminders.

# License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
