PYTHON ?= python
ZIP ?= zip
UNZIP ?= unzip
FLAKE8 ?= flake8
INSTALL_DIR ?= /tmp/atlassian-alfred-workflow

TARGET = target
ATLASSIAN_WORKFLOW = $(TARGET)/Atlassian\ Workflow
ARCHIVE = $(ATLASSIAN_WORKFLOW).alfredworkflow
PYTHON_SOURCES = *.py atlassian
SOURCES = icon.png info.plist $(PYTHON_SOURCES)
SETUPTOOLS = $(PYTHON) setup.py

$(TARGET)/alfred-workflow-1.13.tar.gz = https://codeload.github.com/deanishe/alfred-workflow/tar.gz/v1.13

init:
	mkdir -p $(TARGET) $(TARGET)/workflow
	mkdir -p $(ATLASSIAN_WORKFLOW) $(ATLASSIAN_WORKFLOW)/workflow

$(TARGET)/%.tar.gz: init
	curl -o "$@" "$($@)"

$(TARGET)/%: $(TARGET)/%.tar.gz
	tar -C $(TARGET) -xzf "$^"

bdist-%: $(TARGET)/%
	cd $^; $(SETUPTOOLS) bdist_egg

assemble-workflow: $(TARGET)/alfred-workflow-1.13

assemble: assemble-workflow
	cp $(TARGET)/alfred-workflow-1.13/workflow/* $(TARGET)/workflow

	cp -r $(SOURCES) $(ATLASSIAN_WORKFLOW)
	cp $(TARGET)/workflow/* $(ATLASSIAN_WORKFLOW)/workflow/
	rm -f $(ARCHIVE)
	cd $(ATLASSIAN_WORKFLOW); $(ZIP) -rq ../../$(ARCHIVE) .

develop: assemble test
	ln -sf $(TARGET)/workflow workflow

install: assemble
	$(UNZIP) -oq $(ARCHIVE) -d $(INSTALL_DIR)

code-quality:
	$(FLAKE8) $(PYTHON_SOURCES)

test: code-quality

clean:
	rm -rf $(TARGET) workflow
	find . -name "*.pyc"
