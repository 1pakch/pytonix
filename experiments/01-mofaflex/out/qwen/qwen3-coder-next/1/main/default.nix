{
  lib,
  buildPythonPackage,
  fetchPypi,
  numpy,
  scipy,
  pandas,
  anndata,
  h5py,
  torch,
  pyro-ppl,
  gpytorch,
  scikit-learn,
  statsmodels,
  plotnine,
  tqdm,
  session-info2,
  array-api-compat,
  dtw-python,
  packaging,
  platformdirs,
  mizani,
  mudata,
}:

buildPythonPackage rec {
  pname = "mofaflex";
  version = "0.1.0.post1";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-0h6q9h7z0x2e4a8f0b1c3d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t=";
  };

  build-system = [
    pyro-ppl
    torch
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
    description = "MOFA-FLEX: A Factor Model Framework for Integrating Omics Data with Prior Knowledge";
    longDescription = "MOFA-FLEX is a versatile factor analysis framework designed to streamline the construction and training of complex matrix factorisation models for omics data.";
    homepage = "https://mofaflex.readthedocs.io";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}