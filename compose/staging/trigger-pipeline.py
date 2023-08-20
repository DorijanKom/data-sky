import gitlab
import time
import sys

application = sys.argv[1]
version = sys.argv[2]
environment = sys.argv[3]


def deploy(application, version, environment):
    # try:
    gl = gitlab.Gitlab("https://gitlab.com", private_token="xvLDRAGCYcTPrrVjP-hH")
    project = gl.projects.get("19928181", lazy=True)  # no API call
    pl = project.trigger_pipeline(
        "master",
        "d341d10fde7f953839b57ad9909d5b",
        variables={
            "DEPLOY": "AutoDeployDevelop",
            "APPLICATION": application,
            "VERSION": version,
            "ENVIRONMENT": environment,
        },
    )
    while pl.finished_at is None:
        pl.refresh()
        time.sleep(1)
    print("Job status: " + pl.status + "\n" + pl.web_url)
    if pl.status == "failed":
        return "Deploy pipeline failed!"
    # except Exception as err:
    #     print(err)
    #     return(err)


deploy(application, version, environment)
