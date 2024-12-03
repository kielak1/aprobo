# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
#SPHINXBUILD   ?= sphinx-build
SPHINXBUILD = /opt/avantic/env/bin/sphinx-build

SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Special target for HTML to change ownership after building
html: Makefile
	@sudo chown -R tkielak:tkielak "$(BUILDDIR)/html"
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@sudo chown -R nginx:nginx "$(BUILDDIR)/html"


# Clean target to remove the build directory
clean:
	@echo "Removing build directory..."
	@sudo chown -R tkielak:tkielak "$(BUILDDIR)/html"
	@rm -rf "$(BUILDDIR)/html"/*
	@echo "Build directory removed."

	# Clean target specifically for LaTeX build directory
clean_latex:
	@echo "Removing LaTeX build directory..."
	@rm -rf "$(BUILDDIR)/latex"
	@echo "LaTeX build directory removed."

# Target for building LaTeX PDF documentation
latexpdf: clean_latex Makefile
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "LaTeX PDF documentation built."