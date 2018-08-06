from threading import Thread
import time
from src.model.game import Board, Game
from src.utils import *

class TrainThread(Thread):
    def __init__(self, id, master, visualize=False):
        Thread.__init__(self)
        self.id = id
        self.master = master
        self.job = None
        self.visualize = visualize

    def run(self):
        try:
            while True:
                self.job = self.master.dispatch()
                if self.job == TRAIN:
                    self.run_train()
                elif self.job == PLAY:
                    self.run_play()
                elif self.job == EVAL:
                    self.run_eval()
        except KeyboardInterrupt:
            return

    def run_train(self):
        self.master.policy_update()

    def run_play(self):
        time1 = time.time()
        self.board = Board(width=N, height=N, n_in_row=N_WIN)
        self.game = Game(self.board)
        winner, play_data, moves = self.game.start_self_play(self.master.mcts_players[self.id],
                                                             temp=self.master.temperature, 
                                                             is_shown=self.visualize)
        play_data = list(play_data)[:]
        time2 = time.time()
        play_data = augment(play_data)
        self.master.tee("thrd %d, %d moves in %.2f mins, %.2fs per move" % (self.id, moves, ((time2 - time1) / 60) ,((time2 - time1) / moves)))
        self.play_data = play_data
        self.master.play_job_deliver(self.play_data)

    def run_eval(self):
        pass