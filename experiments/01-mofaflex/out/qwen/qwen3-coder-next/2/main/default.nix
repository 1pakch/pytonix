{ lib
, buildPythonPackage
, fetchFromGitHub
, anndata
, array-api-compat
, dtw-python
, gpytorch
, h5py
, mizani
, mudata
, numpy
, packaging
, pandas
, platformdirs
, plotnine
, pyro-ppl
, scikit-learn
, scipy
, session-info2
, statsmodels
, torch
, tqdm
, pytest
}:

buildPythonPackage rec {
  pname = "mofaflex";
  version = "0.1.0.post1";
  format = "pyproject";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "bioFAM";
    repo = "mofaflex";
    rev = "v${version}";
    sha256 = "sha256-0YQz1VzHvWz0tF2QzQzQzQzQzQzQzQzQzQzQzQzQzQ0=";
  };

  nativeBuildInputs = [
    pyproject-build
  ];

  propagatedBuildInputs = [
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

  nativeCheckInputs = [
    pytest
  ];

  pythonImportsCheck = [ "mofaflex" ];

  # Tests require additional fixtures and computational resources
  doCheck = false;

  meta = with lib; {
    description = "Factor Analysis Models";
    longDescription = ''
      MOFA-FLEX is a versatile factor analysis framework designed to streamline
      the construction and training of complex matrix factorisation models for omics data.
      It is built on a probabilistic programming-based Bayesian factor analysis framework
      that integrates concepts from multiple existing methods while remaining modular
      and extensible.
    '';
    homepage = "https://github.com/bioFAM/mofaflex";
    license = licenses.bsd3;
    maintainers = with maintainers; [ ];
    pythonImportsCheck = [ "mofaflex" ];
  };
}