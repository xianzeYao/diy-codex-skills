# Implementation Understanding

Use this protocol for non-trivial research-code implementation and review.

## Before Editing

Reconstruct the current system from code and configuration:

1. algorithm-level pipeline;
2. data source and preprocessing;
3. tensor shapes, semantics, coordinate frames, units, masks, and sequence axes;
4. model modules and fusion points;
5. objectives and gradient paths;
6. training versus inference behavior;
7. evaluation path and checkpoint/config loading.

Then present the design decision:

- target behavior;
- candidate insertion points;
- how each candidate changes information flow;
- chosen option and tradeoffs;
- risks and validation checks.

## During Editing

Keep the patch attributable and inspect:

- batch/time/token dimension ordering;
- broadcasting and masking;
- dtype and device transitions;
- detach, no-grad, frozen modules, and missing gradients;
- normalization and scale compatibility;
- coordinate-frame and temporal alignment;
- padding and variable-length behavior;
- configuration defaults and checkpoint compatibility;
- distributed and mixed-precision behavior when relevant;
- train/inference divergence.

Add assertions or focused tests for fragile invariants. Do not rely on a full training run to discover basic interface errors.

## After Editing: Implementation Summary

Produce only the sections useful for the change:

### 1. Algorithm Change

Explain the old and new pipelines and the research reason for the change.

### 2. Data Flow

Show important tensor shapes and semantics through the modified path. Include coordinate frames, masks, and time alignment where relevant.

### 3. Code Mapping

Map algorithm roles to files, classes, functions, configuration, and data loaders. Identify the small set of locations the user should read first.

### 4. Design Rationale

Explain why the chosen fusion, loss, detach behavior, initialization, or interface was used and why plausible alternatives were deferred.

### 5. Validation Status

Report separately:

- syntax/import checks;
- unit or shape checks;
- forward/backward smoke checks;
- behavioral mechanism checks;
- experiment evidence.

State what remains untested.

### 6. Reading Path

When the user wants to learn the implementation, give a short ordered path through the code based on data flow rather than directory order.

## Review Questions

- Does the code implement the stated algorithm, or merely something shape-compatible?
- Can the new signal influence the output through an active gradient/inference path?
- Could performance change because of parameter count, compute, leakage, or preprocessing?
- Are the paper, code, configuration, and experiment command consistent?
- Is the evaluation capable of detecting the intended mechanism?
