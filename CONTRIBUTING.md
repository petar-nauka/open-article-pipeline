# Contributing

Contributions that improve accuracy, usability, portability, or editorial quality are welcome.

## Before changing a rule

Describe the observed failure and a realistic request that reproduces it. Identify the smallest skill or reference that should change. A single example should not become an absolute rule for every genre or topic. Preserve explicit user constraints, the chosen evidence boundary, and the distinction between factual readiness and permission to publish.

## Submit a change

1. Open an issue for a substantial workflow change, or make a focused pull request for a clear fix.
2. Keep `SKILL.md` descriptions selective and instructions short. Put conditional detail in a linked reference. A skill must also remain usable alone.
3. If you change `scripts/validate_run.py`, run `python -m unittest discover -s tests -v` and add a test for the new behavior. The script must report mechanical checks honestly; do not make it claim semantic fact verification.
4. Run the local skill validator where available: `python path/to/skill-creator/scripts/quick_validate.py skills/<changed-skill>`.
5. Try the changed workflow on more than one genre and on both ordinary and risky evidence. Report what changed, what you observed, and what remains uncertain.

Avoid including private source files, unpublished drafts, personal data, credentials, or full copyrighted articles in examples or tests. Link to public evidence when a test case needs real sources; synthetic cases should be labeled as synthetic.

## Review criteria

Reviewers check whether the change improves an actual decision, keeps source provenance traceable, handles uncertainty honestly, and avoids adding unnecessary steps to unrelated requests. A new source count, rigid article outline, or extra output file needs a clear reason.
