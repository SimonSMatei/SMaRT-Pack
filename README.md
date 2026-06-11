# SMaRT_Pack

SMaRT_Pack is a deterministic data engineering pipeline for materials science, specifically built to analyze High-Entropy Carbides, but the goal is for it to be adapted for any material system.

SMaRT_Pack is designed to programmatically fetch, deduplicate, and merge conflicting structural data from multi-source databases (e.g., AFLOW and ICSD). It prepares mathematically pure, physically consistent data schemas optimized for downstream Machine Learning models.


## Core Philosophy
When merging large materials science datasets, identical compounds often feature slightly different calculated parameters depending on the source database. SMaRT_Pack resolves this through an Intelligent Variance Engine:

- **Consensus Compression**: Parameters with a variance below a strict threshold (e.g., lattice parameters) are compressed using a standard mean.

- **Divergence Splitting**: Unstable parameters that exceed the variance threshold (e.g., magnetic spin calculations) are safely isolated into distinct source-specific features, preventing data corruption.

- **NaN Propagation Handling**: Employs an "Innocent Until Proven Guilty" logic, seamlessly bridging gaps where one database contains data and the other contains nulls, without artificially splitting the parameters.


## Architecture & Modules

The package is strictly decoupled into orchestration scripts and core processing logic:

- **DataProcessing.loaders**: Utilities for handling remote data ingestion (e.g., automated AFLOW REST API requests).

- **DataProcessing.stats**: The mathematical core containing the variance thresholding logic and Pandas aggregation strategies.

- **DataProcessing.elements**: Integration with pymatgen to dynamically generate fundamental elemental features (electronegativity, atomic radii) based on project-specific chemistries.

- **DevModelPrac.GradBoostReg**: A model prototyping class for evaluating the processed schemas.

## Installation

SMaRT_Pack uses pyproject.toml for dependency management. Ensure your virtual environment is active, then install the package locally:

```bash
pip install -e .
```

## 📂 Repository Structure

```text
SMaRT_Pack/
├── DataBases/                # Raw inputs, processed schemas, and variance logs
├── DataPipelines/            # Orchestration scripts (combine, load, process)
├── Scripts/                  # ML execution, SFS, and outlier identification
├── src/SMaRT_Pack/           # The core Python package
│   ├── DataProcessing/       # Loaders, chemistry logic, and stats engine
│   ├── Descriptors/          # Element-based feature engineering,featurization
|   └── DevModelPrac/         # Model templates and evaluation
├── pyproject.toml            # Package configuration and dependencies
└── README.md                 # Project documentation