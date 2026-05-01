# FIT5047 — Fundamentals of Artificial Intelligence

**Semester:** Semester 1, 2025
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

A rigorous introduction to the core reasoning mechanisms that underpin modern AI systems — search, knowledge representation, and probabilistic inference. The unit builds from deterministic search strategies through to probabilistic graphical models, providing a theoretical and practical foundation for understanding how intelligent agents handle uncertainty. The capstone deliverable is a working Bayesian network constructed in Netica.

---

## What I Worked On

- Analysed classical AI search algorithms (uninformed and informed) and their applicability to structured problem spaces
- Reasoned formally about knowledge representation using propositional and first-order logic
- Constructed a six-node Bayesian network (SmokeAlarmBN) modelling a realistic fire-safety scenario
- Specified prior and conditional probability distributions for each node, encoding causal dependencies between fire, tampering, alarm, smoke, evacuation, and reporting
- Performed probabilistic inference by computing posterior beliefs under different evidence configurations (e.g. alarm active but no smoke observed)

---

## Methods and Approaches

- **Bayesian network construction** using directed acyclic graph (DAG) structure with discrete chance nodes
- **Conditional probability table (CPT) specification** for each non-root node based on parent states
- **Belief propagation** for exact inference over the network given observed evidence
- **Probabilistic reasoning under uncertainty** — evaluating how prior knowledge is updated by partial observations

---

## Work Breakdown

**Ass 1** → Written analysis of AI search strategies: completeness, optimality, and complexity trade-offs across BFS, DFS, UCS, and A\*

**Ass 2** → Formal reasoning problems in propositional and predicate logic; entailment proofs and knowledge-base construction

**Ass 3** → Bayesian network modelling in Netica: six-node smoke alarm scenario with full CPT specification and inference queries under multiple evidence conditions

---

## Key Skills Demonstrated

- Probabilistic graphical model design and inference
- Encoding domain knowledge as structured conditional dependencies
- Reasoning about uncertainty without exhaustive enumeration
- Translating real-world causal relationships into a formal DAG representation
- Evaluating AI search strategies across theoretical complexity dimensions

---

## Key Insights

- A well-structured prior can significantly constrain inference even when only indirect evidence is available — demonstrated clearly by marginalising over unobserved nodes in the smoke alarm network
- The choice of network topology (causal vs. diagnostic direction) changes the efficiency and interpretability of inference substantially
- Classical search and probabilistic reasoning are complementary: deterministic environments suit search; uncertain, partial-observation environments demand probabilistic models

---

## Relevance to Industry

- **AI/ML Engineering:** Bayesian networks underpin medical diagnosis systems, fraud detection pipelines, and sensor fusion in robotics
- **Data Science:** Conditional probability reasoning is the foundation of Naive Bayes classifiers, Kalman filters, and causal inference frameworks
- **AI Safety & Explainability:** Graphical models provide interpretable, auditable reasoning chains — increasingly valued in regulated sectors

---

## Tools and Technologies

- Netica 7.01 — Bayesian network modelling and inference

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
