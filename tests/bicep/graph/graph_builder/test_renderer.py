from pathlib import Path

from checkov.bicep.graph_manager import BicepGraphManager
from checkov.common.graph.db_connectors.db_connector import DBConnector


def test_render_parameter():
    # given
    test_dir = Path(__file__).parent / "examples/parameter"
    graph_manager = BicepGraphManager(db_connector=DBConnector())

    # when
    local_graph, _ = graph_manager.build_graph_from_source_directory(source_dir=str(test_dir), render_variables=True)

    # then
    vertex = local_graph.vertices[local_graph.vertices_by_name["vm"]]

    assert vertex.config["config"] == {
        "name": "example-vm",
        "location": "location",
        "properties": {
            "networkProfile": {"networkInterfaces": [{"id": "example-id"}]},
            "osProfile": {
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {"keyData": "key-data-1", "path": "path-1"},
                            {"keyData": "key-data-2", "path": "path-2"},
                            {"keyData": "key-data-3", "path": "path-3"},
                            {"keyData": "key-data-4", "path": "path-4"},
                        ]
                    }
                }
            },
            "storageProfile": {"imageReference": {"publisher": "MicrosoftWindowsServer"}},
        },
        "tags": {
            "displayName": "Container Registry",
            "'container.registry.name'": "exmaple-acr",
            "'container.registry'": {"name": "exmaple-nested-acr"},
        },
    }
