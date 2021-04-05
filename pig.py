from time import perf_counter
import argparse
import random
random.seed(0)


class Player:
    def __init__(self):
        self._score = 0
        self._turn_total = 0
        self._is_computer = False

    def __repr__(self):
        return f'{0}({1}, {2}, {3})'.format(
            self.__class__.__name__,
            self._score, self._turn_total,
            self.temp_score)

    @property
    def score(self):
        return self._score

    @property
    def turn_total(self):
        return self._turn_total

    @property
    def temp_score(self):
        temp_score = self._score + self._turn_total
        return temp_score

    @property
    def is_computer(self):
        return self._is_computer

    def roll(self, die):
        die.roll_die()
        if die.face == 1:
            self._turn_total = 0
        else:
            self._turn_total += die.face

    def hold(self):
        self._score += self._turn_total
        self._turn_total = 0

    def update_score_with_temp(self):
        self._score = self.temp_score


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self._is_computer = True
        self._decision = None

    @property
    def decision(self):
        ComputerPlayer._strategy(self)
        return self._decision

    def _strategy(self):
        if self._turn_total > min(25, 100 - self.temp_score):
            self._decision = 'h'
        else:
            self._decision = 'r'


class PlayerFactory:
    @staticmethod
    def validate_input(p):
        if p not in {'human', 'computer'}:
            print(f"A player must be either a 'human' or 'computer'")
            quit()

    def __init__(self, p1, p2):
        PlayerFactory.validate_input(p1)
        PlayerFactory.validate_input(p2)
        self._p1 = p1
        self._p2 = p2

    def p_list(self):
        pl = []
        for p in (self._p1, self._p2):
            if p == 'human':
                pl.append(Player())
            elif p == 'computer':
                pl.append(ComputerPlayer())
        return pl


class Die:
    def __init__(self):
        self._face = None

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    @property
    def face(self):
        return self._face

    def roll_die(self):
        self._face = random.randint(1, 6)


class Game:
    _winner = None

    def __init__(self, players, die):
        self._players = players
        self._die = die

    def __repr__(self):
        return f'{0}({1}, {2})'.format(
            self.__class__.__name__,
            self._players,
            self._die)

    def print_scores(self):
        for i in range(len(self._players)):
            print(f'Player {i + 1} score: {self._players[i].score}')
        print('')

    def _print_all_info_after_roll(self, player_idx):
        print(f'Player {player_idx + 1} '
              f'rolling number: {self._die.face}')
        print(f'Player {player_idx + 1} '
              f'turn total: {self._players[player_idx].turn_total}')
        Game.print_scores(self)

    @staticmethod
    def _ask_player_for_decision(player_idx):
        decision = None
        while decision not in {'r', 'h'}:
            decision = input(f"Player {player_idx + 1} Roll or HOLD: ")
        return decision

    def _roll_route(self, player_idx):
        self._players[player_idx].roll(self._die)
        Game._print_all_info_after_roll(self, player_idx)

        if self._players[player_idx].temp_score >= 100:
            self._players[player_idx].update_score_with_temp()
            Game._winner = player_idx + 1
            return None

        elif self._die.face == 1:
            print(f"Player {player_idx + 1}'s turn ended with 1")
            return None

        else:
            Game.turn(self, player_idx)

    def _hold_route(self, player_idx):
        self._players[player_idx].hold()
        return None

    def turn(self, player_idx):
        if self._players[player_idx].is_computer:
            decision = self._players[player_idx].decision
        else:
            decision = Game._ask_player_for_decision(player_idx)

        if decision == 'r':
            Game._roll_route(self, player_idx)
        elif decision == 'h':
            Game._hold_route(self, player_idx)

    @property
    def winner(self):
        return Game._winner


class TimedGameProxy(Game):
    _start_time = perf_counter()

    def __init__(self, players, die, is_timed):
        super().__init__(players, die)
        self._is_timed = is_timed

    def time_up_winner(self):
        if self._players[0].score > self._players[1].score:
            Game._winner = 1
        elif self._players[0].score > self._players[1].score:
            Game._winner = 2
        else:
            print("It's an even game", end='\n\n')
            super().print_scores()
            quit()

    def turn(self, player_idx):
        if self._players[player_idx].is_computer:
            decision = self._players[player_idx].decision
        else:
            decision = super()._ask_player_for_decision(player_idx)

        current_time = perf_counter()
        if self._is_timed and \
                current_time - TimedGameProxy._start_time > 60:
            print("One minute has run out!!!")
            TimedGameProxy.time_up_winner(self)
            return None
        elif decision == 'r':
            super()._roll_route(player_idx)
        elif decision == 'h':
            super()._hold_route(player_idx)


def main(player1, player2, is_timed):
    players = PlayerFactory(player1, player2).p_list()
    die = Die()
    game = TimedGameProxy(players, die, is_timed)

    print('*' * 25)
    print('The Game of Pig', end='\n\n')

    playing = True
    while playing:
        for player_idx in range(len(players)):
            game.turn(player_idx)
            game.print_scores()

            if game.winner:
                print(f'Player {game.winner} has won!')
                playing = False
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="'human' or 'computer'",
                        type=str, required=True)
    parser.add_argument("--player2", help="'human' or 'computer'",
                        type=str, required=True)
    parser.add_argument("--timed", help="activate one minute timer",
                        action='store_true')
    args = parser.parse_args()
    main(args.player1, args.player2, args.timed)
