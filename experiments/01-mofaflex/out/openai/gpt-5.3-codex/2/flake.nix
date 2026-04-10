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
        pyPkgs = pkgs.python311Packages;
        coreScope = { inherit (pkgs) lib; };
        callPackageWith = pkgs.lib.callPackageWith;
        customPackages = rec {
          mudata = callPackageWith (pyPkgs // customPackages // coreScope) ./mudata {};
          main = callPackageWith (pyPkgs // customPackages // coreScope) ./main {};
          mofaflex = main;
        };
      in {
        packages = customPackages // {
          default = customPackages.main;
        };
      }
    );
}
