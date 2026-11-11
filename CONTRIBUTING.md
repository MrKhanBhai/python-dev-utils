# Contributing

Thanks for considering a contribution to python-dev-utils.

## Before starting

1. Search existing issues and pull requests to avoid duplicate work.
2. For a significant feature, open an issue first to discuss its scope.
3. Keep changes focused and avoid adding runtime dependencies without a strong reason.

## Development setup

Python 3.10 or newer is required.

```bash
git clone https://github.com/MrKhanBhai/python-dev-utils.git
cd python-dev-utils
python -m pip install -e ".[dev]"
```

## Make and verify changes

- Add or update unit tests for every behavior change.
- Include edge cases such as empty inputs, missing paths, and invalid arguments where relevant.
- Keep file operations streaming when practical.
- Do not make destructive changes to user files.
- Run the following before submitting:

```bash
python -m unittest discover -s tests -v
ruff check .
dev-utils --help
python -m build
```

## Pull request checklist

- [ ] The change solves one clearly described problem.
- [ ] Tests cover the new or changed behavior.
- [ ] Documentation and examples are updated where needed.
- [ ] Unit tests, lint, CLI smoke test, and package build pass locally where available.
- [ ] No secrets, generated artifacts, or unrelated formatting changes are included.

Please describe what changed, why it is useful, and how it was tested. If a check could not be run, say so clearly.
