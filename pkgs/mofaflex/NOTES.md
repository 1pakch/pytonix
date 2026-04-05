I'd recommend the nixpkgs-style subdirectories (mofaflex/default.nix, mudata/default.nix) because:

1. Each package can have its own additional files (patches, tests, etc.) without cluttering the root
2. Easier to copy/reference nixpkgs examples directly
3. Scales better if you add more packages later
4. callPackage ./mofaflex {} reads more naturally than callPackage ./mofaflex.nix {}

The flat file approach (mofaflex.nix, mudata.nix) is fine too if you want to keep it minimal and don't expect to add patches or extra files per package.

---

## SETUPTOOLS_SCM_PRETEND_VERSION

When a package uses `hatch-vcs` or `setuptools-scm`, it reads version from git tags. But `fetchFromGitHub` has no `.git` directory.

Fix:
```nix
env.SETUPTOOLS_SCM_PRETEND_VERSION = "0.1.0.post1";
```

**Where to get the version:** Check PyPI (https://pypi.org/project/PACKAGE/) for the latest release version.

**Why two versions?**
- Nix version: `0.1.0.post1-unstable-2025-03-26` - includes date suffix (nixpkgs convention)
- Python version: `0.1.0.post1` - strictly PEP 440 compliant (what `pip show` reports)

---

## Hashes

Can I get the hash before building?
