import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo

    import geopandas as gpd
    import pystac_client
    import xarray as xr


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

    "Hello " + "Z_GIS"
    return


@app.cell
def _():
    def say_hello(name):
        return "Hello " + name

    "Hello Salzburg"

    say_hello("Z_GIS")

    # (Only the final expression is output)
    return


@app.cell
def _():
    sentinel = 2

    # (No return value, no output)
    return (sentinel,)


@app.cell
def _(sentinel):
    fave_mission = f"Copernicus Sentinel-{sentinel}"

    # (Note the underline)
    return (fave_mission,)


@app.cell
def _(fave_mission):
    mo.md(f"""
    My favourite mission is **{fave_mission}**
    """)
    return


@app.cell
def _():
    sentinel_slider = mo.ui.slider(start=1, stop=5, show_value=True)
    sentinel_slider
    return (sentinel_slider,)


@app.cell
def _(sentinel_slider):
    second_fave = f"Copernicus Sentinel-{sentinel_slider.value}"
    return (second_fave,)


@app.cell
def _(second_fave):
    mo.md(f"""
    My second favourite mission is **{second_fave}**
    """)
    return


@app.cell
def _():
    # Uncomment and try this:
    # fave_mission = "Landsat 8"
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
    def find_stac_items(bbox, time_range):
        catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=time_range,
        )

        items = list(search.item_collection())
        return items

    # This is a 'reusable' function - it can be imported directly from other Python files.
    # See https://docs.marimo.io/guides/reusing_functions/
    return (find_stac_items,)


@app.cell
def _(find_stac_items):
    # Area of interest (AoI) bounding box
    lat_min, lon_min = 27.706, -15.843
    lat_max, lon_max = 28.203, -15.321
    bbox = (lon_min, lat_min, lon_max, lat_max)

    time_range = "2023-04-01/2023-04-30"

    my_items = find_stac_items(bbox, time_range)
    print(f"Found {len(my_items)} matching STAC items.")
    return bbox, my_items


@app.cell
def _(my_items):
    # Show STAC contents as a (geo)dataframe
    gpd.GeoDataFrame.from_features(my_items, crs="EPSG:4326")
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
    # Add package via terminal with:
    # pixi add odc-stac
    import odc.stac

    return (odc,)


@app.cell
def _():
    load_data_button = mo.ui.run_button(label="Load data")
    load_data_button
    return (load_data_button,)


@app.cell
def _(bbox, load_data_button, my_items, odc):
    mo.stop(not load_data_button.value, "Click ☝️ to load")

    resolution = 200  # Downsampled for demo purposes

    s2_ds = odc.stac.load(
        items=my_items,
        resolution=resolution,
        groupby="solar_day",
        bbox=bbox,
        bands=["red", "green", "blue", "scl"],
        # Make this a lazy dask array by setting chunks, e.g.,
        # chunks={"x": "auto", "y": "auto", "time": "auto"}
    )

    # Reformat as DataArray for later use
    s2_data = s2_ds[["red", "green", "blue", "scl"]].to_dataarray(dim="band")
    return (s2_data,)


@app.cell
def _(s2_data):
    # Preview the data (as an array)
    s2_data
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Scene plots
    """)
    return


@app.cell
def _():
    # Luke's choice of plotting library
    # https://holoviews.org/

    import holoviews as hv
    import hvplot.xarray

    # Others such as Altair and Plotly have tighter reactive integration with marimo, though
    return


@app.cell
def _():
    # Our little 'utils' module
    import utils

    # Keep this outside of the setup cell so changes can be reloaded without affecting anything else
    return (utils,)


@app.cell
def _(s2_data):
    # The timestamps of our available scenes
    s2_data["time"]
    return


@app.cell
def _(s2_data):
    # A dropdown to let us choose a scene
    _labels = [str(t) for t in s2_data["time"].values]
    scene_selector = mo.ui.dropdown(options=_labels, value=_labels[0])
    scene_selector
    return (scene_selector,)


@app.cell
def _(scene_selector):
    scene_selector.value
    return


@app.cell
def _(s2_data, scene_selector):
    s2_data_slice = s2_data.sel(time=scene_selector.value)
    return (s2_data_slice,)


@app.cell
def _(s2_data_slice, utils):
    def plot_scl(time):
        data = s2_data_slice.sel(band="scl")
        scl_plot = (
            data
            .astype(str)
            .hvplot.image(cmap=utils.scl_cmap, data_aspect=1.0)
        )
        return scl_plot

    return (plot_scl,)


@app.cell
def _(plot_scl, scene_selector):
    plot_scl(time=scene_selector.value)
    return


@app.cell
def _():
    gamma_slider = mo.ui.slider(start=0.5, stop=0.8, step=0.01, show_value=True)
    gamma_slider
    return (gamma_slider,)


@app.cell
def _(gamma_slider, s2_data_slice):
    def plot_rgb(time):
        data = s2_data_slice ** gamma_slider.value
        data = data.clip(min=0, max=255)
        return data.hvplot.rgb(x="x", y="y", bands="band", aspect=1)

    return (plot_rgb,)


@app.cell
def _(plot_rgb, scene_selector):
    plot_rgb(time=scene_selector.value)
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
    _sample_points_file = "/data/gran_canaria/sample_points.gpkg"

    sample_points_file = mo.watch.file(_sample_points_file)
    return (sample_points_file,)


@app.cell
def _(sample_points_file):
    sample_points = gpd.read_file(sample_points_file)
    return (sample_points,)


@app.cell
def _(sample_points):
    sample_points
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Sample SCL at points
    """)
    return


@app.cell
def _(s2_data, sample_points):
    _xs = xr.DataArray(sample_points.geometry.x, dims="sample")
    _ys = xr.DataArray(sample_points.geometry.y, dims="sample")
    scl_sampled = s2_data.sel(x=_xs, y=_ys, method="nearest")
    scl_sampled = scl_sampled.sel(band="scl").rename("scl")
    scl_sampled = scl_sampled.assign_coords(sample=sample_points.label)
    return (scl_sampled,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Plot SCL classes over time
    """)
    return


@app.cell
def _(scl_sampled, utils):
    scl_sampled.hvplot.scatter(
        x="time", y="sample", color="scl", cmap=utils.scl_cmap
    ).opts(legend_labels=utils.scl_names)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tips, tricks, other things

    - Split cells to avoid re-running unneccessarily.

    - Renaming things, moving imports between cells and similar can cause unwanted re-runs.

    - Check out 'Explore dependencies'.

    - Reactive mode is optional.

    - Building widgets from other widgets is tricky (referencing `.value` in same cell not allowed).

    - [Cycles](https://docs.marimo.io/guides/understanding_errors/cycles/) between cells are not supported.

    - Working with [expensive notebooks](https://docs.marimo.io/guides/expensive_notebooks/) — marimo docs

    - Has a [VS Code extension](https://marimo.io/blog/vscode).

    - [molab](https://molab.marimo.io/notebooks): marimo's version of colab.

    - Integration in JupyterHub possible with [marimo-jupyter-extension](https://github.com/marimo-team/marimo-jupyter-extension).

    - Strong [AI integration](https://docs.marimo.io/guides/editor_features/ai_completion/).

    - Under heavy development, expect some rough edges.

    - Governance: Created by Akshay Agrawal and Myles Scolnick in 2023; Apache 2.0 licensed; acquired by CoreWeave in November 2025.
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
