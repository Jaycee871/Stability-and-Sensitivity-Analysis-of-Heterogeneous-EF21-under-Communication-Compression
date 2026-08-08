# Phase 6 — Core reference audit

This file records the authoritative public sources used to verify the initial manuscript bibliography. It is a provenance aid; `manuscript/references.bib` remains the machine-readable bibliography.

## `thomsen2026tight`

**Daniel Berg Thomsen, Adrien Taylor, Aymeric Dieuleveut. _A Tight Theory of Error Feedback Algorithms in Distributed Optimization_. 2026.**

- Source: arXiv record
- URL: https://arxiv.org/abs/2605.31594
- Checked: title, author order, year, arXiv identifier
- Manuscript role: inherited source paper; Empirical Law 4.3; homogeneous baseline and PEP context

## `richtarik2021ef21`

**Peter Richtárik, Igor Sokolov, Ilyas Fatkhullin. _EF21: A New, Simpler, Theoretically Better, and Practically Faster Error Feedback_. NeurIPS 2021.**

- Source: official NeurIPS paper page
- URL: https://papers.nips.cc/paper_files/paper/2021/hash/231141b34c82aa95e48810a9d1b33a79-Abstract.html
- Checked: title, authors, venue, volume 34, pages 4384--4396
- Manuscript role: EF21 background and contractive-compression setting

## `karimireddy2019error`

**Sai Praneeth Karimireddy, Quentin Rebjock, Sebastian U. Stich, Martin Jaggi. _Error Feedback Fixes SignSGD and Other Gradient Compression Schemes_. ICML 2019.**

- Source: PMLR proceedings page
- URL: https://proceedings.mlr.press/v97/karimireddy19a.html
- Checked: title, authors, PMLR volume 97, pages 3252--3261, year
- Manuscript role: foundational modern error-feedback theory

## `stich2018sparsified`

**Sebastian U. Stich, Jean-Baptiste Cordonnier, Martin Jaggi. _Sparsified SGD with Memory_. NeurIPS 2018.**

- Source: official NeurIPS paper page
- URL: https://papers.nips.cc/paper/7697-sparsified-sgd-with-memory
- Checked: title, authors, volume 31, pages 4452--4463, year
- Manuscript role: compression with memory/error compensation

## `seide2014onebit`

**Frank Seide, Hao Fu, Jasha Droppo, Gang Li, Dong Yu. _1-bit Stochastic Gradient Descent and Its Application to Data-Parallel Distributed Training of Speech DNNs_. Interspeech 2014.**

- Source: ISCA Archive
- URL: https://www.isca-archive.org/interspeech_2014/seide14_interspeech.html
- Checked: authors, pages 1058--1062, DOI 10.21437/Interspeech.2014-274
- Manuscript role: early practical error-feedback / residual-carry mechanism

## `drori2014performance`

**Yoel Drori, Marc Teboulle. _Performance of First-Order Methods for Smooth Convex Minimization: A Novel Approach_. Mathematical Programming 145, 451--482 (2014).**

- Sources: Google Research publication record and journal metadata
- URL: https://research.google/pubs/performance-of-first-order-methods-for-smooth-convex-minimization-a-novel-approach/
- DOI: 10.1007/s10107-013-0653-0
- Checked: title, authors, volume, pages, year, DOI
- Manuscript role: performance estimation problem background

## `taylor2017exact`

**Adrien B. Taylor, Julien M. Hendrickx, François Glineur. _Exact Worst-Case Performance of First-Order Methods for Composite Convex Optimization_. SIAM Journal on Optimization 27(3), 1283--1313 (2017).**

- Source: SIAM Journal on Optimization article page
- DOI: 10.1137/16M108104X
- Checked: title, author order, volume/issue, pages, year, DOI
- Manuscript role: exact PEP / semidefinite worst-case analysis background

## Citation policy for the draft

- Cite the 2026 source paper whenever an inherited theorem, empirical law, or formula is stated.
- Cite EF21 for the algorithmic lineage and distributed contractive-compression context.
- Cite Seide/Stich/Karimireddy only for historical and conceptual error-feedback background.
- Cite Drori--Teboulle and Taylor--Hendrickx--Glineur when discussing performance estimation.
- Do not cite these papers as support for the new Phase 2--4 numerical findings; those findings are supported by the repository's own audited outputs.
