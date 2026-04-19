{
  description = "pytonix (ptx) - Experimental tool to wrap Python packages for Nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

	# dependencies of the tooling
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          httpx
          click
          msgspec
          platformdirs  # multi-platform analogues for XDG_USER_CACHE etc
          packaging     # PEP-508 parsing and evalution
          ijson         # streaming json parser
          pytest
        ]);

        # ptx cli tool wrapper script
        ptx = pkgs.writeShellScript "ptx" ''
          export PYTHONPATH="${self}"
          exec ${pythonEnv}/bin/python -m pytonix "$@"
        '';
      in {
        apps.default = {
          type = "app";
          program = "${ptx}";
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
	    pythonEnv
            pkgs.ruff
            pkgs.nixfmt
          ];
          # Set PYTHONPATH so pytest and other tools can import pytonix module
          # NOTE: ${self} points to a git snapshot in /nix/store, so you need to
          # exit and re-run `nix develop` after staging new files with `git add`
          # for them to be visible to pytest and other tools (or use direnv).
          shellHook = ''
            export PYTHONPATH="${self}"
          '';
        };
      }
    );
}
