# Knowledge Bridge

Use just-in-time teaching to unblock a live research decision. Do not turn the task into a survey course.

## Bridge Structure

Cover only the useful parts:

1. **Decision**: name the decision the user cannot yet evaluate.
2. **Missing concept**: define the smallest prerequisite in plain language.
3. **Mechanism**: show the causal or mathematical mechanism.
4. **Concrete mapping**: connect it to the current model, tensor, code, data, or experiment.
5. **Contrast**: compare the nearest plausible alternative when it clarifies the choice.
6. **Check**: ask for or demonstrate a small prediction, explanation, or application.

Prefer one worked local example over broad history or a list of papers.

## Explanation Ladder

Start at the lowest sufficient level and climb only when needed:

1. Intuition: what changes and why it matters.
2. Interface: inputs, outputs, shapes, and invariants.
3. Mechanism: equations, information flow, gradients, or probability.
4. Implementation: modules, functions, and failure modes.
5. Research consequence: hypotheses, controls, and claims enabled by the concept.

## Verify Learning

Do not mark an unknown as known merely because an explanation was delivered. Seek evidence that the user or joint workflow can now:

- predict what changes under an intervention;
- choose between two implementations and give a reason;
- trace the concept through the current code;
- identify a failure mode;
- design a control that tests whether the mechanism is used.

If verification fails, locate the missing rung and rebuild only that part of the bridge.

## Avoid

- encyclopedic background unrelated to the current decision;
- unexplained jargon replacing an explanation;
- analogies that do not map back to equations or code;
- presenting one implementation pattern as the only theoretical option;
- quizzes that interrupt urgent implementation without improving the decision.
