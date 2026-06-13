"""Initialize knowledge base with sample solutions, patterns, and procedures.

This script populates the Chroma knowledge base with example data for demonstration.
"""
from src.tools.chroma_kb import ChromaKnowledgeBase


def initialize_knowledge_base():
    """Populate knowledge base with sample data."""
    kb = ChromaKnowledgeBase(persist_dir="./data/chroma_db")
    
    # Clear existing data if needed (for testing)
    # In production, you might want to preserve existing data
    
    # Add sample solutions
    sample_solutions = [
        {
            "id": "sol_001",
            "title": "Database Connection Timeout",
            "description": "Database connection fails with timeout error after 30 seconds",
            "steps": [
                "Check database server status",
                "Verify network connectivity",
                "Increase connection timeout in application config",
                "Restart application",
            ],
            "root_cause": "Database server is slow or unreachable",
            "tags": ["database", "connection", "timeout", "network"]
        },
        {
            "id": "sol_002",
            "title": "High Memory Usage - Memory Leak",
            "description": "Application memory usage grows over time until system runs out of memory",
            "steps": [
                "Enable memory profiling",
                "Identify unreleased objects",
                "Check for circular references",
                "Review recent code changes",
                "Deploy fix and monitor memory",
            ],
            "root_cause": "Memory leak in application code",
            "tags": ["memory", "performance", "leak", "java", "python"]
        },
        {
            "id": "sol_003",
            "title": "API Rate Limit Exceeded",
            "description": "API returns 429 Too Many Requests error",
            "steps": [
                "Check API rate limit documentation",
                "Implement exponential backoff retry",
                "Add request queuing mechanism",
                "Contact API provider if limit too low",
            ],
            "root_cause": "Application exceeding API rate limits",
            "tags": ["api", "rate-limit", "throttling", "external-service"]
        },
        {
            "id": "sol_004",
            "title": "SSL Certificate Expiration",
            "description": "HTTPS connections fail with SSL certificate expired error",
            "steps": [
                "Check certificate expiration date",
                "Renew certificate with CA",
                "Update certificate in application/server",
                "Test HTTPS connections",
                "Update certificate renewal schedule",
            ],
            "root_cause": "SSL certificate expired",
            "tags": ["ssl", "certificate", "https", "security"]
        },
        {
            "id": "sol_005",
            "title": "Out of Disk Space",
            "description": "Application fails to write files: No space left on device",
            "steps": [
                "Identify large directories with: du -sh /*",
                "Check log files and clean up old logs",
                "Review temporary files and caches",
                "Remove unnecessary data or archives",
                "Configure log rotation and retention",
            ],
            "root_cause": "Disk storage full",
            "tags": ["disk-space", "storage", "filesystem", "maintenance"]
        },
    ]
    
    for sol in sample_solutions:
        kb.add_solution(
            solution_id=sol["id"],
            title=sol["title"],
            description=sol["description"],
            steps=sol["steps"],
            root_cause=sol["root_cause"],
            tags=sol["tags"]
        )
    
    # Add sample error patterns
    sample_patterns = [
        {
            "id": "pat_001",
            "error_signature": "java.net.ConnectException: Connection refused",
            "symptoms": "Application cannot connect to service, connection refused immediately",
            "resolution": "Check if target service is running, firewall rules, and network connectivity",
            "frequency": "frequent"
        },
        {
            "id": "pat_002",
            "error_signature": "OutOfMemoryError: Java heap space",
            "symptoms": "Application suddenly crashes, memory usage at maximum",
            "resolution": "Increase heap size, identify and fix memory leaks, optimize memory usage",
            "frequency": "occasional"
        },
        {
            "id": "pat_003",
            "error_signature": "ERROR: relation does not exist",
            "symptoms": "Database queries fail, table or column not found",
            "resolution": "Check database schema, run migrations, verify table names and schema",
            "frequency": "occasional"
        },
        {
            "id": "pat_004",
            "error_signature": "TimeoutError: Request timeout",
            "symptoms": "API calls hang and timeout after N seconds",
            "resolution": "Reduce timeout values, improve backend performance, check network latency",
            "frequency": "frequent"
        },
        {
            "id": "pat_005",
            "error_signature": "Failed to authenticate with credentials",
            "symptoms": "Login or API authentication fails despite correct credentials",
            "resolution": "Check token expiration, verify credentials, check authentication service status",
            "frequency": "occasional"
        },
    ]
    
    for pattern in sample_patterns:
        kb.add_error_pattern(
            pattern_id=pattern["id"],
            error_signature=pattern["error_signature"],
            symptoms=pattern["symptoms"],
            resolution=pattern["resolution"],
            frequency=pattern["frequency"]
        )
    
    # Add sample procedures
    sample_procedures = [
        {
            "id": "proc_001",
            "title": "Emergency Restart Procedure",
            "description": "Steps to safely restart production services with minimal downtime",
            "steps": [
                "Check current system status and health metrics",
                "Notify team of planned restart",
                "Stop accepting new requests (graceful shutdown)",
                "Wait for in-flight requests to complete",
                "Stop application services",
                "Clear temporary files and caches",
                "Start application services",
                "Verify services are healthy",
                "Re-enable request acceptance",
                "Monitor metrics for 30 minutes",
            ],
            "prerequisites": ["VPN access", "SSH access", "Admin credentials", "Runbooks available"]
        },
        {
            "id": "proc_002",
            "title": "Database Backup and Recovery",
            "description": "Procedure for backing up database and recovering from backup",
            "steps": [
                "Stop write operations to database",
                "Execute backup command",
                "Verify backup integrity",
                "Upload backup to secure storage",
                "For recovery: Locate backup file",
                "Stop database service",
                "Restore from backup",
                "Start database service",
                "Verify data consistency",
            ],
            "prerequisites": ["Database access", "Storage credentials", "Backup tool installed"]
        },
        {
            "id": "proc_003",
            "title": "Application Rolling Update",
            "description": "Safely update application with zero downtime",
            "steps": [
                "Build new application version",
                "Run test suite against new version",
                "Create backup of current version",
                "Update instance 1 of N",
                "Health check instance 1",
                "Route traffic away from instance 1",
                "Repeat for each instance",
                "Monitor logs and metrics",
                "Perform smoke tests",
            ],
            "prerequisites": ["CI/CD pipeline", "Load balancer access", "Monitoring tools"]
        },
    ]
    
    for proc in sample_procedures:
        kb.add_procedure(
            proc_id=proc["id"],
            title=proc["title"],
            description=proc["description"],
            steps=proc["steps"],
            prerequisites=proc["prerequisites"]
        )
    
    # Print statistics
    stats = kb.get_stats()
    print("Knowledge Base Initialized Successfully!")
    print(f"  Solutions: {stats['solutions']} entries")
    print(f"  Error Patterns: {stats['patterns']} entries")
    print(f"  Procedures: {stats['procedures']} entries")
    print(f"  Total: {sum(stats.values())} entries")


if __name__ == "__main__":
    initialize_knowledge_base()
