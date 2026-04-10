{
  lib,
  buildPythonPackage,
  fetchPypi,
  anndata,
  array-api-compat,
  dtw-python,
  gpytorch,
  h5py,
  mizani,
  mudata,
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
}:

buildPythonPackage rec {
  pname = "mofaflex";
  version = "0.1.0.post1";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-YqJZkGRkmFGhKjKrRppYsvKtYjk7XGvzFgHhRWkY1+Q=";
  };

  build-system = [
    setuptools
  ];

  dependencies = [
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

  pythonImportsCheck = [ "mofaflex" ];

  doCheck = false;

  meta = {
    description = "Factor Analysis Models for integrating omics data with prior knowledge";
    homepage = "https://mofaflex.readthedocs.io";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}