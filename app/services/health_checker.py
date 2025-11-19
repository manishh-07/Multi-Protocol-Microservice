class HealthChecker:
    @staticmethod
    def perform_check() -> dict:
        # In real prod, check DB connection, Redis, Disk space here
        return {
            "status": "operational",
            "is_healthy": True,
            "component": "eros-health-module"
        }