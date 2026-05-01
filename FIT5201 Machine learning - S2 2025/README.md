# FIT5201 — Machine Learning

**Semester:** Semester 2, 2025
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

A mathematically rigorous treatment of machine learning that demands from-scratch implementation rather than high-level framework usage. The focus is on understanding what algorithms actually do — not just calling `model.fit()`. Work spans regression, model complexity analysis, and statistically sound model selection, implemented in NumPy with the only permitted external search structure being scikit-learn's KDTree. This constraint forces engagement with the underlying mathematics at every step.

---

## What I Worked On

- Built a k-nearest neighbour regressor from scratch using a KDTree for efficient spatial lookup, without using any scikit-learn estimator wrappers
- Implemented custom min-max feature normalisation fitted exclusively on training data to prevent data leakage from the test set
- Swept k from 1 to 60 on the scikit-learn diabetes dataset and analysed the resulting bias-variance tradeoff curve, identifying underfitting and overfitting regimes
- Implemented L-fold cross-validation from scratch with optional shuffling and reproducible random seeding
- Applied the one-standard-error rule to select a conservative, simpler model from a noisy CV error curve
- Automated model selection via inner cross-validation on the training fold, then refitted on the full training set before evaluating on the held-out test set

---

## Methods and Approaches

- **KNN regression** with Euclidean distance in normalised feature space
- **Manual L-fold cross-validation** with reproducible splits and 95% confidence interval estimation
- **Bias-variance tradeoff analysis** across the full complexity spectrum (k = 1 to 60)
- **One-standard-error rule** for principled model selection under CV uncertainty
- **Nested cross-validation** pattern (inner CV for selection, outer split for unbiased error estimation)
- **MSE** as the primary evaluation metric throughout

---

## Work Breakdown

**Ass 1** → From-scratch KNN regressor on the diabetes dataset: min-max scaling, k sweep from 1 to 60, manual L-fold CV with 95% CIs, one-standard-error rule model selection, and inner-CV-based automatic model selection evaluated against held-out test error

---

## Key Skills Demonstrated

- Implementing ML algorithms from mathematical definitions, not API calls
- Preventing data leakage through rigorous train/test discipline
- Statistically grounded model selection using cross-validation and confidence intervals
- Bias-variance analysis and its implications for model complexity decisions
- Clean experimental design with reproducible random seeds

---

## Key Insights

- Leaking test set statistics into normalisation is a subtle but pervasive error in practice — implementing it manually makes the failure mode viscerally clear
- The one-standard-error rule is a principled way to prefer simpler models when CV curves are noisy — important when deploying models to new data distributions
- Inner CV for model selection followed by outer evaluation is the correct pattern for unbiased performance estimation; conflating the two is one of the most common mistakes in applied ML benchmarking

---

## Relevance to Industry

- **ML Engineering:** From-scratch implementation skills separate engineers who understand their tools from those who merely use them — critical for debugging model failures in production
- **Data Science:** Rigorous cross-validation and model selection practices directly impact the reliability of deployed models
- **Research:** The experimental rigour demonstrated here (reproducible seeding, proper data splits, CI-based reporting) is a prerequisite for credible ML research

---

## Tools and Technologies

- Python 3.12
- NumPy
- Matplotlib
- scikit-learn (KDTree and diabetes dataset only)

---

## Getting Started

```bash
pip install numpy matplotlib scikit-learn
jupyter notebook "Ass 1/34525416_RISHABH_RAY_Assignment1/34525416_RISHABH_RAY_Assignment1/34525416_RISHABH_RAY_a1_sec1.ipynb"
```

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
