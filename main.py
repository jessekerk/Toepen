from randomplayer import RandomPlayer  # noqa: F401
from toepen import ToepController
from zeroorderplayer import (  # noqa: F401
    OptimisticZeroOrderPlayer,
    PessimisticZeroOrderPlayer,
    RationalZeroOrderPlayer,
    ZeroOrderPlayer,
)

controller = ToepController()
controller.join(RationalZeroOrderPlayer())
controller.join(OptimisticZeroOrderPlayer())
controller.play(debug=False)
print(controller.repeated_games(10000))
