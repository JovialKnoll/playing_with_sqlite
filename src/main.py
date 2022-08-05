import sys

import projectapi


def demoApi():
    # print(projectapi.getProject(new_project_id))
    projectapi.updateProjectStatus(1, 30)
    for p in projectapi.getAllProjects():
        print(p)
    # projectapi.updateProjectStatus(2, 4)
    # projectapi.updateProjectStatus(3)
    # print(projectapi.getAllProjects())
    projectapi.closeDB()


if __name__ == '__main__':
    demoApi()

sys.exit()
