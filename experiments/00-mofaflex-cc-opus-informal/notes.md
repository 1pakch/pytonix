The derivation here resulted from a semi-interactive attempt using Claude Code with Opus 4.5.

Note the initial instructions were suboptimal as they provided an explicit commit. In reality we maybe wwant to follow the latest release on pypi? Moreover the resulting flake does not have a devShell that would be nixc to have to test whether the package works.

The resulting code seems is ok but is lightly unidiomatic for nixpkgs becase not all package dependencies of `mofaflex` and `mudata` are declared as the arguments of the derivation. Instead they are imported from nixpkgs within the derivation. It violates the nixpkgs conventions and does not allow for overriding the input dependencies with modified versions etc.

The mofaflex derivation produced by Claude included the line `env.SETUPTOOLS_SCM_PRETEND_VERSION = version`; which is not necessary since nixpkgs already handles this automatically via a setup hook in the `setuptools-scm` package. The override within the derivation definitions of Python packages is still prevalent in nixpkgs as of 2026-04-06 (commit `8b52132`).
Background:

- `setuptools-scm` (Source Control Management) determines the package version by reading git tags from the repository's SCM history. In a Nix build sandbox the source tree has no `.git` directory, so `setuptools-scm` cannot determine the version and would fail without intervention
- setuptools-scm package in nixpkgs ships a setup hook (pkgs/development/python-modules/setuptools-scm/setup-hook.sh) that automatically sets SETUPTOOLS_SCM_PRETEND_VERSION to the derivation's version attribute at build time, solving this problem
- The hook was added in commit `4c1f249` (Dec 20, 2023, by yajo/mweinelt) and only fires if `setuptools-scm` is in build-system and `SETUPTOOLS_SCM_PRETEND_VERSION` isn't already set
- For hatch-vcs projects like mofaflex it works transitively since hatch-vcs depends on setuptools-scm
- LLMs still suggest the manual override because most training data predates the hook and hundreds of existing nixpkgs package definitions still include it
