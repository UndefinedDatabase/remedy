"""F287 claim measurement — what provider session resume does today (read-only).

Run from the repository root: `python3 .agent/authored/f287-r1-measure.py`. It imports the
product, instantiates every production provider without calling it, and reads source text;
it starts no provider process and writes nothing.
"""
import inspect
import re
from pathlib import Path

from packages.orchestration import pingpong_loop as loop
from packages.orchestration import pingpong_provider as pp

print("1. supports_resume per provider (instantiated, never called)")
for cls in (pp.FakeProvider, pp.ClaudeProvider, pp.ClaudeCliProvider, pp.OllamaPingPongProvider):
    obj = cls()
    print(f"   {cls.__name__:24} name={obj.name!r:14} supports_resume={obj.supports_resume}")

print("2. build_claude_cli_args: parameters and the argv of a plain call")
print("  ", list(inspect.signature(pp.build_claude_cli_args).parameters))
print("  ", pp.build_claude_cli_args("claude", "PROMPT"))

print("3. ClaudeCliProvider: which methods take `resume`, and how often the body uses it")
for meth in ("build", "_build_impl", "review", "_review_impl", "_call", "_call_streamed",
             "_call_reviewer_structured"):
    fn = getattr(pp.ClaudeCliProvider, meth)
    src = inspect.getsource(fn)
    body = src[src.index(") ->") :] if ") ->" in src else src
    print(f"   {meth:26} takes_resume={'resume' in inspect.signature(fn).parameters}"
          f"  body_uses={len(re.findall(r'(?<![_.])resume(?![_])', body))}")

print("4. ClaudeCliProvider outputs: is resume_used / resume_session_ref ever set?")
csrc = inspect.getsource(pp.ClaudeCliProvider)
print("   resume_used:", csrc.count("resume_used"),
      " resume_session_ref:", csrc.count("resume_session_ref"))

print("5. run_pingpong: the R-1055 relaunch hand-over and the fallback-once rule")
lsrc = inspect.getsource(loop)
for needle in ('resume_sessions.get("builder")', 'resume_sessions.get("reviewer")',
               "builder_out.resume_fallback = True", "reviewer_out.resume_fallback = True"):
    print(f"   {needle!r}: {lsrc.count(needle)}")

print("6. the claude-cli provider's working directory is the run's staging path")
fsrc = inspect.getsource(loop._create_provider_with_cwd)
print('   \'"cwd": staging_dir\' in _create_provider_with_cwd:', '"cwd": staging_dir' in fsrc)

print("7. tests that construct a resuming claude-cli provider today")
hits = [str(p) for p in sorted(Path("tests").rglob("test_*.py"))
        if re.search(r"ClaudeCliProvider\([^)]*\)\.supports_resume|claude-cli.*resume_used",
                     p.read_text(encoding="utf-8", errors="replace"))]
print("  ", hits or "none")
