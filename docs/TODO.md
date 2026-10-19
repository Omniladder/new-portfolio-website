# TODO

Deferred work that's been agreed on but not started. Not decisions (those go in `docs/arch/`) — just things to come back to.

- **Example projects in `docs/examples/`.** Eventually write a few complete example forks (a sample `data.json` plus any assets it references) showing what a finished portfolio looks like, so someone forking the repo has more to go on than `data.template.json`. Blocked on the `data.json` schema settling — today it only models `projects[].project_name`, so an example would be stale almost immediately. `docs/examples/` exists as a placeholder until then.
- **Build out `templates/project.html` and `templates/project_home.html`.** Both are still empty placeholders — the home page's "Projects" top-nav link and "View more projects..." link point at a projects index that doesn't render anything yet.
- **Automatically restyle uploaded images to look 90s.** Eventually have the `process_assets` manipulate step (currently a no-op, see [0016](arch/0016-process-assets-image-pipeline.md)) transform images dropped into `assets/` to match the site's retro aesthetic, instead of requiring forkers to pre-style their own images.
