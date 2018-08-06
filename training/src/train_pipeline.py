# -*- coding: utf-8 -*-
"""
Multi-thread implementation of the training pipeline of AlphaZero for Gomoku

@author: Zhuoqian Yang
"""

from __future__ import print_function
import random
import time
import os
import sys
import pickle
from collections import defaultdict, deque
from src.model.mcts_pure import MCTSPlayer as MCTS_Pure
from src.model.mcts_alphaZero import MCTSPlayer
from src.model.pvn_resnet import PolicyValueNet
from src.train_thread import TrainThread
from src.utils import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class TrainPipeline():
    def __init__(self, ckpt=0, visualize=False):
        # training params
        self.learn_rate = 2e-4
        self.lr_multiplier = 1.0  # adaptively adjust the learning rate based on KL
        self.temperature = 1.0  # the temperatureerature param
        self.n_playout = 400  # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.batch_size = 512  # mini-batch size for training
        self.epochs = 5  # num of train_steps for each update
        self.kl_targ = 0.02

        # accounting
        self.train_dir = os.path.join('.', 'train', 'resnet_11x11')
        self.log_dir = os.path.join(self.train_dir, 'tensorboard')
        self.save_freq = 50
        self.eval_points = [1000, 2000, 3000, 4000]
        self.total_trained = 0.0
        self.last_update = time.time()

        # load progress
        self.i = ckpt+1
        self.init_model(ckpt)
        self.init_memory(ckpt)
        self.init_progress(ckpt)

        # threads
        if visualize: self.n_thread = 1
        else: self.n_thread = 1
        self.remaining_train_jobs = 0
        self.accumulating = True
        self.accumulation_threshold = self.n_thread
        self.threads = [TrainThread(i, self, visualize=visualize) for i in range(self.n_thread)]
        self.mcts_players = []

        self.play_locked = False
        self.train_locked = False
        self.dispatch_locked = False

        random.seed(int((time.time()%1)*1000000))

    def init_model(self, ckpt):
        if ckpt > 0:
            model_path = os.path.join(self.train_dir, 'models', '%d.model' % ckpt)
            self.pvn = PolicyValueNet(N, N, model_file=model_path, is_training=True, log_dir=self.log_dir)
        else:
            self.pvn = PolicyValueNet(N, N, is_training=True, log_dir=self.log_dir)

    def init_memory(self, ckpt):
        if ckpt > 0:
            mem_file = open(os.path.join(self.train_dir, 'memory.deque'), "rb")
            self.memory = pickle.load(mem_file)
            mem_file.close()
            if len(self.memory) != self.buffer_size:
                self.tee("memory size changed from %d to %d" % (len(self.memory), self.buffer_size))
                old = self.memory
                self.memory = deque(maxlen=self.buffer_size)
                for obj in old:
                    self.memory.append(obj)
                del old

        else:
            self.memory = deque(maxlen=self.buffer_size)
            

    def init_progress(self, ckpt):
        if ckpt > 0:
            with open(os.path.join(self.train_dir, 'progress.pkl'), 'rb') as prog_file:
                prog = pickle.load(prog_file)
                self.total_trained = prog['total_trained']
                self.lr_multiplier = prog['lr_multiplier']
        else:
            self.total_trained = 0.0
            self.lr_multiplier = 1.0

    def dispatch(self):
        while self.dispatch_locked: time.sleep(0.01)
        self.dispatch_locked = True

        if self.remaining_train_jobs >= self.accumulation_threshold:
            self.accumulating = False

        job = PLAY
        if self.remaining_train_jobs > 0 and not self.accumulating:
            self.remaining_train_jobs -= 1
            job = TRAIN
            if self.remaining_train_jobs == 0:
                self.accumulating = True

        self.dispatch_locked = False
        return job

    def tee(self, str):
        with open(os.path.join(self.train_dir, 'train_log.txt'), "a") as myfile:
            myfile.write(str + "\n")
        print(str)

    def play_job_deliver(self, play_data):
        while self.play_locked: time.sleep(0.01)
        self.play_locked = True
        self.memory.extend(play_data)
        if len(self.memory) > self.batch_size:
            self.remaining_train_jobs += 1
        self.play_locked = False

    def policy_update(self):
        """update the policy-value net"""

        while self.train_locked: time.sleep(0.1)
        self.train_locked = True

        self.train_step()
        
        if self.i % self.save_freq == 0:
            self.save()

        self.i += 1
        self.train_locked = False

    def train_step(self):
        mini_batch = random.sample(self.memory, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]
        old_probs, old_v = self.pvn.policy_value(state_batch)

        loss, entropy, summary, kl, new_v = None, None, None, None, None
        for i in range(self.epochs):
            loss, entropy, summary = self.pvn.train_step(
                    state_batch,
                    mcts_probs_batch,
                    winner_batch,
                    self.learn_rate*self.lr_multiplier)
            new_probs, new_v = self.pvn.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (
                    np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)),
                    axis=1)
            )
            if kl > self.kl_targ * 4:  # early stopping if D_KL diverges badly
                break

        # record summary
        self.pvn.write_summary(summary, self.i)

        # adaptively adjust the learning rate
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1:
            self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10:
            self.lr_multiplier *= 1.5

        explained_var_old = (1 -
                             np.var(np.array(winner_batch) - old_v.flatten()) /
                             np.var(np.array(winner_batch)))
        explained_var_new = (1 -
                             np.var(np.array(winner_batch) - new_v.flatten()) /
                             np.var(np.array(winner_batch)))

        now = time.time()
        self.total_trained += now-self.last_update
        self.last_update = now
        self.tee(("update {} at {:.2f} hrs | "
                  "kl:{:.5f}, lr_multiplier:{:.3f}, loss:{}, entropy:{},"
                  "explained_var_old:{:.3f}, explained_var_new:{:.3f}"
                  ).format(self.i, self.total_trained/3600,
                           kl, self.lr_multiplier, loss, entropy,
                           explained_var_old, explained_var_new))


    def save(self):
        self.pvn.save_model(os.path.join(self.train_dir, 'models', '%d.model' % self.i))
        with open(os.path.join(self.train_dir, 'progress.pkl'), "wb") as prog_file:
            prog = {}
            prog['total_trained'] = self.total_trained
            prog['lr_multiplier'] = self.lr_multiplier
            pickle.dump(prog, prog_file)
        with open(os.path.join(self.train_dir, 'memory.deque'), "wb") as mem_file:
            pickle.dump(self.memory, mem_file)
        self.tee("progress saved at iteration %d" % self.i)

            
    def run(self):
        for i in range(self.n_thread):
            player = MCTSPlayer(self.pvn.policy_value_fn,
                                c_puct=self.c_puct,
                                n_playout=self.n_playout,
                                is_selfplay=True)
            self.mcts_players.append(player)
            time.sleep(0.1)

        self.tee("traning started at iteration %d" % self.i)   

        try:
            for thread in self.threads:
                thread.daemon=True
                thread.start()
            while True: time.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            print("Interrupted at iteration %d" % self.i)
            sys.exit(0)