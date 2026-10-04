# AI systems, built from first principles

Coursework from my Master of Artificial Intelligence at Monash University (2024 to 2025), kept as a portfolio. The common thread is building the algorithm rather than calling it: optimisers on raw tensors instead of `torch.optim`, cross-validation instead of `GridSearchCV`, a particle filter instead of a library.

## Start here

| | What it is | Why it is worth a look |
|---|---|---|
| **[Multi-agent DQN](FIT5226%20Multi%20agent%20systems%20and%20collective%20behaviour%20-%20S1%202025)** | Four agents learn to share a shuttle task on a grid | Independent learners usually collide and stall. Target networks, a 200k replay buffer and a curriculum that starts with short trips make them cooperate. |
| **[Hybrid Pacman agent](FIT5222%20Planning%20and%20automated%20reasoning%20-%20S2%202025)** | A competitive team that cannot see its opponents | Three kinds of reasoning in one agent: symbolic strategy, a particle filter tracking hidden enemies, and A* that weighs risk. |
| **[Deep learning by hand](FIT5215%20Deep%20learning%20-%20S2%202025)** | A feedforward network with no `nn.Linear` and no `torch.optim` | Every layer, activation, derivative and optimiser written out, then compared on MNIST. |
| **[KNN and model selection](FIT5201%20Machine%20learning%20-%20S2%202025)** | KNN regression and honest model selection | Scaling fitted on training data only, cross-validation written from scratch, and the one-standard-error rule to prefer the simpler model. |

## Every unit

| Unit | Topic | What I built | Tools |
|---|---|---|---|
| [FIT5226](FIT5226%20Multi%20agent%20systems%20and%20collective%20behaviour%20-%20S1%202025) | Multi-agent systems | Four DQN agents learn a shared shuttle task with no assigned roles: target networks, replay, curriculum by task distance, collision penalties | PyTorch |
| [FIT5222](FIT5222%20Planning%20and%20automated%20reasoning%20-%20S2%202025) | Planning | A* with conflict detection and local repair for multi-agent rail pathfinding; a Pacman team mixing symbolic strategy, a particle filter for hidden opponents, and risk-aware A* | Python, PDDL |
| [FIT5215](FIT5215%20Deep%20learning%20-%20S2%202025) | Deep learning | Layers, ELU and GELU, and SGD, momentum and AdaGrad written by hand on raw tensors, trained on MNIST | PyTorch tensors |
| [FIT5201](FIT5201%20Machine%20learning%20-%20S2%202025) | Machine learning | KNN regression with a KDTree, leak-free scaling, cross-validation from scratch and the one-standard-error rule | NumPy |
| [FIT5047](FIT5047%20Fundamentals%20of%20artificial%20intelligence%20-%20S1%202025) | AI fundamentals | Search, logic, and Bayesian networks built and queried in Netica | Netica |
| [FIT5216](FIT5216%20Modelling%20discrete%20optimisation%20problems%20-%20S1%202025) | Discrete optimisation | Constraint models for vaccine scheduling under a budget and for service scheduling with two competing objectives | MiniZinc |
| [FIT9132](FIT9132%20Introduction%20to%20databases%20-%20S2%202024) | Databases | ER design to 3NF, Oracle SQL with JSON output, and the same data as MongoDB documents | SQL, MongoDB |
| [FIT9136](FIT9136%20Algorithms%20and%20programming%20foundations%20in%20Python%20-%20S2%202024) | Algorithms in Python | A state machine for login, graph search over a family tree, and an object-oriented inventory, standard library only | Python |
| [MAT9004](MAT9004%20-%20Mathematical%20foundations%20for%20data%20science%20and%20AI%20-%20S2%202024) | Maths for AI | Linear algebra, multivariable calculus, probability and inference, by derivation | Maths |
| [FIT5152](FIT5152%20User%20interface%20design%20and%20usability%20-%20S2%202025) | UI design and usability | Heuristic evaluation, prototypes, and think-aloud usability testing, as a team | Prototyping, user research |
| [FIT5057](FIT5057%20Project%20management%20-%20S2%202024) | Project management | Business case, WBS and critical path, risk register, and agile planning | Planning |

Each folder has its own README with the unit overview, what I worked on, and the methods used.

## Skills, mapped

- **Reinforcement learning**: DQN, experience replay, target networks, curriculum learning (FIT5226)
- **Search and planning**: A*, conflict detection, PDDL, particle filters (FIT5222, FIT5047)
- **Deep learning**: backpropagation, activations, optimisers from scratch (FIT5215)
- **Machine learning**: KNN, cross-validation, bias and variance, model selection (FIT5201)
- **Optimisation**: constraint programming in MiniZinc (FIT5216)
- **Data**: relational design, SQL, MongoDB (FIT9132)

## More of my work

Shipped projects, each with a live demo, are on my [GitHub profile](https://github.com/rishabhrayy) and at [rishabhray.me](https://rishabhray.me).

## Note

This is academic coursework, restructured as a portfolio. Unit materials belong to Monash University. Team submissions in FIT5152 and FIT5057 were group work.
