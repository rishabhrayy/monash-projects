# FIT5215 — Deep Learning

**Semester:** Semester 2, 2025
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

A low-level deep learning unit focused on building neural network components from mathematical first principles using PyTorch's tensor and autograd primitives — not its high-level abstractions. Every layer, activation function, and optimiser is implemented manually. The result is a working feedforward network trained on MNIST digit classification, demonstrating that an understanding of the gradient flow, not just the API, drives effective neural network engineering.

---

## What I Worked On

- Derived ELU (Exponential Linear Unit) and GELU (Gaussian Error Linear Unit) analytically and implemented both activation functions with their exact derivatives for use in backpropagation
- Built a custom linear layer (`MyLinear`) using `torch.nn.Module`, implementing the forward pass with manual weight and bias operations — no `torch.nn.Linear`
- Assembled a multi-layer feedforward network (`MyFFN`) from custom layers, with softmax output and cross-entropy loss via `torch.nn.functional`
- Implemented vanilla SGD with manual parameter updates (no `torch.optim` call)
- Extended to SGD with momentum by manually accumulating velocity vectors across steps
- Implemented AdaGrad from scratch with per-parameter cumulative squared gradient tracking
- Trained and evaluated the full network on MNIST (flattened 784-dimensional inputs, 10-class output) and compared convergence behaviour across all three optimisers

---

## Methods and Approaches

- **Analytical activation function derivation** — ELU and GELU computed from definition including GELU's CDF approximation via `scipy.stats.norm`
- **Custom layer design** using `torch.nn.Module` subclassing with proper parameter registration
- **Manual gradient-based optimisation** — SGD, SGD+momentum, and AdaGrad all implemented via direct tensor arithmetic
- **MNIST multi-class classification** as a concrete evaluation benchmark for implementation correctness
- **Optimiser convergence comparison** to understand how adaptive and momentum-based methods differ in practice

---

## Work Breakdown

**Ass 1** → Full from-scratch deep learning pipeline: ELU/GELU derivation and implementation, `MyLinear` and `MyFFN` custom classes, three manual optimisers (SGD, SGD+momentum, AdaGrad), trained end-to-end on MNIST with comparative convergence analysis

---

## Key Skills Demonstrated

- Deriving and implementing activation functions from mathematical definitions
- Building neural network components using low-level PyTorch tensor operations
- Implementing gradient descent variants (SGD, momentum, AdaGrad) without framework optimisers
- Understanding how backpropagation flows through custom layers
- Evaluating optimiser behaviour empirically on a real classification benchmark

---

## Key Insights

- Implementing AdaGrad manually makes clear why learning rate scaling by accumulated gradient magnitude matters — parameters with infrequent updates receive larger effective steps
- GELU's smoothness near zero, relative to ReLU's hard threshold, has a meaningful effect on gradient flow in early training — observable empirically when comparing activation functions
- The gap between "using PyTorch" and "understanding PyTorch" is significant; manual implementation closes that gap in a way that debugging production models later rewards

---

## Relevance to Industry

- **ML/AI Engineering:** Low-level framework knowledge is essential for custom layer development, model debugging, and performance profiling in production ML systems
- **Research Engineering:** Understanding the mathematical basis of optimisers is a prerequisite for reading and implementing papers that propose new training dynamics
- **Deep Learning Infrastructure:** Engineers who can work below the `torch.nn` API level are significantly more effective at diagnosing and fixing silent numerical errors

---

## Tools and Technologies

- Python 3
- PyTorch (`torch`, `torch.nn`, `torch.nn.functional`)
- torchvision (MNIST dataset and transforms)
- NumPy, Matplotlib
- SciPy (`scipy.stats.norm` for GELU approximation)
- tqdm

---

## Getting Started

```bash
pip install torch torchvision numpy matplotlib scipy tqdm
jupyter notebook "Ass 1/34525416_assignment01_solution/34525416_assignment01_solution/34525416_assignment01_solution_Q1_Q2.ipynb"
```

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
