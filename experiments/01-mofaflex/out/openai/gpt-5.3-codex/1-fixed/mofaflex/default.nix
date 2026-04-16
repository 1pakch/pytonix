{
  lib,
  buildPythonPackage,
  fetchPypi,
  hatchling,
  pythonOlder,
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
    hash = lib.fakeHash;
  };

  build-system = [
    hatchling
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

  meta = with lib; {
    description = "Factor Analysis Models";
    homepage = "https://github.com/bioFAM/mofaflex";
    license = licenses.bsd3;
    maintainers = [ ];
  };
}
