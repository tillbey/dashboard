# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "fastexcel==0.19.0",
#     "marimo",
#     "openpyxl==3.1.5",
#     "polars==1.38.1",
#     "pyarrow==23.0.1",
# ]
# ///

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # Diamond Open Access journals in the Netherlands
    """)
    return


@app.cell
def _(domain_chart, mo, platform_chart, publisher_chart, years_chart):
    mo.vstack([
        mo.hstack([platform_chart, publisher_chart]),
        mo.hstack([domain_chart, years_chart])
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    The data behind the dashboard can be found below, and also on Zenodo under [10.5281/zenodo.17185088](https://doi.org/10.5281/zenodo.17185088).
    """)
    return


@app.cell
def _(data_path, pl):
    journals = pl.read_excel(data_path, sheet_name='Included Diamond OA Journals', engine='openpyxl')
    journals
    return (journals,)


@app.cell
def _(alt, journals):
    years_chart = (
        alt.Chart(journals)
        .mark_bar()
        .encode(
            x=alt.X(field='DOAJ - Year OA', type='quantitative'),
            y=alt.Y(aggregate='count', type='quantitative'),
            color=alt.Color(field='Model', type='nominal'),
            tooltip=[
                alt.Tooltip(field='DOAJ - Year OA', format=',.0f'),
                alt.Tooltip(aggregate='count'),
                alt.Tooltip(field='Model')
            ]
        )
        .properties(height=300, width=300)
    )
    return (years_chart,)


@app.cell
async def _():
    # data_path = mo.notebook_location() / 'public' / 'Diamond OA - NL Journals - WGNM - FINAL - SHAREABLE-3.xlsx'

    import micropip
    await micropip.install('polars')
    await micropip.install('altair')
    await micropip.install('openpyxl')

    data_path = 'https://docs.google.com/spreadsheets/d/1CaHEgS6Nu9OAeyEHe9tmCpMgnhRr196zFp2gsRw20YM/export?format=xlsx'
    return (data_path,)


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt
    return alt, mo, pl


@app.cell
def _(alt, journals):
    domain_chart = (
        alt.Chart(journals)
        .mark_arc(innerRadius=80)
        .encode(
            color=alt.Color(field='OpenAlex - domain', type='nominal'),
            theta=alt.Theta(aggregate='count', type='quantitative'),
            tooltip=[
                alt.Tooltip(aggregate='count'),
                alt.Tooltip(field='Journal Title')
            ]
        )
        .properties(height=300, width=300)
    )
    return (domain_chart,)


@app.cell
def _(alt, journals):
    publisher_chart = (
        alt.Chart(journals)
        .mark_arc(innerRadius=80)
        .encode(
            color=alt.Color(field='Publisher', type='nominal'),
            theta=alt.Theta(aggregate='count', type='quantitative'),
            tooltip=[
                alt.Tooltip(aggregate='count'),
                alt.Tooltip(field='Journal Title')
            ]
        )
        .properties(height=300, width=300)
    )
    return (publisher_chart,)


@app.cell
def _(alt, journals):
    platform_chart = (
        alt.Chart(journals)
        .mark_arc(innerRadius=80)
        .encode(
            color=alt.Color(field='Technical platform', type='nominal'),
            theta=alt.Theta(aggregate='count', type='quantitative'),
            tooltip=[
                alt.Tooltip(aggregate='count'),
                alt.Tooltip(field='Publisher')
            ]
        )
        .properties(height=300, width=300)
    )
    return (platform_chart,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
