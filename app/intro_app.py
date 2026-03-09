import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo

    import geopandas as gpd
    import odc.stac
    import pystac_client
    import xarray as xr

    import holoviews as hv
    import hvplot.xarray


@app.cell
def _():
    # Our little 'utils' module
    import utils

    # Keep this outside of the setup cell so changes can be reloaded without affecting anything else
    return (utils,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Sentinel-2 Explorer
    """)
    return


@app.function
def find_stac_items(bbox, time_range):
    catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=time_range,
    )

    items = list(search.item_collection())
    return items


@app.cell
def _():
    # Area of interest (AoI) bounding box
    lat_min, lon_min = 27.706, -15.843
    lat_max, lon_max = 28.203, -15.321
    bbox = (lon_min, lat_min, lon_max, lat_max)

    time_range = "2023-04-01/2023-04-30"

    my_items = find_stac_items(bbox, time_range)
    print(f"Found {len(my_items)} matching STAC items.")
    return bbox, my_items


@app.cell
def _():
    load_data_button = mo.ui.run_button(label="Load data")
    load_data_button
    return (load_data_button,)


@app.cell
def _(bbox, load_data_button, my_items):
    mo.stop(not load_data_button.value, "Click ☝️ to load")

    resolution = 200  # Downsampled for demo purposes

    s2_ds = odc.stac.load(
        items=my_items,
        resolution=resolution,
        groupby="solar_day",
        bbox=bbox,
        bands=["red", "green", "blue", "scl"],
    )

    # Reformat as DataArray for later use
    s2_data = s2_ds[["red", "green", "blue", "scl"]].to_dataarray(dim="band")
    return (s2_data,)


@app.cell
def _(s2_data):
    # A dropdown to let us choose a scene
    _labels = [str(t) for t in s2_data["time"].values]
    scene_selector = mo.ui.dropdown(options=_labels, value=_labels[0], label="Choose scene date")
    scene_selector
    return (scene_selector,)


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
def _():
    gamma_slider = mo.ui.slider(start=0.5, stop=0.8, step=0.01, show_value=True, label="Gamma")
    # gamma_slider  # Don't display the widget yet.
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
    rgb_plot = plot_rgb(time=scene_selector.value)
    return (rgb_plot,)


@app.cell
def _(plot_scl, scene_selector):
    scl_plot = plot_scl(time=scene_selector.value)
    return (scl_plot,)


@app.cell
def _(gamma_slider, rgb_plot, scl_plot):
    mo.hstack(
        [
            mo.vstack([gamma_slider, rgb_plot], align="center"),
            scl_plot,
        ],
        align="end",
    )
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
def _(s2_data, sample_points):
    _xs = xr.DataArray(sample_points.geometry.x, dims="sample")
    _ys = xr.DataArray(sample_points.geometry.y, dims="sample")
    scl_sampled = s2_data.sel(x=_xs, y=_ys, method="nearest")
    scl_sampled = scl_sampled.sel(band="scl").rename("scl")
    scl_sampled = scl_sampled.assign_coords(sample=sample_points.label)
    return (scl_sampled,)


@app.cell
def _(scl_sampled, utils):
    def plot_scl_timeseries():
        return scl_sampled.hvplot.scatter(
            x="time", y="sample", color="scl", cmap=utils.scl_cmap
        ).opts(legend_labels=utils.scl_names, title="SCL time series")

    return (plot_scl_timeseries,)


@app.cell
def _(plot_scl_timeseries):
    timeseries_plot = plot_scl_timeseries()
    return (timeseries_plot,)


@app.cell
def _(timeseries_plot):
    timeseries_plot
    return


if __name__ == "__main__":
    app.run()
