PYTHON ?= python
ZIP ?= zip
UNZIP ?= unzip
FLAKE8 ?= flake8
SETUPTOOLS ?= $(PYTHON) setup.py
ATLASSIAN_WORKFLOW ?= /tmp/atlassian-alfred-workflow

TARGET = target
WORKFLOW = $(TARGET)/Atlassian\ Workflow
ARCHIVE = $(WORKFLOW).alfredworkflow
PYTHON_SOURCES = src/*
SOURCES = icon.png info.plist $(PYTHON_SOURCES)
INSTALL_DIR = $(ATLASSIAN_WORKFLOW)

$(TARGET)/alfred-workflow-1.13.tar.gz = https://pypi.python.org/packages/source/A/Alfred-Workflow/Alfred-Workflow-1.13.tar.gz

init:
	mkdir -p $(TARGET) $(TARGET)/workflow
	mkdir -p $(WORKFLOW) $(WORKFLOW)/workflow

.PRECIOUS: $(TARGET)/%.tar.gz

$(TARGET)/%.tar.gz: init
	curl -o "$@" "$($@)"

$(TARGET)/%: $(TARGET)/%.tar.gz
	tar -C $(TARGET) -xzf "$^"

bdist-%: $(TARGET)/%
	cd $^; $(SETUPTOOLS) bdist_egg

assemble-workflow: $(TARGET)/alfred-workflow-1.13
	cp $(TARGET)/alfred-workflow-1.13/workflow/* $(TARGET)/workflow

assemble: assemble-workflow
	cp -r $(SOURCES) $(WORKFLOW)
	cp $(TARGET)/workflow/* $(WORKFLOW)/workflow/
	rm -f $(ARCHIVE)
	cd $(WORKFLOW); $(ZIP) -rq ../../$(ARCHIVE) .

develop: assemble-workflow
	$(SETUPTOOLS) develop

install-workflow: assemble
	$(UNZIP) -oq $(ARCHIVE) -d $(INSTALL_DIR)

code-quality:
	$(FLAKE8) $(PYTHON_SOURCES)

test: code-quality

clean:
	$(SETUPTOOLS) clean
	rm -rf $(TARGET)
	find . -type l -delete
	find . -name "*.pyc" -delete
