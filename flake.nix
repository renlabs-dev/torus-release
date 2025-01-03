{
  description = "Alternative library/SDK to the original Commune AI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          system = system;
          config.allowUnfree = true;
        };
        python = pkgs.python310;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.poetry
            pkgs.ruff
          ];
        };
      });
}
