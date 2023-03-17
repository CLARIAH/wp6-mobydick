[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# Herman Melville- Moby Dick

This repo contains a single book in different representations:

*   `tei`: [TEI](https://tei-c.org)
    (our source, from the [DBNL](https://www.dbnl.orgdbnl.org))
*   `tf`: [Text-Fabric](https://github.com/annotation/text-fabric)
*   `pd`: [Pandas](https://pandas.pydata.org)

The conversion TEI to TF is done with [programs/tfFromTei.py](programs/tfFromTei.py).

The conversion TF to Pandas is done with [programs/bigTable.py](programs/bigTable.py).

For an example of how to use the Pandas file, see
[programs/pandas.ipynb](https://nbviewer.org/github/CLARIAH/wp6-mobydick/blob/main/programs/pandas.ipynb).

See [docs](docs) for documentation about provenance and encoding.

# Requirements

If you want to reproduce or make your own computations, pip-install the following
Python modules

``` sh
pip install text-fabric pandas pyarrow
```

Also, clone this repo, preferably in your
`~/github/CLARIAH` directory.

# Author

See [about](docs/about.md) for the authors/editors of the data.

[Dirk Roorda](https://github.com/dirkroorda) is the author of the
representation in Text-Fabric of the data,
and the programs and docs.
