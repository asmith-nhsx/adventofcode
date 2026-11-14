# Knit every solution.Rmd under this folder to GitHub markdown (solution.md).
#
# Usage, from anywhere:
#   Rscript aoc2022/render.R                          # all solutions
#   Rscript aoc2022/render.R aoc2022/q1/p1            # one folder
#   Rscript aoc2022/render.R aoc2022/q1/p1/solution.Rmd
#
# Each file is rendered in its own R session, as RStudio's Knit button does,
# so console output (package banners, warnings) matches knitting in RStudio.

# Use RStudio's bundled pandoc if pandoc isn't otherwise available.
if (!rmarkdown::pandoc_available()) {
  rstudio_pandoc <- "C:/Program Files/RStudio/bin/quarto/bin/tools"
  if (file.exists(file.path(rstudio_pandoc, "pandoc.exe"))) {
    Sys.setenv(RSTUDIO_PANDOC = rstudio_pandoc)
  } else {
    stop("pandoc not found: install RStudio or pandoc")
  }
}

render_one <- function(f) {
  f <- normalizePath(f, winslash = "/")
  env <- new.env(parent = globalenv())
  # harness() calls rstudioapi::getSourceEditorContext() to find test.txt and
  # input.txt, which only works inside RStudio. Defining it in the knit
  # environment shadows the attached rstudioapi version.
  env$getSourceEditorContext <- function() list(path = f)
  rmarkdown::render(f, envir = env, quiet = TRUE,
                    output_options = list(html_preview = FALSE))
}

all_args <- commandArgs(trailingOnly = FALSE)
script <- normalizePath(sub("^--file=", "", grep("^--file=", all_args, value = TRUE)))
args <- commandArgs(trailingOnly = TRUE)

# Child mode: render a single file in this session.
if (length(args) == 2 && args[1] == "--one") {
  render_one(args[2])
  quit(status = 0)
}

target <- if (length(args)) args[1] else dirname(script)
files <- if (grepl("\\.Rmd$", target)) target else
  list.files(target, pattern = "\\.Rmd$", recursive = TRUE, full.names = TRUE)
if (!length(files)) stop("no .Rmd files found under ", target)

rscript <- file.path(R.home("bin"), "Rscript")
failed <- character()
for (f in files) {
  cat("==>", f, "\n")
  status <- system2(rscript, c(shQuote(script), "--one", shQuote(f)))
  if (status != 0) failed <- c(failed, f)
}

cat("\nRendered", length(files) - length(failed), "of", length(files), "files\n")
if (length(failed)) {
  cat("Failed:\n", paste(" ", failed, collapse = "\n"), "\n")
  quit(status = 1)
}
