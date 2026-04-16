## Summary

- This folder contains the results of an experiment to produce the nix code for `mofaflex` python package and and its dependency `mudata`. The prompt was manually crafted and included pypi json for both packagess. The models used were `x-ai/grok-code-fast-1`, `qwen/qwen3-coder-next` and `openai/gpt-5.3-codex`. 

- At least one SOTA coding model (gpt-5.3-codex) tended to produce syntactically correct nix with correctly inferred intent of the templates (e.g. replacing "main" and "dep1" for the actual package names in 2 cases out of 3). Yet, still the output is problematic and shows the inability of the model to show or mimic the necessary semantic reasoning about the produced code.

- Specifically, the output of gpt-5.3-codex model experiment on one hand alters the provided template and specifies the version of the python to be used as 3.11 (rather than 3.13 which would be default in nixpkgs at the cut-off point) in all three repicates. On the other hand, however, it inserts arbitrary and inconsistent "disabled = pythonOlder ..." restrictions ("3.10" and "3.11" for each of the packages) in the package definition nix code that effectively makes it impossible to realize (build) both packages.

- Fixing these issues produces nix code that at least proceeds to checking the missing hashes of the outputs and failing. 

- I have not evaluated the outputs of the other models with the same detail. It is clear, however, that these models failed to replace the names "main" and "dep1" for actual package names when creating the outputs. 

- I also did not check the reasoning outputs provided by the model (comments).

- The experiment follows-up on initial attempt on the same task with semi-formal approach using Claude Code and then the initial OpenRouter-based experiments where the (multi-file) output was not well structured in the LLMs outputs (which also included `gemma-3-4b-it:free` as a model but it was clearly too weak and could not even get the nix syntax right).

## Output of gpt-5.3.codex

Was using `lib.fakeSha265` instead of `lib.fakeHash`

In two cases out of three gpt-5.3.codex insisted on using python3.11.

In `out/openai/gpt-5.3-codex/1/flake.nix` we have

```
          python = pkgs.python311;
          # ...
          pythonPackageScope = python.pkgs // customPackages // coreScope
          # ...
          mudata = callPackageWith pythonPackageScope ./mudata { };
          mofaflex = callPackageWith pythonPackageScope ./mofaflex { };

```

In `out/openai/gpt-5.3-codex/2/flake.nix` we have

```
          pyPkgs = pkgs.python311Packages;
          # ...
          mudata = callPackageWith (pyPkgs // customPackages // coreScope) ./mudata {};
          main = callPackageWith (pyPkgs // customPackages // coreScope) ./main {};
```

In `out/openai/gpt-5.3-codex/3/flake.nix` again

```
        pyPkgs = pkgs.python311Packages;
        # ...
            pythonPackageScope =
              pyPkgs
              // coreScope
              # ...
```
