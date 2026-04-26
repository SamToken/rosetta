{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.tree-sitter
    pkgs.gcc
    pkgs.pkg-config
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.tree-sitter
      python-pkgs.pip
      python-pkgs.setuptools
      python-pkgs.wheel
    ]))
  ];
}
