from scripts.analyze_health_report import evaluate_report, extract_disk_usage


def test_extract_disk_usage() -> None:
    output = (
        "Filesystem 1024-blocks Used Available Capacity Mounted on\n"
        "/dev/sda2 100000 25000 75000 25% /"
    )

    assert extract_disk_usage(output) == 25


def test_healthy_report() -> None:
    report = {
        "hostname": "server-01",
        "disk_output": "/dev/sda2 100000 25000 75000 25% /",
        "nginx_status": "running",
    }

    result = evaluate_report(report)

    assert result["status"] == "healthy"
    assert result["disk_usage_percent"] == 25
    assert result["findings"] == []


def test_critical_disk_usage() -> None:
    report = {
        "hostname": "server-01",
        "disk_output": "/dev/sda2 100000 95000 5000 95% /",
        "nginx_status": "running",
    }

    result = evaluate_report(report)

    assert result["status"] == "critical"
    assert result["disk_usage_percent"] == 95


def test_stopped_nginx_is_critical() -> None:
    report = {
        "hostname": "server-01",
        "disk_output": "/dev/sda2 100000 25000 75000 25% /",
        "nginx_status": "stopped",
    }

    result = evaluate_report(report)

    assert result["status"] == "critical"
    assert result["findings"][0]["component"] == "nginx"
