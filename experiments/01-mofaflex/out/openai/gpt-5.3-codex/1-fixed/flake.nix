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
        coreScope = { inherit (pkgs) lib fetchPypi; };
        customPackages = let
          callPackageWith = pkgs.lib.callPackageWith;
          pythonPackageScope = python.pkgs // customPackages // coreScope;
        in rec {
          mudata = callPackageWith pythonPackageScope ./mudata { };
          mofaflex = callPackageWith pythonPackageScope ./mofaflex { };
          main = mofaflex;
        };
      in {
        packages = customPackages // {
          default = customPackages.mofaflex;
        };
      }
    );
}
