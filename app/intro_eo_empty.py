import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Introducing _marimo_ for Earth Observation

    By Luke McQuade, [EO Analytics Group](https://www.plus.ac.at/geoinformatik/research/research-areas/eo-analytics/?lang=en), Z_GIS, University of Salzburg

    A brief introduction to using [marimo](https://marimo.io) notebooks in Earth Observation (EO) work.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## First steps - reactivity & widgets
    """)
    return


@app.cell
def _():
    # Expressions are output

    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Further info:

    Guides to [reactivity](https://docs.marimo.io/guides/reactivity/) and [cell outputs](https://docs.marimo.io/guides/outputs/) — marimo docs
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## STAC query

    Query the [Element84 STAC API](https://element84.com/earth-search) for Sentinel-2 data.
    """)
    return


@app.cell
def _():
    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Load data

    Create an Xarray Dataset/DataArray from the STAC items, using [odc.stac.load](https://odc-stac.readthedocs.io/en/latest/_api/odc.stac.load.html).
    """)
    return


@app.cell
def _():
    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Scene plots
    """)
    return


@app.cell
def _():
    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Time series
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Load point data
    """)
    return


@app.cell
def _():
    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Sample SCL at points
    """)
    return


@app.cell
def _():
    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Plot SCL classes over time
    """)
    return


@app.cell
def _():
    # ...
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tips, tricks, other things

    ...
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Getting started

    Clone [this repo](https://github.com/lukesdm/marimo-intro-eo):
    ```
    git clone https://github.com/lukesdm/marimo-intro-eo
    ```

    Then, e.g.,
    ```
    docker compose up --build
    ```
    And browse to `http://localhost:8080`.

    *Or*, outside a container with [pixi](https://pixi.prefix.dev/latest/) ([installation](https://pixi.prefix.dev/latest/installation/)):

    ```
    cd app
    pixi install
    pixi run marimo edit
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Further reading



    [NYC Taxi trips with Lonboard and GeoParquet](https://developmentseed.org/lonboard/latest/examples/marimo/nyc_taxi_trips/) — Kyle Barron (Development Seed)
    """)
    return


if __name__ == "__main__":
    app.run()
