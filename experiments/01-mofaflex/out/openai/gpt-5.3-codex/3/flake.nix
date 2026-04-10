{
  description = "mofaflex - Factor Analysis Models";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pyPkgs = pkgs.python311Packages;
        coreScope = { inherit (pkgs) lib fetchPypi; };

        customPackages =
          let
            callPackageWith = pkgs.lib.callPackageWith;
            pythonPackageScope =
              pyPkgs
              // coreScope
              // {
                array_api_compat = pyPkgs."array-api-compat";
                dtw_python = pyPkgs."dtw-python";
                pyro_ppl = pyPkgs."pyro-ppl";
                scikit_learn = pyPkgs."scikit-learn";
                session_info2 = pyPkgs."session-info2";
              }
              // customPackages;
          in
          {
            mudata = callPackageWith pythonPackageScope ./mudata { };
            mofaflex = callPackageWith pythonPackageScope ./mofaflex { };
          };
      in
      {
        packages = customPackages // {
          default = customPackages.mofaflex;
        };
      }
    );
}
