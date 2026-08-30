# Pipeline assets

The files in this directory are public contracts, not the experiment's source records.

- [`flow.mmd`](flow.mmd) is the editable Mermaid overview.
- [`checks.md`](checks.md) lists the gates a real authorized run must satisfy.
- [`../examples/manifest.example.json`](../examples/manifest.example.json) is a synthetic manifest accepted by the validator.

The private implementation may have several route-specific versions. A public manifest should always identify the route, configuration, source version, temporal window and missingness policy rather than pretending that all runs are equivalent.

