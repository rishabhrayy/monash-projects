# FIT5226 — Multi-Agent Systems and Collective Behaviour

**Semester:** Semester 1, 2025
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

Cooperative and competitive multi-agent reinforcement learning, with a focus on the coordination challenges that emerge when multiple independent learning agents share an environment. The unit goes beyond single-agent RL to address collision avoidance, curriculum design, and collective task completion under strict performance budgets. The assignment trains four independent DQN agents to coordinate an indefinite shuttle task on a 5×5 grid — a problem where naïve independent learning fails without careful architectural and training design choices.

---

## What I Worked On

- Designed and trained four independent DQN agents, each with a 3-layer MLP (256 hidden units, ReLU), to complete a cooperative shuttle task on a 5×5 grid without pre-assigned roles
- Implemented a double-network architecture (online + target) with Polyak soft-update (τ = 1e-3) to stabilise training
- Built an experience replay buffer (capacity 200,000) with mini-batch sampling (batch size 256) to decorrelate training updates
- Implemented ε-greedy exploration with exponential decay (0.85 → 0.02) to balance exploration and exploitation across training
- Designed a curriculum learning strategy grouping the 9,600 possible scenarios by Manhattan distance ({1, 2, 4, 8}) between pickup and dropoff cells, training agents on easier configurations first
- Implemented head-on collision (agent swap) detection and penalisation in the shared grid reward structure
- Monitored Q-value convergence and rolling delivery success rate across training to track learning stability

---

## Methods and Approaches

- **Independent DQN** with separate replay buffers and target networks per agent
- **Double-network (online/target) architecture** with Polyak soft-update for training stability
- **Experience replay** with uniform mini-batch sampling to break temporal correlation
- **ε-greedy exploration** with exponential decay schedule
- **Curriculum learning** ordered by task difficulty (Manhattan distance proxy)
- **Swap collision detection** and reward shaping for cooperative safety constraints
- **Adam optimiser** (lr = 3e-4), discount factor γ = 0.8

---

## Work Breakdown

**Ass 1** → Full DQN multi-agent training pipeline: double-network architecture, experience replay, curriculum learning across 9,600 scenarios ordered by Manhattan distance, head-on collision penalisation, and convergence monitoring with rolling success rate visualisation

---

## Key Skills Demonstrated

- Implementing Deep Q-Networks from scratch in PyTorch with full training infrastructure
- Designing curriculum learning schedules based on task complexity proxies
- Multi-agent coordination with collision avoidance in shared environments
- Stabilising RL training via target networks, soft updates, and replay buffers
- Experimental design for RL: tracking convergence, success rate, and Q-value stability

---

## Key Insights

- Curriculum learning by Manhattan distance dramatically accelerates convergence compared to random scenario sampling — agents learn the easier sub-tasks before confronting harder configurations
- Head-on collision penalisation must be tuned carefully: too strong and it dominates the task reward, causing agents to freeze rather than navigate; too weak and collisions persist late into training
- Independent DQN is not cooperative by design — emergent coordination arises purely from shared environment dynamics and reward shaping, which makes the resulting behaviour fragile to distribution shift

---

## Relevance to Industry

- **Robotics / Warehouse Automation:** Multi-agent coordination with collision avoidance is a core problem in autonomous warehouse systems (e.g. Amazon Robotics, Agility Robotics)
- **Autonomous Vehicles:** Independent DQN with collision penalisation mirrors simplified versions of the multi-vehicle coordination problem in urban driving
- **RL Engineering:** The full training pipeline demonstrated here — curriculum, replay, soft updates, convergence monitoring — represents production-grade RL system design

---

## Tools and Technologies

- Python 3
- PyTorch (`torch`, `torch.nn`, `torch.optim`, `torch.nn.functional`)
- NumPy, Matplotlib, Seaborn, Pandas

---

## Getting Started

```bash
pip install torch numpy matplotlib seaborn pandas
jupyter notebook "Ass 1/FIT5226_34525416.ipynb"
```

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
