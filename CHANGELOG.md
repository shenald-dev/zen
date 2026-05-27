@@ -1,5 +1,11 @@
 # Changelog
 
+## [0.1.14] - 2026-05-26
+
+### Changed
+* **[Reliability]:** Modified the `console` truthiness check in the exception handler to explicitly check `console is not None`. Guarded dependency baselines with safe upper bounds (`rich<16.0.0`, `typer<0.26.0`) in `pyproject.toml` to prevent future breaking releases from breaking the build.
+* **[Release]:** Cut release v0.1.14 to finalize stability and safety improvements.
+
 ## [0.1.13] - 2026-05-22
 
 ### Changed