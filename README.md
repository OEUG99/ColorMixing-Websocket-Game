# BrowserSocketGame
A fun demo of how to make browser games via sockets!

Play now via http://beever.xyz:8000/
Note: multiple people are needed to see how the game works, as its multiplayer. This can be simulated in multiple tabs though if you wanna mess around by yourself.


Game note:
- White is a neutral colour, grabbing white food or player will set your to white.
- Mixing no primary colors (r,g,b) will lead to a mixed color which has special abilities.
- Space is how to activate special abilities. arrow keys to control
- Food respawns when consumed, but only within the grid. You can leave the grid, but there is nothing to do outside it.


Mixed colors have special abilities...-

purple:
- change your size to random amount, may be larger or smaller.

yellow:
- double speed for 8 seconds, but lose 1/4 your size. Harder to grab foods.

cyan:
- teleport randomly near by, reduces size by a factor on the scale up to 1/4 your size.
- can teleport every 15 seconds.

black:
- nothing, as this is typically the larger players thus balance

Demo of networking code via sockets:
![CleanShot 2023-03-31 at 22 13 26](https://user-images.githubusercontent.com/46060175/229262560-4ba233d9-4412-4495-9e16-d940d0ab64c5.gif)
