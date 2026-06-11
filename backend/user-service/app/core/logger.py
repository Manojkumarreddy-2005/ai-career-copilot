import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level, # Pure structlog processor variant
        structlog.processors.JSONRenderer()
    ]
)

def get_logger(name: str):
    return structlog.get_logger(name)