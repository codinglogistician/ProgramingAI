from mcp.server.fastmcp import FastMCP
import pandas as pd


mcp = FastMCP("Tools")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

@mcp.tool()
def search_apartments(min_price: int, max_price: int):
    """Search apartments in Warsaw by price range. Returns max 3 offers with direct URLs to listings."""
    df = pd.read_csv("data/adresowo_warszawa_wroclaw.csv").drop_duplicates()

    # Czyszczenie cen
    df['price_total_zl'] = (
        df['price_total_zl']
        .astype(str)
        .str.replace(" ", "")
        .str.replace(",", "")
        .str.extract(r"(\d+)")
    )
    df['price_total_zl'] = pd.to_numeric(df['price_total_zl'], errors="coerce")
    results = df[
        (df['city'] == "Warszawa") &
        (df['price_total_zl'] >= min_price) &
        (df['price_total_zl'] <= max_price)
    ].head(5)

    return results[['locality', 'street', 'rooms', 'area_m2', 'price_total_zl', 'url']].to_dict(orient="records")


if __name__ == "__main__":
    mcp.run(transport="stdio")