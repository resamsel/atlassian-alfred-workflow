PACKAGE_NAME ?= atlassian
PYTHON ?= python
ZIP ?= zip
UNZIP ?= unzip
ATLASSIAN_WORKFLOW ?= /tmp/atlassian-alfred-workflow

# Code quality and coverage
FLAKE8 ?= flake8 --max-complexity=16
PYLINT ?= pylint

TARGET = target
WORKFLOW = $(TARGET)/Atlassian\ Workflow
ARCHIVE = $(WORKFLOW).alfredworkflow
PYTHON_SOURCES = src/*
SOURCES = icon.png info.plist $(PYTHON_SOURCES)
INSTALL_DIR = $(ATLASSIAN_WORKFLOW)

SETUPTOOLS = $(PYTHON) setup.py
TEST_NOSE = nosetests --with-coverage --cover-package=$(PACKAGE_NAME) --cover-html \
	--cover-html-dir=$(PWD)/$(TARGET)/coverage
TEST = $(SETUPTOOLS) $(TEST_NOSE)

$(TARGET)/Alfred-Workflow-1.13.tar.gz = https://pypi.python.org/packages/source/A/Alfred-Workflow/Alfred-Workflow-1.13.tar.gz

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

assemble-workflow: $(TARGET)/Alfred-Workflow-1.13
	cp $^/workflow/* $(TARGET)/workflow

	cp -r $(SOURCES) $(WORKFLOW)
	cp $(TARGET)/workflow/* $(WORKFLOW)/workflow/
	rm -f $(ARCHIVE)
	cd $(WORKFLOW); $(ZIP) -rq ../../$(ARCHIVE) .

assemble: assemble-workflow

develop:
	$(SETUPTOOLS) develop

install:
	$(SETUPTOOLS) install

install-workflow: assemble-workflow
	$(UNZIP) -oq $(ARCHIVE) -d $(INSTALL_DIR)

check-code:
	$(FLAKE8) src
	$(PYLINT) src/$(PACKAGE_NAME)

test: init check-code
	$(TEST)

clean:
	$(SETUPTOOLS) clean
	rm -rf $(TARGET)
	find . -type l -delete
	find . -name "*.pyc" -delete
