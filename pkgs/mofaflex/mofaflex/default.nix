{
  lib,
  python3Packages,
  fetchFromGitHub,
  mudata,
}:

python3Packages.buildPythonPackage rec {
  pname = "mofaflex";
  version = "0.1.0.post1-unstable-2025-03-26";
  pyproject = true;

  # hatch-vcs needs git tags to determine version, but fetchFromGitHub has no .git
  # Use latest PyPI version: https://pypi.org/project/mofaflex/
  env.SETUPTOOLS_SCM_PRETEND_VERSION = "0.1.0.post1";

  src = fetchFromGitHub {
    owner = "bioFAM";
    repo = "mofaflex";
    rev = "ebeb258c05764fe3b732f22e028d60005b01871b";
    hash = "sha256-F3DD+nyB8ICGBCg7n9fI9ISaDlb5UYKYgMLHTDrMmLk=";
  };

  build-system = with python3Packages; [
    hatchling
    hatch-vcs
  ];

  dependencies = [
    mudata
  ] ++ (with python3Packages; [
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
  ]);

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
