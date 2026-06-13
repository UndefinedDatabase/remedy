"""Contract tests for frontend degraded state visibility and CommandBar."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestDegradedBannerContract:
    def test_degraded_banner_component_exists(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "DegradedBanner.tsx"
        assert f.is_file(), "DegradedBanner.tsx not found"

    def test_degraded_banner_uses_role_alert(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "DegradedBanner.tsx"
        content = f.read_text()
        assert 'role="alert"' in content, "DegradedBanner must use role=alert for accessibility"

    def test_degraded_banner_shows_failed_endpoints(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "DegradedBanner.tsx"
        content = f.read_text()
        assert "failedEndpoints" in content, "DegradedBanner must display failed endpoints"

    def test_shell_renders_degraded_banner(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"
        content = f.read_text()
        assert "DegradedBanner" in content, "RemedyShell must render DegradedBanner"
        assert "apiHealth" in content, "RemedyShell must pass apiHealth to DegradedBanner"


class TestCommandBarCopiesCommand:
    def test_command_bar_uses_clipboard(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "components" / "command" / "CommandBar.tsx"
        content = f.read_text()
        assert "clipboard" in content, "CommandBar must use clipboard API"
        assert "nextAction.command" in content, "CommandBar must copy command not label"

    def test_command_bar_has_copy_button(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "components" / "command" / "CommandBar.tsx"
        content = f.read_text()
        assert 'aria-label="Copy next safe command"' in content

    def test_api_types_has_command_field(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "api" / "types.ts"
        content = f.read_text()
        assert "command: string" in content, "RemedyNextAction must have command field"

    def test_api_health_type_exists(self):
        f = REPO_ROOT / "apps" / "ui" / "src" / "api" / "types.ts"
        content = f.read_text()
        assert "RemedyApiHealth" in content
        assert "degraded: boolean" in content
        assert "failedEndpoints: string[]" in content
