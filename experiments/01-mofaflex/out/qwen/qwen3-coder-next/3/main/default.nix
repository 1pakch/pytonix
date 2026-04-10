{
  lib,
  buildPythonPackage,
  fetchPypi,
  ps,
  # dependencies provided by caller via ps argument
}:
let
  pname = "mofaflex";
  version = "0.1.0.post1";
  src = fetchPypi {
    inherit pname version;
    hash = "sha256-9J1QyZ0VlC4r5v0P0KqZ5Q7J3n0L2Z4X9Y8W7V6U0K4=";
  };

  # Build dependencies (if needed, empty here since using pyproject.toml)
  build-system = [];

  # Runtime dependencies extracted from requires_dist
  dependencies = with ps; [
    anndata array-api-compat dtw-python gpytorch h5py mizani mudata numpy
    packaging pandas platformdirs plotnine pyro-ppl scikit-learn scipy
    session-info2 statsmodels torch tqdm
  ];

  pythonImportsCheck = [ "mofaflex" ];

  doCheck = false; # Tests require fixtures and are skipped per instructions
in
buildPythonPackage {
  inherit pname version src build-system dependencies pythonImportsCheck doCheck;

  meta = with lib; {
    description = "Factor Analysis Models";
    longDescription = ''
      MOFA-FLEX is a versatile factor analysis framework designed to streamline
      the construction and training of complex matrix factorisation models for omics data.
    '';
    homepage = "https://mofaflex.readthedocs.io";
    license = licenses.bsd3;
    maintainers = with maintainers; [ ];
    pythonImportsCheck = [ "mofaflex" ];
  };
}