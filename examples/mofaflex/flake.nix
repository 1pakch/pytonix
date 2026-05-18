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

        callPkg = pkgs.lib.callPackageWith (
          pkgs.python3.pkgs // { inherit (pkgs) lib fetchFromGitHub; } // customPackages
        );

        customPackages = {
          mofaflex = callPkg ./mofaflex { };
          mudata = callPkg ./mudata { };
        };

        pythonEnv = pkgs.python3.withPackages (_: [
          customPackages.mofaflex
          customPackages.mudata
        ]);
      in
      {
        packages = customPackages // {
          default = customPackages.mofaflex;
        };

        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ];
        };
      }
    );
}
