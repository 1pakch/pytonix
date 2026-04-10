{
  lib,
  buildPythonPackage,
  fetchPypi,
  ps,
  # dependencies provided by caller via ps argument
}:
let
  pname = "mudata";
  version = "0.3.3";
  src = fetchPypi {
    inherit pname version;
    hash = "sha256-A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0=";
  };

  build-system = [];

  dependencies = with ps; [
    anndata numpy pandas scipy session-info2
  ];

  pythonImportsCheck = [ "mudata" ];

  doCheck = false;
in
buildPythonPackage {
  inherit pname version src build-system dependencies pythonImportsCheck doCheck;

  meta = with lib; {
    description = "Multimodal data";
    longDescription = ''
      MuData is designed to provide functionality to load, process, and store multimodal omics data.
    '';
    homepage = "https://muons.scverse.org";
    license = licenses.bsd3;
    maintainers = with maintainers; [ ];
    pythonImportsCheck = [ "mudata" ];
  };
}