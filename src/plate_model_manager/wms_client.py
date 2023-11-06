from typing import List

from .network_requests import fetch_file


def get_map(
    layers: List[str],
    styles: List[str],
    format="image/png",
    width=1800,
    height=800,
    bbox=[-180, -80, 180, 80],
    server_url: str = "https://geoserver.gplates.org/geoserver",
    version: str = "1.1.0",
):
    url = (
        f"{server_url}/wms?service=WMS&version={version}&request=GetMap&layers={','.join(layers)}"
        + f"&bbox={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}&width={width}&height={height}&srs=EPSG:4326"
        + f"&styles={','.join(styles)}&format={format}"
    )
    print(fetch_file(url, "./", filename="test.png"))
