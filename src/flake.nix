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
          shellHook = ''
            export PYTHONPATH="${self}"
          '';
        };
      }
    );
}
