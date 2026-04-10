{
  description = "MOFA-FLEX and mudata Python packages";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        pythonEnv = python.withPackages (ps: with ps; [
          numpy
          scipy
          pandas
          anndata
          h5py
          torch
          pyro-ppl
          gpytorch
          scikit-learn
          statsmodels
          plotnine
          mudata
          mofaflex
        ]);

        coreScope = { inherit (pkgs) lib fetchFromGitHub fetchPypi; };
        callPackageWith = pkgs.lib.callPackageWith;

        mofaflex = callPackageWith (python.pkgs // coreScope) ./main { inherit (python.pkgs) buildPythonPackage; };
        mudata = callPackageWith (python.pkgs // coreScope) ./dep1 { inherit (python.pkgs) buildPythonPackage; };

        customPackages = {
          inherit mofaflex mudata;
        };
      in {
        packages = customPackages // {
          inherit pythonEnv;
          default = pythonEnv;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
          ];
        };
      }
    );
}