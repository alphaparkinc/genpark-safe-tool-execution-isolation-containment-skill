"""
Demonstration of genpark-safe-tool-execution-isolation-containment-skill
"""

from client import SafeToolContainmentSentinelClient

def main():
    sentinel = SafeToolContainmentSentinelClient(
        allowed_root_dir=r"D:	mp_sandbox",
        allowed_domains=["api.github.com", "genpark.ai"]
    )

    # 1. Test directory escape attempt
    p_check = sentinel.validate_file_path(r"../../Windows/System32/config/SAM")
    print("Path traversal check:", p_check)

    # 2. Test valid path
    p_valid = sentinel.validate_file_path("workspace/output.txt")
    print("Valid file path check:", p_valid)

    # 3. Test domain egress
    d_bad = sentinel.validate_domain("malicious-c2-server.com")
    print("Domain egress check:", d_bad)

    # 4. Test dangerous command
    cmd_bad = sentinel.validate_command_safety(["sudo", "rm", "-rf", "/"])
    print("Dangerous command check:", cmd_bad)

if __name__ == "__main__":
    main()
