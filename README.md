# AlphaGomokuZero
An illustration program which visualizes CNN filters inside AlphaZero and its MCTS mechanism in order to provide a better understanding of how an AI makes decisions. Based Tensorflow and Tkinter. Exhibited at China Science and Technology Museum.
一个通过可视化Alphago Zero中的MCTS机制来解释AI决策方式的程序。展出于中国科技馆。

## Screenshots



## Training

The training module is based on https://github.com/junxiaosong/AlphaZero_Gomoku.
I experimented numerous models and added a multi-thread training scheme for the policy value net.

```
training
├── main.py                             Main script.
└── src
    ├── __init__.py
    ├── human_play.py                   A simple command-line client for human play.
    ├── model
    │   ├── __init__.py
    │   ├── game.py                     Defines rules of Gomoku Game.
    │   ├── inception_resnet_v2.py    
    │   ├── mcts_alphaZero.py           AlphaZero player.
    │   ├── mcts_pure.py                MCTS player.
    │   ├── pvn_inception.py            inception version of the policy value net.
    │   ├── pvn_resnet.py               resnet version of the policy value net.
    │   └── resnet.py
    ├── train_pipeline.py               Training pipeline.
    ├── train_thread.py                 A single training thread.
    └── utils.py                        Utilities.
```

## Demonstration

Illustration program with GUI. Allows users to play game with AlphaZero and see visualizations of Monte Carlo Tree Search.
Implemented with Tkinter on python3.

### GUI Structure
```
GameApp
├── WelcomeScene                        Welcome Screen.
├── OrderSelectionScene                 Scene for selecting play order.
├── GameScene                           Game Screen.
├── IdleScene                           Displayed when game is not played.
└── ThinkScene                          Displays visualizations of MCTS.
```

### Directory Stucture
```
demonstration/
├── Main.py                             Main script.
├── img                                 Store image resources.
├── mdl                                 Store trained models
├── src
│   ├── GameApp.py                      
│   ├── GameScene.py
│   ├── IdleScene.py
│   ├── OrderSelectionScene.py
│   ├── ThinkScene.py
│   ├── WelcomeScene.py
│   ├── __init__.py
│   ├── components                      UI components.
│   ├── config.py                       Configurations.
│   ├── model                           Basic models of game and AI.
│   │   ├── CrossPoint.py
│   │   ├── Gomoku.py
│   │   ├── MCTS_AlphaZero.py
│   │   ├── MCTS_Pure.py
│   │   ├── PVN_11.py
│   │   └── __init__.py
│   └── play_data.py                    Data structure used to store play data.
└── static                              Place to store play data
```
