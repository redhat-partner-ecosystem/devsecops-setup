from github import Github

def get_create_label(repo, name, description, color):
    labels = repo.get_labels()
    for label in labels:
        if label.name == name:
            return label
    
    return repo.create_label(name, color, description)


def create_issue(repo, title, body, labels=[], check_exists=True):

    if check_exists:
        open_issues = repo.get_issues(state='open', labels=labels)
        for issue in open_issues:
            if issue.title == title:
                return None

    return repo.create_issue(title=title, body=body, labels=labels)