import time

from src.ai.boards.board_agent_for_ai import TetrisAgentForAI

agent = TetrisAgentForAI()

agent.set_random_block()
while True:
    agent.random_move()
    print(agent.board)
    time.sleep(0.3)
