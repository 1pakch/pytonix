{
  lib,
  buildPythonPackage,
  fetchPypi,
  hatchling,
  setuptools,
  wheel,
  anndata,
  numpy,
  pandas,
  scipy,
  session_info2,
  pythonOlder,
}:

buildPythonPackage rec {
  pname = "mudata";
  version = "0.3.3";
  pyproject = true;

  disabled = pythonOlder "3.10";

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
    numpy
    pandas
    scipy
    session_info2
  ];

  pythonImportsCheck = [ "mudata" ];

  doCheck = false;

  meta = {
    description = "Multimodal data";
    homepage = "https://muons.scverse.org";
    license = lib.licenses.bsd3;
    maintainers = [ ];
  };
}
