import sys
import traceback
import pygame

from state import State
from game import Game

state=State()
print(state)
state=state.generate_successor_state(3)
print(state)
print(state.get_checkers(State.RED))
print(state.get_checkers(State.YEL))
print(state.win_masks)
print('------------------------------------')
# Kreiraj novo stanje igre
stanje_igre = State()

# Prikazi trenutno stanje
print(stanje_igre)

# Dobavi vrednosti figura za crvenog igrača
crvene_figure = stanje_igre.get_checkers(State.RED)
print(crvene_figure)
# Dobavi sledećeg igrača na potezu
sledeci_igrac = stanje_igre.get_next_on_move()
print(sledeci_igrac)
# Dobavi status igre
status_igre = stanje_igre.get_state_status()
print(status_igre)
# Dobavi moguće kolone za sledeći potez
moguce_kolone = stanje_igre.get_possible_columns()
print(moguce_kolone)
# Napravi potez u određenoj koloni
novo_stanje = stanje_igre.generate_successor_state(3)
print(novo_stanje)
print(stanje_igre.get_next_on_move())
print(stanje_igre.get_win_checkers_positions())

try:
    module_agents = __import__('agents')
    first_agent_class = getattr(module_agents, sys.argv[1] if len(sys.argv) > 1 else 'Human')
    second_agent_class = getattr(module_agents, sys.argv[2] if len(sys.argv) > 2 else 'ExampleAgent')
    max_depth = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    max_think_time = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    actions_filename = sys.argv[5] if len(sys.argv) > 5 else None
    g = Game([first_agent_class(), second_agent_class()], max_depth, max_think_time, actions_filename)
    g.run()
except (Exception,):
    traceback.print_exc()
    input()
finally:
    pygame.display.quit()
    pygame.quit()


