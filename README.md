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

Open the workflow in the Alfred preferences and edit the **Sprint Script Filter**. Change the values for your *server*, *username*, *password*, and *filter* according to your needs.

Here is an example:

```
SERVER=https://jira.atlassian.com
USERNAME=resamsel
PASSWORD=$(cat ~/.domain_password)
FILTER=12345

/usr/bin/python jiraissues2alfred.py $SERVER $USERNAME $PASSWORD $FILTER
```

## Development

```
make develop
```
