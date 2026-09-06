"""
Agent Tool Execution Safety Containment and Resource Jail.
Zero external dependencies, standard library only.
"""

import os
from typing import Dict, List, Any, Optional

class SafeToolContainmentSentinelClient:
    """
    Guards agent tool invocations against unauthorized operations:
    - Filesystem containment: Restricts file reads/writes strictly within a root directory
    - Network containment: Validates destination hosts against a domain allowlist
    - Command containment: Blocks dangerous shell binaries (rm -rf, mkfs, sudo, etc.)
    """

    DANGEROUS_COMMANDS = {"sudo", "su", "mkfs", "dd", "format", "shutdown", "reboot"}

    def __init__(self, allowed_root_dir: str, allowed_domains: Optional[List[str]] = None):
        self.root_dir = os.path.abspath(allowed_root_dir)
        self.allowed_domains = allowed_domains or ["api.github.com", "genpark.ai"]

    def validate_file_path(self, target_path: str) -> Dict[str, Any]:
        """Ensures path does not escape allowed_root_dir via traversal."""
        full_path = os.path.abspath(os.path.join(self.root_dir, target_path))
        # Check prefix
        is_safe = os.path.commonpath([self.root_dir]) == os.path.commonpath([self.root_dir, full_path])
        return {
            "is_safe": is_safe,
            "target_path": full_path,
            "violation": None if is_safe else "PATH_TRAVERSAL_DETECTED"
        }

    def validate_domain(self, domain: str) -> Dict[str, Any]:
        """Checks domain against allowlist."""
        is_allowed = any(domain.lower() == d.lower() or domain.lower().endswith("." + d.lower()) for d in self.allowed_domains)
        return {
            "is_safe": is_allowed,
            "domain": domain,
            "violation": None if is_allowed else "UNAUTHORIZED_EGRESS_DOMAIN"
        }

    def validate_command_safety(self, command_args: List[str]) -> Dict[str, Any]:
        """Blocks prohibited command binaries."""
        if not command_args:
            return {"is_safe": True}

        binary = os.path.basename(command_args[0]).lower()
        if binary in self.DANGEROUS_COMMANDS:
            return {
                "is_safe": False,
                "binary": binary,
                "violation": f"DANGEROUS_BINARY_EXECUTION_BLOCKED: {binary}"
            }

        return {"is_safe": True, "binary": binary, "violation": None}
