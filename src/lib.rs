use std::path::Path;
use std::path::PathBuf;

use markdown_it::MarkdownIt;
use markdown_it::plugins::{cmark, extra, html};
use pyo3::prelude::*;

fn create_parser(icon_dirs: Vec<PathBuf>) -> MarkdownIt {
    let mut md = MarkdownIt::new();
    // CommonMark
    cmark::add(&mut md);
    // Markdown Extensions
    // Don't enable extra::typographer, because it converts `--` to `–` in Text nodes,
    // breaking CSS custom property names like `--color` in attributes.
    extra::beautify_links::add(&mut md);
    // extra::heading_anchors::add(&mut md, slugify);
    extra::linkify::add(&mut md);
    extra::smartquotes::add(&mut md);
    extra::strikethrough::add(&mut md);
    extra::tables::add(&mut md);
    html::add(&mut md);
    polka::add(&mut md, icon_dirs);
    md
}

#[pyfunction]
#[must_use]
pub fn generate_html(filename: &str, content: &str, icon_dirs: Vec<String>) -> String {
    #[allow(clippy::collapsible_if)]
    if cfg!(debug_assertions)
        && std::env::var("POLKA_DEBUG").is_ok()
        && Path::new(filename).file_stem().is_some_and(|s| s == "index")
    {
        if let Ok(cwd) = std::env::current_dir() {
            polka::set_debug(Some(cwd.join(".debug")));
        }
    } else {
        polka::set_debug(None);
    }

    let icon_dirs = icon_dirs.into_iter().map(PathBuf::from).collect();
    let md = create_parser(icon_dirs);
    let ast = md.parse(content);

    ast.render()
}

#[pyfunction]
fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

#[pymodule]
fn bridge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_function(wrap_pyfunction!(generate_html, m)?)?;
    Ok(())
}
