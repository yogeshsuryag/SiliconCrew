from types import SimpleNamespace

import start


def _stub_groups(monkeypatch, *, account_groups, process_groups, effective_gid=1000):
    def getgrnam(name):
        assert name == start.DOCKER_SOCKET_GROUP
        return SimpleNamespace(gr_gid=967)

    monkeypatch.setattr(start.grp, "getgrnam", getgrnam)
    monkeypatch.setattr(
        start.pwd,
        "getpwuid",
        lambda uid: SimpleNamespace(pw_name="yogesh", pw_gid=1000),
    )
    monkeypatch.setattr(start.os, "getuid", lambda: 1000)
    monkeypatch.setattr(start.os, "getgrouplist", lambda name, gid: account_groups)
    monkeypatch.setattr(start.os, "getgroups", lambda: process_groups)
    monkeypatch.setattr(start.os, "getegid", lambda: effective_gid)


def test_docker_group_refresh_is_needed_when_account_has_group_but_process_does_not(monkeypatch):
    _stub_groups(monkeypatch, account_groups=[1000, 967], process_groups=[1000])

    assert start._docker_group_needs_refresh(start.DOCKER_SOCKET_GROUP)


def test_docker_group_refresh_is_not_needed_when_process_already_has_group(monkeypatch):
    _stub_groups(monkeypatch, account_groups=[1000, 967], process_groups=[1000, 967])

    assert not start._docker_group_needs_refresh(start.DOCKER_SOCKET_GROUP)


def test_docker_group_refresh_is_not_needed_when_account_is_not_a_member(monkeypatch):
    _stub_groups(monkeypatch, account_groups=[1000], process_groups=[1000])

    assert not start._docker_group_needs_refresh(start.DOCKER_SOCKET_GROUP)
