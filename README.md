# Atlassian Alfred Workflow

Shows the list of issues of a given filter and allows you to copy/insert their key and summary.

## Installation

Clone the repository locally, change into its directory, and make assemble:

```
git clone 	https://github.com/resamsel/atlassian-alfred-workflow.git
cd atlassian-alfred-workflow
make assemble
```

Then double click the **Atlassian Workflow.alfredworkflow** file within the **target** directory.

## Configuration

Configuration can be done using the installed Alfred workflow. Type `awf` into the Alfred input window and use tab on each configuration entry. Then enter the value of that entry and hit enter.

Here is an example configuration:

```
awf jira-server https://jira.atlassian.com
awf bamboo-server https://bamboo.atlassian.com
awf username myuser
awf password mypassword
awf jira-filter 12345
awf bamboo-project PROJECT
```

### Keychain Access

The password will be saved in the OSX Keychain, so it will not be saved in clear text.

**The password will never be shown in the workflows!**

## Development

```
make develop
```
