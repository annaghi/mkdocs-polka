
# MkDocs Polka

MkDocs project demonstrating the [Polka](https://github.com/annaghi/polka) crate.

Polka is a markdown AST transforms via [markdown-it Rust port](https://github.com/markdown-it-rust/markdown-it), exposed to Python through [PyO3](https://pyo3.rs/) / [maturin](https://www.maturin.rs/).

## Prerequisites

- Python 3.12+
- [Rust](https://rustup.rs/)
- [uv](https://docs.astral.sh/uv/)

## Quick Start

```shell
make install
make serve
```

## Debugging

Set `POLKA_DEBUG=1` to write AST output at each transform stage to `.debug/`.

`make serve` enables this by default.

## Commands

| Command | Description |
|---------|-------------|
| `make install` | Full dev environment setup |
| `make serve` | MkDocs dev server (enables `POLKA_DEBUG=1`) |
| `make build` | Build MkDocs site (compiles Rust first) |
| `make compile` | Compile Rust extension via maturin |
| `make fix` | Auto-format and lint (pre-commit) |
| `make clean` | Remove all build artifacts, caches, venv |
| `make reset` | `clean` + `install` |
| `make upgrade` | Full upgrade cycle (deps + pre-commit hooks) |


