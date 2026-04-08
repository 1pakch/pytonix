{
  lib,
  buildPythonPackage,
  fetchFromGitHub,
  mudata,
  hatchling,
  hatch-vcs,
  anndata,
  array-api-compat,
  dtw-python,
  gpytorch,
  h5py,
  mizani,
  numpy,
  packaging,
  pandas,
  platformdirs,
  plotnine,
  pyro-ppl,
  scikit-learn,
  scipy,
  session-info2,
  statsmodels,
  torch,
  tqdm,
  dask
}:

buildPythonPackage rec {
  pname = "mofaflex";
  version = "0.1.0.post1";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "bioFAM";
    repo = "mofaflex";
    tag = "v0.1.0post1";
    hash = "sha256-OsS5UbTI41a4905WF/79eezFhrZGHX8L2zldQ0gRRHY=";
  };

  build-system = [
    hatchling
    hatch-vcs
  ];

  dependencies = [
    mudata
    anndata
    array-api-compat
    dtw-python
    gpytorch
    h5py
    mizani
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

  optional-dependencies = {
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
