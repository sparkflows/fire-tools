from pathlib import Path

_RES = Path(__file__).resolve().parent.parent / "resources"

class MySqlMcpService:
    """Python port of the Java MySqlMcpService tools.
    Each method returns the contents of the matching JSON file as a string.
    """

    def _read(self, relpath: str) -> str:
        p = _RES / relpath
        return p.read_text(encoding="utf-8")

    # === Tools that return resource JSONs ===
    def createWorkflow(self) -> str:
        return self._read("workflow/Read-And-Display-Data.json")

    def LegoblockXMLParser(self) -> str:
        return self._read("pipeline/xmlparser.json")

    def LegoblockXMLMapping(self) -> str:
        return self._read("pipeline/xmlMapping.json")

    def createPipelineNode(self) -> str:
        return self._read("pipeline_node/xmlMapping.json")

    def createWorkflowNode(self) -> str:
        return self._read("workflow_node/csv.json")
