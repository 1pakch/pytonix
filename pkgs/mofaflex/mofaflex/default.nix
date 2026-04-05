{
  lib,
  python3Packages,
  fetchFromGitHub,
  mudata,
}:

python3Packages.buildPythonPackage rec {
  pname = "mofaflex";
  version = "0-unstable-2025-03-26";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "bioFAM";
    repo = "mofaflex";
    rev = "ebeb258c05764fe3b732f22e028d60005b01871b";
    hash = lib.fakeHash;
  };

  build-system = with python3Packages; [
    hatchling
    hatch-vcs
  ];

  dependencies = with python3Packages; [
    anndata
    array-api-compat
    dtw-python
    gpytorch
    h5py
    mizani
    mudata
    numpy
    packaging
    pandas
    platformdirs
    plotnine
    pyro-ppl
    scikit-learn
    scipy
    session-info2
    statsmodels
    torch
    tqdm
  ];

  optional-dependencies = with python3Packages; {
    lazy = [ dask ];
  };

  pythonImportsCheck = [ "mofaflex" ];

  # Tests require additional data and network access
  doCheck = false;

  meta = {
    description = "Factor Analysis Models";
    homepage = "https://github.com/bioFAM/mofaflex";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}
