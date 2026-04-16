# PYTONIX

## Why

Nix packaging offers compelling advantages for scientific computing: language-agnostic builds, near-perfect reproducibility, and nixpkgs standing as the largest package repository of any Linux distribution by package count. These properties are highly relevant to research, where reproducibility, transparency, and ease of sharing matter at every stage — from exploratory analysis to publication. Nix makes it remarkably straightforward to share complete, reproducible analysis environments and scripts. Yet this potential remains largely untapped, due to UX friction, historical inertia, and critically, the unavailability of frontier packages.

## What

PYTONIX explores the potential of AI agents to remove one of these barriers: converting native scientific software packages into working Nix derivations. We focus initially on frontier bioinformatics and computational biology software, a domain characterized by a steady stream of applied research and a constant flow of new packages — many available only on PyPI. Conda, Bioconda, and R ecosystems are natural follow-up targets.

## Review 2026-04-16 (Apr 16)

### Priorities/Roadmap

After discussing the status (below) with Claude I have identified the following priorities

- Automating the test harness (e.g. to test nix build . and maybe the import) #todo
- Trying nix eval for "diffing" vs the ground truth # todo
- Automating the prompting as well. start point: internal pypi cache # todo
- Design prompting code to support both one- and multi-shot (each file/package separately) # todo
- Identify candidate packages for the test set (review my jupyter flakes repo, Theis lab) #todo
- Think about having structure (patches) for imperfect solutions that I can fix manually #todo

Upon further thinking I decided to first model the domain e.g. design/implement
- the PythonEnvironmentRequest (or PythonPackagingRequest) structure including
  - the requested "target" packages from a specific source (limited to pypi as of now)
  - the specific revision of nixpgs to build against
- the output of an attempt to such request (including, possibly, the ground truth ones)
  which might include multiple files (and additional comments) some of which are assumed
  to be mandatory e.g. `main/default.nix`, `depX/default.nix` and the outer `flake.nix`.
- the interface for an "agent" attempting at the above request (probably caching the
  llm requests/responses and pypi requests - but this is the implementation detail).
- the evaluation/testing interface probably limited to the building attempt as of now
  (but keeping softer scoring/judging possibilities in mind, e.g. syntax correctness,
  the correct specificaiton of dependencies)

### Status

- I have created minimal tooling to use llms on openrouter and parse their output (which is supposed to be multiple output files and reasoning comments packed in a json object).

- I have produced ground-truth nix structure for a couple of pypi packages called mofa-flex and its dependency mudata which are relevant to some research projects I am working on and are not in nixpkgs. This effects to a nix flake and two nix files one for package which are used via callPackageWith in the flake

- I ran experiments with 3 models where I have asked LLMs three times (3) to produce the same flake/packages structure for these packages using template I provided and (unfliltered) data from pypi json files. Strictly one-shot with a manulally-crafted prompt.

- I resorted to manual evaluation and at least one model (openai/gpt-5.3-codex) got reasonably close to a solution but still hallucinated quite a bit (see `experiments/01-mofaflex/NOTES.md`). The fixes to a buildable solution did not seem unsurmountable.

The plans I have devised at this point:

- Tighter harness and automated experiments.
    1. Write code that would enable and/or make it easier to test and/or evaluate the outputs of the model. This includes, for instance, creating a temp directory bringing in the (controlled, external) flake.lock and trying to build the required nix derivations (and then probably to run import the main package in python from the resulting environment).
    2. Similarly, restructure and automate the input prompt creation from package metadata (which was manually created before).
    3. One could also try to add additional scoring non-functional checks on the output e.g. judging whether all the dependencies present in the pypi description were specified in the nix derivation. More generally, one could imagine using an LLM to meaningfully diff the solution to the ground truth using a fixed scorecard and a field for arbitrary comments.

- Simplifying the task itself by breaking it into smaller subtasks that can be solved by llm or by other tools. For instance, the flake.nix file could be produced with or without LLMs once one infers the for a specific target package (mofaflex)  what are its required depoendencies not present in the nixpkgs already (mudata). The task then could be simplified to producing a derivation for each package assuming all other dependencies are available.

- Increasing the test set. Identifying one or more target packages to be used in experimentation and producing the ground truth nix code for them.

- Finally, one could spend more time analyzing the output of the already performed expermine

I was a bit hesitant how to prioritize between this steps. Almost all needs to be done and automating the both the prompting and automating the evaluation of the results are clear priorities, however the design of the prompting might depend on how we break the test (and one can imagine different prompting strategies that need to be potentially supported). I think, however, there is a bit of risk on working on design and infrastructure before having more experience with specific packages (meaning designing early might trigger "expensive" redesigns and code changes).

## Initial experiment on 2026-04-05

Tried Claude Code for wrapping the mofaflex interactively. See `experiments/00-mofaflex-cc-opus-informal`. Extremely pissed that non-interactive mode requires buying API tokens separately from CC subscription.
