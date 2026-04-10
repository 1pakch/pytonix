{
  lib,
  buildPythonPackage,
  fetchPypi,
  anndata,
  hatchling,
  hatch-vcs,
  numpy,
  pandas,
  scipy,
  session-info2
}:

buildPythonPackage rec {
  pname = "mudata";
  version = "0.3.3";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-CsvXw8Zo/V/R4XwuM7yf0X3xLOpepC3JuJhq0QQZWl0=";
  };

  build-system = [
    hatchling
    hatch-vcs
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
    description = "Multimodal data format for Python";
    homepage = "https://muons.scverse.org";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}
