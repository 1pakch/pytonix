# PYTONIX

## Why

Nix packaging offers compelling advantages for scientific computing: language-agnostic builds, near-perfect reproducibility, and nixpkgs standing as the largest package repository of any Linux distribution by package count. These properties are highly relevant to research, where reproducibility, transparency, and ease of sharing matter at every stage — from exploratory analysis to publication. Nix makes it remarkably straightforward to share complete, reproducible analysis environments and scripts. Yet this potential remains largely untapped, due to UX friction, historical inertia, and critically, the unavailability of frontier packages.

## What

PYTONIX explores the potential of AI agents to remove one of these barriers: converting native scientific software packages into working Nix derivations. We focus initially on frontier bioinformatics and computational biology software implemeted in Python, a domain characterized by a steady stream of applied research and a constant flow of new packages — many available only on PyPI. Conda, Bioconda, and R ecosystems are natural follow-up targets.
