import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GenerateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        shutil.copytree(ROOT / "project-setup", self.tmp_path / ".roster")

    def tearDown(self):
        self.tmp.cleanup()

    def run_generate(self):
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, ".roster/generate.py"],
            cwd=self.tmp_path,
            text=True,
            capture_output=True,
            env=env,
        )

    def test_generate_writes_all_tool_adapters(self):
        result = self.run_generate()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.tmp_path / ".claude/skills/roster/SKILL.md").exists())
        self.assertTrue((self.tmp_path / ".cursor/rules/roster.mdc").exists())
        self.assertTrue((self.tmp_path / ".windsurf/rules/roster.md").exists())
        self.assertTrue((self.tmp_path / "AGENTS.md").exists())

    def test_unmanaged_agents_file_is_not_overwritten(self):
        agents_path = self.tmp_path / "AGENTS.md"
        agents_path.write_text("existing project rules\n", encoding="utf-8")

        result = self.run_generate()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            agents_path.read_text(encoding="utf-8"),
            "existing project rules\n",
        )
        self.assertTrue((self.tmp_path / ".roster/generated/AGENTS.roster.md").exists())
        self.assertIn("existing unmanaged AGENTS.md", result.stdout)

    def test_modified_managed_file_blocks_regeneration(self):
        first = self.run_generate()
        self.assertEqual(first.returncode, 0, first.stderr)

        managed_path = self.tmp_path / ".cursor/rules/roster.mdc"
        managed_path.write_text(
            managed_path.read_text(encoding="utf-8") + "\nmanual edit\n",
            encoding="utf-8",
        )

        second = self.run_generate()

        self.assertEqual(second.returncode, 1)
        self.assertIn("Cannot overwrite .cursor/rules/roster.mdc", second.stdout)


if __name__ == "__main__":
    unittest.main()
