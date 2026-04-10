{ lib
, buildPythonPackage
, fetchPypi
, anndata
, numpy
, pandas
, scipy
, session-info2
}:

buildPythonPackage rec {
  pname = "mudata";
  version = "0.3.3";
  format = "pyproject";
  pyproject = true;

  src = fetchPypi {
    pname = "mudata";
    inherit version;
    hash = "sha256-8J8QJ8QJ8QJ8QJ8QJ8QJ8QJ8QJ8QJ8QJ8QJ8QJ8QJ8Q=";
  };

  nativeBuildInputs = [
    setuptools
    wheel
  ];

  propagatedBuildInputs = [
    anndata
    numpy
    pandas
    scipy
    session-info2
  ];

  pythonImportsCheck = [ "mudata" ];

  doCheck = false;

  meta = with lib; {
    description = "Multimodal data";
    longDescription = ''
      MuData provides functionality to load, process, and store multimodal omics data.
      It is designed to represent multimodal annotated datasets in Python.
    '';
    homepage = "https://muons.scverse.org";
    license = licenses.bsd3;
    maintainers = with maintainers; [ ];
    pythonImportsCheck = [ "mudata" ];
  };
}