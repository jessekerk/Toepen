from randomplayer import RandomPlayer
from toepen import ToepController
from zeroorderplayer import ZeroOrderPlayer, PessimisticZeroOrderPlayer, OptimisticZeroOrderPlayer, ReasonableZeroOrderPlayer  # noqa: F401

controller = ToepController()
controller.join(OptimisticZeroOrderPlayer())
controller.join(ReasonableZeroOrderPlayer())
controller.play(debug=True)
print(controller.repeated_games(10000))
