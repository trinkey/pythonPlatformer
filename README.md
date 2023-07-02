# Python Platformer
This is a generic platformer made with python turtle.

To create your own level, first, open the levelCreator.html file. Then, design the game. The key is on the right. Then, in either in main.py or all_in_one.py, whichever you are using, change the value in the line that says `controller = Controller(1, player, screen)` to `controller = Controller(0, player, screen)` (change the 1 to 0)
Once you do that, put the json (generated at the bottom of the page), ignoring the last comma, into {maps.json}.0.map. Then, when you start the game, you should see your level. To change back to the first level, change the number in the file back to 1 from 0.
