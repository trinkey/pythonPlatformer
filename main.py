import _player
import _screen
import _controller

screen = _screen.Screen()
player = _player.Player(0, 0, [])
controller = _controller.Controller(1, player, screen)

controller.start()
