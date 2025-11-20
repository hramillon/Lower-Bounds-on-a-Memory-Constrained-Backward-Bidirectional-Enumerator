# Lower Bounds on a Memory-Constrained Bidirectional Enumerator

## Table of Contents

## Abstract

We study the relation between the time needed and the memory available for a specifically chosen sequence of operations, in this case the enumeration of n elements in a unidirectional enumerator. Our objective is twofold: first, to establish a general lower bound on the performance of any bidirectional enumerator operating within bounded memory; second, to construct explicit enumerators that closely approach these bounds after deamortization. We consider three distinct memory regimes—constant memory $\Theta(1)$, linear memory $\Theta(n)$, and logarithmic memory $\Theta(\log n)$—and show that in each case, the work per operation can match the theoretical lower bounds up to tight asymptotic factors: respectively $\Theta(1)$, $\Theta(n)$, and $\Theta(\log n)$.

To unify these regimes, we introduce a novel relationship that governs the trade-off between memory usage and computational cost. We rigorously prove this relationship and use it to derive an optimality framework applicable to all three cases. Our approach includes a detailed analysis of the recursion underlying the enumeration process, focusing on its optimal segments. This analysis is supported by empirical data, validating the theoretical predictions and guiding the fine-tuning of the recursive structure.

We implemented the resulting algorithms in Python, producing practical enumerators that come with provable guarantees on both average throughput and worst-case latency. Our work provides a comprehensive and practically viable framework for designing nearly optimal bidirectional enumerators under strict memory constraints.

## Introduction

Efficient enumeration of data under memory constraints is a fundamental problem with significant implications in both theory and practice. We study the problem of enumerating a sequence in both forward and backward directions using sublinear memory, and we quantify the recomputation cost required to support backward traversal. This is especially relevant for unidirectional data structures such as hashchains, where backward traversal is not natively supported.

To illustrate this, consider a sequence of commits in a Git repository:

```
Commit A → Commit B → Commit C
```

Each commit includes the hash of its predecessor. In such structures, forward traversal is straightforward: from Commit A one can derive Commit B, and then Commit C. However, given only Commit C, reconstructing Commit B is infeasible because cryptographic hash functions are one-way. Thus, backward traversal requires storing intermediate states, and a hashchain provides precisely the forward-only behavior that characterizes constrained enumeration models.

In constrained environments such as streaming or external memory models, one cannot store all intermediate states and must rely on sparse checkpointing to simulate backward movements. Our objective is to quantify the optimal tradeoff between memory usage and backward traversal cost, and to construct algorithms that achieve this optimal tradeoff.

This problem has been studied from various perspectives for a long time. Early results by Munro and Paterson and Beame show that any sequential algorithm operating with sublinear memory must pay a superlinear computational cost. Vitter's survey outlines the challenges of constrained I/O, which inspire the structural constraints considered in our model. Brodal and Fagerberg's lower bounds for external memory dictionaries motivate the search for fundamental limits under restricted memory. Sparse checkpointing, central to our approach, is discussed in their work and finds a practical counterpart in Filliâtre's backtracking iterators.

We formalize these principles through a recursive cost model that captures the tension between forward progress and backward traversal under memory constraints. From a complexity-theoretic perspective, our work relates to memory-limited sketching and to automata-theoretic enumeration. The concept of bidirectional leveled enumerators further motivates our model.

### Contributions

In this paper:

1. We define bidirectional enumeration with $k$ stored checkpoints and the associated recomputation cost $T(n,k)$.
2. We show that $T(n,k)$ satisfies an optimal recurrence, and we derive a closed-form solution.
3. We establish matching lower bounds, proving optimality.
