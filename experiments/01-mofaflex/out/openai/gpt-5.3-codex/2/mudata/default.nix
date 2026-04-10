{
  lib,
  buildPythonPackage,
  fetchPypi,
  hatchling,
  setuptools,
  wheel,
  setuptools-scm,
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
    hash = lib.fakeHash;
  };

  build-system = [
    hatchling
    setuptools
    wheel
    setuptools-scm
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
    description = "Multimodal data";
    homepage = "https://muons.scverse.org";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}
