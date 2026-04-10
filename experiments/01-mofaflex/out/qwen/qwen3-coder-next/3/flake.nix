{
  description = "mofaflex - Factor Analysis Models";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        pythonWithPackages = python.withPackages (ps: [
          ps.numpy ps.scipy ps.pandas ps.anndata ps.session-info2
          ps.torch ps.pyro-ppl ps.scikit-learn ps.statsmodels
          ps.h5py ps.plotnine ps.mizani ps.dtw-python ps.tqdm
          ps.platformdirs ps.packaging ps.gpytorch ps.array-api-compat
          ps.mudata
        ]);
        customPackages = {
          mofaflex = ps: (import ./main { inherit ps; }).mofaflex;
          mudata = ps: (import ./dep1 { inherit ps; }).mudata;
        };
        finalPackages = let
          ps = python.pkgs;
          allDeps = ps: with ps; [
            numpy scipy pandas anndata session-info2 torch pyro-ppl
            scikit-learn statsmodels h5py plotnine mizani dtw-python tqdm
            platformdirs packaging gpytorch array-api-compat mudata
          ];
        in {
          mofaflex = pythonWithPackages (ps: allDeps ps);
          mudata = pythonWithPackages (ps: allDeps ps);
        };
      in {
        packages = {
          inherit (finalPackages) mofaflex mudata;
          default = finalPackages.mofaflex;
        };
        devShells.default = pkgs.mkShell {
          name = "mofaflex-dev";
          buildInputs = with pkgs; [
            python
            python.pkgs.pip
            python.pkgs.setuptools
            python.pkgs.wheel
          ];
        };
      }
    );
}