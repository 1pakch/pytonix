# pytonix

## Why and What

[Nix](https://nixos.org) packaging offers compelling advantages for scientific computing: language-agnostic builds, near-perfect reproducibility, and nixpkgs standing as the largest package repository of any Linux distribution by package count. These properties are highly relevant to research, where reproducibility, transparency, and ease of sharing matter at every stage — from exploratory analysis to publication. Nix makes it remarkably straightforward to share complete, reproducible analysis environments and scripts. Yet this potential remains largely untapped, due to UX friction, historical inertia, and critically, the unavailability of frontier packages.

Here I explore the potential of llm-based agents to remove one of these barriers: converting native scientific software packages into working Nix derivations. We focus initially on frontier bioinformatics and computational biology software implemeted in Python, a domain familiar to the author and characterized by a steady stream of new packages - many available only on PyPI. Conda, Bioconda, and R ecosystems are natural follow-up targets.

Examples of packages: squidpy, scvelo, ehrapy, scvi, moscot -> ott (ott-jax) -> diffrax, cellchat (R) and the crown jewel: anvio[^1]. TODO: add links.

## Where it's at?

I have run some initial one-shot experiments using Claude Code Opus 4.6 ([write-up](experiments/00-mofaflex-cc-opus-informal/NOTES.md)) and then with three standalone models (`x-ai/grok-code-fast-1`, `qwen/qwen3-coder-next` and `openai/gpt-5.3-codex` via [OpenRouter](http://openrouter.ai) ([write-up](experiments/01-mofaflex/NOTES.md)) . The experiments clearly showed that the models do not perform well even in the simples and while the prompting can probably improved the performance I decided to focus on the underlying tooling that can be used independently or by the agents via the tools-usage approach commonplace by now.

As of now I have integrated PyPI metadata retrieval as well as rudimentary index of Python packages in nixpkgs (via `/pkgs/top-level/packages-info.nix`. This allows checking recursively the dependencies of pypi packages and matching them to the nixpkgs ones where possible (the matching logic is really primitive and PoC at the moment):

```bash
$ ./ptx pypi nixify moscot -p 3.13
moscot (pypi)
  numpy (nixpkgs)
  scipy (nixpkgs)
  pandas (nixpkgs)
  networkx (nixpkgs)
  matplotlib (nixpkgs)
  anndata (nixpkgs)
  scanpy (nixpkgs)
  wrapt (nixpkgs)
  docrep (nixpkgs)
  jax (nixpkgs)
  ott-jax (pypi)
    jax (nixpkgs, seen)
    jaxopt (nixpkgs)
    lineax (nixpkgs)
    numpy (nixpkgs, seen)
    optax (nixpkgs)
  cloudpickle (nixpkgs)
  rich (nixpkgs)
  docstring_inheritance (pypi)
    typing-extensions (nixpkgs)
  mudata (pypi)
    anndata (nixpkgs, seen)
    h5py (nixpkgs)
    numpy (nixpkgs, seen)
    pandas (nixpkgs, seen)
    scipy (nixpkgs, seen)
    scverse-misc (pypi)
      session-info2 (nixpkgs)
    session-info2 (nixpkgs, seen)
  optax (nixpkgs, seen)
  flax (nixpkgs)
  diffrax (pypi)
    equinox (nixpkgs)
    jax (nixpkgs, seen)
    jaxtyping (nixpkgs)
    lineax (nixpkgs, seen)
    optimistix (nixpkgs)
    typing-extensions (nixpkgs, seen)
    wadler-lindig (nixpkgs)
  ott-jax (pypi, seen)
```

or

```bash
$ ./ptx pypi nixify moscot -p 3.13 | grep -v nixpkgs
moscot (pypi)
  ott-jax (pypi)
  docstring_inheritance (pypi)
  mudata (pypi)
    scverse-misc (pypi)
  diffrax (pypi)
  ott-jax (pypi, seen)
```

Interestingly, Domain Driven Design seems to work quite well for this code base so far. The domain classes sit in the same-named folder while the infra modules implement the interation with the outside world. The resolving logic is currently with cli code but clearly it needs a better place and the code base needs some work in general


## References

[^1]: https://anvio.org/install/linux/dev/#2-set-up-the-conda-environment
