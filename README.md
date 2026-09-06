# GenPark AI Agent Skill - Safe Tool Execution Sentinel

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Tool execution safety sentinel enforcing filesystem path containment, network egress domain allowlists, and command binary restrictions.

```mermaid
flowchart TD
    A[Agent Tool Action] --> B{Safety Sentinel Checks}
    B -->|Path Traversal?| C[Block & Raise Violation]
    B -->|Unauthorized Domain?| D[Block Egress]
    B -->|Dangerous Binary sudo/rm?| E[Block Command]
    B -->|All Safe| F[Permit Execution]
```

## Features
- **Path Traversal Shield**: Blocks `../` escapes outside designated workspace root.
- **Egress Guard**: Enforces strict domain allowlists for outbound network calls.
- **Zero External Dependencies**: Python 3.9+ standard library.

## Quickstart
```python
from client import SafeToolContainmentSentinelClient

sentinel = SafeToolContainmentSentinelClient(root_dir="/app/sandbox")
check = sentinel.validate_file_path("../etc/passwd")
print(check["is_safe"])
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
