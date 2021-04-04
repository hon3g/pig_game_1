import argparse
import random
random.seed(0)


class Player:
    def __init__(self):
        self._score = 0
        self._turn_total = 0
        self._temp_score = self._score + self._turn_total

    def __repr__(self):
        return f'{0}({1}, {2}, {3})'.format(
            self.__class__.__name__,
            self._score, self._turn_total,
            self._temp_score)

    @property
    def score(self):
        return self._score

    @property
    def turn_total(self):
        return self._turn_total

    @property
    def temp_score(self):
        return self._temp_score

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
    pass


class PlayerFactory:
    pass


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
        print(f'rolling number: {self._die.face}')
        print(f'turn total: {self._players[player_idx].turn_total}')
        Game.print_scores(self)

    @staticmethod
    def _ask_player_for_decision(player_idx):
        deci = None
        while deci not in {'r', 'h'}:
            deci = input(f"Player {player_idx + 1} Roll or HOLD: ")
        return deci

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
        decision = Game._ask_player_for_decision(player_idx)

        if decision == 'r':
            Game._roll_route(self, player_idx)

        elif decision == 'h':
            Game._hold_route(self, player_idx)

    @property
    def winner(self):
        return Game._winner


def main(num_players, num_games):
    num_players, num_games = num_players or 2, num_games or 1

    for _ in range(num_games):
        print('*' * 25)
        print('The Game of Pig', end='\n\n')

        players = [Player() for _ in range(num_players)]
        die = Die()
        game = Game(players, die)

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
    parser.add_argument("--numPlayers", help="number of players",
                        type=int)
    parser.add_argument("--numGames", help="number of games",
                        type=int)
    args = parser.parse_args()
    main(args.numPlayers, args.numGames)
