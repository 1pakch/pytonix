{
  lib,
  buildPythonPackage,
  fetchPypi,
  hatchling,
  pythonOlder,
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

  disabled = pythonOlder "3.10";

  src = fetchPypi {
    inherit pname version;
    hash = lib.fakeSha256;
  };

  build-system = [
    hatchling
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

  meta = with lib; {
    description = "Multimodal data";
    homepage = "https://muons.scverse.org";
    license = licenses.bsd3;
    maintainers = [ ];
  };
}
