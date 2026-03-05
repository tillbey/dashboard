# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "fastexcel==0.19.0",
#     "marimo",
#     "polars==1.38.1",
#     "pyarrow==23.0.1",
# ]
# ///

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt
    import pyodide.http
    return alt, mo, pl, pyodide


@app.cell
def _():
    # data_path = mo.notebook_location() / 'public' / 'Diamond OA - NL Journals - WGNM - FINAL - SHAREABLE-version 2.xlsx'
    # data_path = 'https://zenodo.org/records/17195184/files/Diamond%20OA%20-%20NL%20Journals%20-%20WGNM%20-%20FINAL%20-%20SHAREABLE-version%202.xlsx'
    data_path = 'https://docs.google.com/spreadsheets/d/1CaHEgS6Nu9OAeyEHe9tmCpMgnhRr196zFp2gsRw20YM/export?format=xlsx'
    return (data_path,)


@app.cell
async def _(data_path, pyodide):
    res = await pyodide.http.pyfetch(data_path)
    with open('/data.xlsx', 'wb') as f:
        f.write(await res.bytes())
    return


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
def _(domain_chart, mo, platform_chart, publisher_chart):
    mo.vstack([
        mo.hstack([platform_chart, publisher_chart]),
        mo.hstack([domain_chart])
    ])
    return


@app.cell
def _(pl):
    journals = pl.read_excel('/data.xlsx', sheet_name='Included DOA Journals')
    journals
    return (journals,)


if __name__ == "__main__":
    app.run()
