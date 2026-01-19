# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.0",
#     "pyzmq",
# ]
# ///

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pyodide.http
    import altair as alt
    return alt, mo, pyodide


@app.cell
async def _(pyodide):
    res = await pyodide.http.pyfetch('https://docs.google.com/spreadsheets/d/e/2PACX-1vTSaXarmKB4RWMlpEDueeMBnwp4_BYJDUwTgBvhqCQ_-hpco9-fa7yZrAIr0T-TIA/pub?output=csv')
    with open('/organizations.csv', 'wb') as f:
        f.write(await res.bytes())

    res = await pyodide.http.pyfetch('https://docs.google.com/spreadsheets/d/e/2PACX-1vQwM24DIUWmqbjxaAy62w9w8gNpOMSg5sxmFro-OexCeMzIlyUJh5iVVsVxyrcLkQ/pub?output=csv')
    with open('/repositories.csv', 'wb') as f:
        f.write(await res.bytes())
    return


@app.cell
def _(mo):
    organizations = mo.sql(
        f"""
        select * from read_csv('/organizations.csv')
        """
    )
    return (organizations,)


@app.cell
def _(mo):
    repositories = mo.sql(
        f"""
        select * from read_csv('/repositories.csv')
        """
    )
    return (repositories,)


@app.cell
def _(mo, organizations, repositories):
    df = mo.sql(
        f"""
        select * from organizations o full join repositories r on o.OpenAIRE_ORG_ID = r.OpenAIRE_ORG_ID;
        """
    )
    return (df,)


@app.cell
def _(mo):
    kind = mo.ui.dropdown(options=['Total Research Products', 'Publications', 'Research data', 'Research software', 'Other research products'], value='Publications')
    kind
    return (kind,)


@app.cell
def _(alt, df, kind, mo):
    chart = mo.ui.altair_chart(
     alt.Chart(data=df).mark_bar().encode(x='grouping', y=kind.value)   
    )
    chart
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
