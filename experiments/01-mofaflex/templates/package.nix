{
  lib,
  buildPythonPackage,
  fetchFromGitHub, # or fetchPypi
  requests, # example dependency
  # ...other dependencies
}:

buildPythonPackage rec {
  pname = "name of package";
  version = "version";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-[hash]";
  };

  build-system = [
    # add build time dependencies
  ];

  dependencies = [
    requests
  ];

  pythonImportsCheck = [ "" ];

  # Tests require additional fixtures
  doCheck = false;

  meta = {
    description = "...";
    homepage = "...";
    license = lib.licenses.bsd3; # for instance
    maintainers = with lib.maintainers; [ ];
  };
}
