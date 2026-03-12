from toepen import ToepController
from randomplayer import RandomPlayer


controller = ToepController()
controller.join(RandomPlayer())
controller.join(RandomPlayer())
controller.play(debug=True)
print(controller.repeated_games(1000))