{
  description = "mofaflex - Factor Analysis Models";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        
        python = pkgs.python3;
        pythonPackages = python.pkgs;

        # Helper to call package with correct scope
        callPackageWith = pkgs.lib.callPackageWith (pythonPackages // customPackages);

        customPackages = {
          mudata = callPackage ./dep1 {
            pname = "mudata";
            version = "0.3.3";
          };
          
          mofaflex = callPackage ./main {
            pname = "mofaflex";
            version = "0.1.0.post1";
          };
        };
      in {
        packages = customPackages // { inherit (pythonPackages) anndata numpy pandas scipy h5py; };
        default = customPackages.mofaflex;
        formatter = pkgs.alejandra;
      }
    );
}