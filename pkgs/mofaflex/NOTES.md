I'd recommend the nixpkgs-style subdirectories (mofaflex/default.nix, mudata/default.nix) because:

1. Each package can have its own additional files (patches, tests, etc.) without cluttering the root
2. Easier to copy/reference nixpkgs examples directly
3. Scales better if you add more packages later
4. callPackage ./mofaflex {} reads more naturally than callPackage ./mofaflex.nix {}

The flat file approach (mofaflex.nix, mudata.nix) is fine too if you want to keep it minimal and don't expect to add patches or extra files per package.

