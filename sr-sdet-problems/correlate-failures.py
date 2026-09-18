from collections import defaultdict


def correlate_failures(logs):

    failures_by_trace = defaultdict(list)

    for log in logs:
        if log.get("level") != "ERROR":
            continue

        trace_id = log.get("trace_id")

        if not trace_id:
            continue

        failures_by_trace[trace_id].append(
            {"service": log.get("service"), "message": log.get("message")}
        )

    return dict(failures_by_trace)


def find_cross_service_failures(logs):

    trace_services = defaultdict(set)

    for log in logs:
        if log.get("level") != "ERROR":
            continue

        trace_id = log.get("trace_id")
        service = log.get("service")

        if trace_id and service:
            trace_services[trace_id].add(service)

    # Return requests that failed in multiple services.
    return {
        trace_id: services
        for trace_id, services in trace_services.items()
        if len(services) > 1
    }


logs = [
    {
        "service": "checkout",
        "trace_id": "abc123",
        "level": "ERROR",
        "message": "Checkout failed",
    },
    {
        "service": "payment",
        "trace_id": "abc123",
        "level": "ERROR",
        "message": "Payment timeout",
    },
    {
        "service": "inventory",
        "trace_id": "abc123",
        "level": "INFO",
        "message": "Inventory reserved",
    },
    {
        "service": "auth",
        "trace_id": "xyz789",
        "level": "ERROR",
        "message": "Invalid token",
    },
]


result = correlate_failures(logs)
result2 = find_cross_service_failures(logs)
print(result)
print(result2)
