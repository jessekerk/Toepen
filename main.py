from toepen import ToepController
from randomplayer import RandomPlayer
from zeroorderplayer import ZeroOrderPlayer


controller = ToepController()
controller.join(RandomPlayer())
controller.join(RandomPlayer())
controller.play(debug=True)
print(controller.repeated_games(1000))