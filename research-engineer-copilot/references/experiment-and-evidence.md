# Experiment and Evidence

## Convert Intuition to a Hypothesis

Express the hypothesis with:

- **intervention**: what changes;
- **mechanism**: why it should matter;
- **observable**: what should change and in which direction;
- **scope**: where the prediction is expected to hold;
- **falsifier**: what outcome would weaken or reject it.

Example form:

```text
If [intervention] exposes [information/mechanism] to [component], then
[observable] should change relative to [control], especially under [scope],
because [mechanism]. The hypothesis is weakened if [falsifier].
```

## Design the Smallest Discriminating Experiment

Specify:

1. research question;
2. compared conditions;
3. fixed factors;
4. data and evaluation protocol;
5. primary metric and uncertainty reporting;
6. expected outcomes under competing explanations;
7. failure criteria;
8. implementation sanity checks.

Prefer controls that distinguish "the model received the signal" from "the model used the signal." Depending on the mechanism, consider:

- remove the condition;
- shuffle it across samples;
- supply a plausible but wrong condition;
- mask it at train or inference time;
- match parameter count or compute;
- compare against a simpler fusion route;
- test sensitivity to controlled perturbations;
- evaluate the regime where the signal should matter most.

Do not add every possible ablation. Select controls by the alternative explanation they eliminate.

## Build a Claim-Evidence Matrix

For each candidate claim, record:

| Claim | Required evidence | Current evidence | Alternative explanations | Status |
|---|---|---|---|---|

Use status values such as `unsupported`, `suggestive`, `supported within scope`, or `contradicted`. Avoid `proven` for empirical ML results.

## Interpret Results

Separate:

- observation: measured result;
- interpretation: proposed explanation;
- assumption: required but unchecked premise;
- limitation: boundary of the evidence;
- follow-up: cheapest test separating remaining explanations.

Check variance, seeds, selection effects, data leakage, metric validity, baseline fairness, compute differences, and train/evaluation mismatch before strengthening a claim.

Negative or null results should update the hypothesis space. Identify whether they challenge the mechanism, implementation, optimization, statistical power, or evaluation sensitivity.
