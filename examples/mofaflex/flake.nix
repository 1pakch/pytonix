{
  description = "mofaflex - Factor Analysis Models";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        coreScope = { inherit (pkgs) lib fetchFromGitHub; };
        customPackages =
          let
            pythonPackageScope = pkgs.python3.pkgs // customPackages // coreScope;
            callPackageWith = pkgs.lib.callPackageWith;
          in
          {
            mofaflex = callPackageWith pythonPackageScope ./mofaflex { };
            mudata = callPackageWith pythonPackageScope ./mudata { };
          };
      in
      {
        packages = customPackages // {
          default = customPackages.mofaflex;
        };
      }
    );
}
