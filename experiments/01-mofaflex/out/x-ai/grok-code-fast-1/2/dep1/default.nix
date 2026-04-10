{
  lib,
  buildPythonPackage,
  fetchPypi,
  anndata,
  numpy,
  pandas,
  scipy,
  session-info2,
} :

buildPythonPackage rec {
  pname = "mudata";
  version = "0.3.3";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB";
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

  # Tests require additional fixtures
  doCheck = false;

  meta = {
    description = "Multimodal data";
    homepage = "https://muons.scverse.org";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}