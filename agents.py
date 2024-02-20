import random
import time
import math
from state import State
from main_evaluation import count_consecutive_zeros
from main_evaluation import number_to_matrix
class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_column(self, state, max_depth):
        pass


class Human(Agent):
    pass


class ExampleAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        print(len(state.get_all_win_states()))
        print(max_depth)
        time.sleep(random.random())
        columns = state.get_possible_columns()
        return columns[random.randint(0, len(columns) - 1)]


class MinimaxABAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        _, column = self.minimax_alpha_beta(state, State.RED, -math.inf, math.inf, 0, max_depth)
        return column

    def minimax_alpha_beta(self, state, player, alpha, beta, curr_depth, depth):
        # ako smo stigli do dna(i fleg za ton je postavljen) ili smo stigli do odredjene dubine, ili smo stigli do terminalnog cvora
        if ((depth == 0 and state.get_state_status() is not None) or (
                curr_depth == depth and depth != 0) or state.get_state_status() is not None):
            return self.evaluate(state)

        sredina=3
        niz=[3,2,4,1,5,0,6]
        if player == State.RED:
            max_score = -math.inf
            best_column = None

            for column in state.get_possible_columns():

                successor_state = state.generate_successor_state(column)
                score, _ = self.minimax_alpha_beta(successor_state, State.YEL, alpha, beta, curr_depth + 1, depth)
                # max_score = max(max_score, score)
                if (score > max_score):
                    max_score = score
                    best_column = column
                if (score==max_score and niz.index(column) < niz.index(best_column)):
                    best_column = column

                alpha = max(alpha, score)

                if alpha >= beta:
                    break
            return max_score, best_column
        else:
            min_score = math.inf
            best_column = None

            for column in state.get_possible_columns():

                successor_state = state.generate_successor_state(column)
                score, _ = self.minimax_alpha_beta(successor_state, State.RED, alpha, beta, curr_depth + 1, depth)

                if (score < min_score):
                    min_score = score
                    best_column = column

                if(score==min_score and niz.index(column)<niz.index(best_column)):
                    best_column=column

                beta = min(beta, score)
                if alpha >= beta:
                    break
            return min_score, best_column

    def provera_polja(self, broj1, broj2):
        return (broj1 & broj2)!=0

    def dodatna_nagrada(self, broj):
        return 42 - bin(broj).count('1')

    def evaluate(self, state):
        if (state.get_state_status() == State.RED):
            return 100000, None
        elif (state.get_state_status() == State.YEL):
            return -100000, None
        else:
            '''
            player_wins = sum(1 for mask in state.win_masks if
                              self.provera_polja(state.checkers_yellow, mask))+ self.dodatna_nagrada(state.checkers_red)


            opponent_wins = sum(1 for mask in state.win_masks if
                                not self.provera_polja(state.checkers_red, mask))+ self.dodatna_nagrada(state.checkers_red)

            '''
            player_wins=count_consecutive_zeros(number_to_matrix(state.checkers_yellow)) #+self.dodatna_nagrada(state.checkers_red)
            print(player_wins)
            opponent_wins=count_consecutive_zeros(number_to_matrix(state.checkers_red)) #+self.dodatna_nagrada(state.checkers_yellow)
            print(opponent_wins)
            evaluation = abs(player_wins - opponent_wins)
            return evaluation, None


class Negascout(Agent):

    def get_chosen_column(self, state, max_depth):
        _, column = self.negascout(state, State.RED, -math.inf, math.inf, 0, max_depth)
        return column

    def negascout(self, node, player, alpha, beta, curr_depth, depth):

        if ((depth == 0 and node.get_state_status() is not None) or (
                curr_depth == depth and depth != 0) or node.get_state_status() is not None):
            return self.evaluate(node)[0] * (-1 if player == State.YEL else 1), None

        score = -math.inf
        best_column = None

        niz = [3, 2, 4, 1, 5, 0, 6]

        for column in node.get_possible_columns():
            successor_state = node.generate_successor_state(column)
            val, _ = self.negascout(successor_state, self.switch(player), -beta, -alpha, curr_depth + 1, depth)
            val = -val
            if alpha < val < beta:
                val, _ = self.negascout(successor_state, self.switch(player), -beta, -alpha, curr_depth + 1, depth)
                val = -val

            if(val>score):
                score=val
                best_column=column

            if(val==score and niz.index(column)<niz.index(best_column)):
                best_column=column


            alpha = max(alpha, score)

            if alpha >= beta:
                break
        return score, best_column

    def provera_polja(self, broj1, broj2):
        return (broj1 & broj2) != 0

    def dodatna_nagrada(self, broj):
        return 42 - bin(broj).count('1')

    def evaluate(self, state):
        if (state.get_state_status() == State.RED):
            return 100000, None
        elif (state.get_state_status() == State.YEL):
            return -100000, None
        else:

            player_wins = sum(1 for mask in state.win_masks if
                              self.provera_polja(state.checkers_yellow, mask)) + self.dodatna_nagrada(
                state.checkers_red)

            opponent_wins = sum(1 for mask in state.win_masks if
                                not self.provera_polja(state.checkers_red, mask)) + self.dodatna_nagrada(
                state.checkers_red)

            evaluation = abs(player_wins - opponent_wins)
            return evaluation, None

    def switch(self, player):
        return State.RED if player == State.YEL else State.YEL