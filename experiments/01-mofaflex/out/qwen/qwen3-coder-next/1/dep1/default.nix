{
  lib,
  buildPythonPackage,
  fetchPypi,
  numpy,
  pandas,
  scipy,
  anndata,
  session-info2,
}:

buildPythonPackage rec {
  pname = "mudata";
  version = "0.3.3";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z=";
  };

  build-system = [ ];

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
    description = "Multimodal data analysis for single-cell omics";
    longDescription = "MuData provides a multimodal data container for integration of multiple single-cell omics modalities.";
    homepage = "https://muons.scverse.org";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ ];
  };
}