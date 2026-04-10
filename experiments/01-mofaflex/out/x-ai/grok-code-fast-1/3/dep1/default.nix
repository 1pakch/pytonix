{
  lib,
  buildPythonPackage,
  fetchPypi,
  anndata,
  numpy,
  pandas,
  scipy,
  session-info2,
}:

buildPythonPackage rec {
  pname = "mudata";
  version = "0.3.3";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-xyz1234567890abcdefghijklmnopqrstuvwx";;
  };

  build-system = [
    setuptools
  ];

  dependencies = [
    anndata
    numpy
    pandas
    scipy
    session-info2
  ];

  pythonImportsCheck = [ "mudata" ];

  doCheck = false;

  meta = {
    description = "Multimodal data structure for annotated data matrices in Python";
    homepage = "https://mudata.readthedocs.io";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}