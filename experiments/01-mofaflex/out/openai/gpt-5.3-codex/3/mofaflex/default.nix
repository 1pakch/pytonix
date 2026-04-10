{
  lib,
  buildPythonPackage,
  fetchPypi,
  hatchling,
  setuptools,
  wheel,
  anndata,
  array_api_compat,
  dtw_python,
  gpytorch,
  h5py,
  mizani,
  mudata,
  numpy,
  packaging,
  pandas,
  platformdirs,
  plotnine,
  pyro_ppl,
  scikit_learn,
  scipy,
  session_info2,
  statsmodels,
  torch,
  tqdm,
  pythonOlder,
}:

buildPythonPackage rec {
  pname = "mofaflex";
  version = "0.1.0.post1";
  pyproject = true;

  disabled = pythonOlder "3.11";

  src = fetchPypi {
    inherit pname version;
    hash = lib.fakeHash;
  };

  build-system = [
    hatchling
    setuptools
    wheel
  ];

  dependencies = [
    anndata
    array_api_compat
    dtw_python
    gpytorch
    h5py
    mizani
    mudata
    numpy
    packaging
    pandas
    platformdirs
    plotnine
    pyro_ppl
    scikit_learn
    scipy
    session_info2
    statsmodels
    torch
    tqdm
  ];

  pythonImportsCheck = [ "mofaflex" ];

  doCheck = false;

  meta = {
    description = "Factor Analysis Models";
    homepage = "https://github.com/bioFAM/mofaflex";
    license = lib.licenses.bsd3;
    maintainers = [ ];
  };
}
