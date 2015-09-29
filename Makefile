PYTHON ?= python
ZIP ?= zip
UNZIP ?= unzip
#INSTALL_DIR ?= ~/Documents/Alfred/Alfred.alfredpreferences/workflows/user.workflow.7AE7E44F-2B27-4962-8FD8-074AD733480B
INSTALL_DIR ?= /tmp/alfred-jira-workflow

TARGET = target
JIRA_WORKFLOW = $(TARGET)/Jira\ Workflow
ARCHIVE = $(JIRA_WORKFLOW).alfredworkflow
SOURCES = icon.png info.plist jiraissues2alfred.py
SETUPTOOLS = $(PYTHON) setup.py

$(TARGET)/jira-0.50.tar.gz = https://pypi.python.org/packages/source/j/jira/jira-0.50.tar.gz
$(TARGET)/requests-2.7.0.tar.gz = https://pypi.python.org/packages/source/r/requests/requests-2.7.0.tar.gz
$(TARGET)/alfred-workflow-1.13.tar.gz = https://codeload.github.com/deanishe/alfred-workflow/tar.gz/v1.13

init:
	mkdir -p $(TARGET) $(TARGET)/lib $(TARGET)/workflow
	mkdir -p $(JIRA_WORKFLOW) $(JIRA_WORKFLOW)/lib $(JIRA_WORKFLOW)/workflow

$(TARGET)/%.tar.gz: init
	curl -o "$@" "$($@)"

$(TARGET)/%: $(TARGET)/%.tar.gz
	tar -C $(TARGET) -xzf "$^"

bdist-%: $(TARGET)/%
	cd $^; $(SETUPTOOLS) bdist_egg

assemble-jira: bdist-jira-0.50

assemble-requests: bdist-requests-2.7.0

assemble-workflow: $(TARGET)/alfred-workflow-1.13

assemble: assemble-jira assemble-requests assemble-workflow
	cp $(TARGET)/jira-0.50/dist/*py2.7*.egg $(TARGET)/lib
	cp $(TARGET)/requests-2.7.0/dist/*py2.7*.egg $(TARGET)/lib
	cp $(TARGET)/alfred-workflow-1.13/workflow/* $(TARGET)/workflow

	cp $(SOURCES) $(JIRA_WORKFLOW)
	cp $(TARGET)/lib/* $(JIRA_WORKFLOW)/lib
	cp $(TARGET)/workflow/* $(JIRA_WORKFLOW)/workflow
	rm -f $(ARCHIVE)
	cd $(JIRA_WORKFLOW); $(ZIP) -rq ../../$(ARCHIVE) .

develop: assemble
	ln -sf $(TARGET)/lib lib
	ln -sf $(TARGET)/workflow workflow

install: assemble
	$(UNZIP) -oq $(ARCHIVE) -d $(INSTALL_DIR)

clean:
	rm -rf $(TARGET) lib workflow
