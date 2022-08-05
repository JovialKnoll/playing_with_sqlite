import os
import sqlite3
from collections.abc import Sequence


_DB_FILE = 'project.db'
# setup api
_db_existed = os.path.isfile(_DB_FILE)
_connection = sqlite3.connect(_DB_FILE)
_cursor = _connection.cursor()
if not _db_existed:
    # init DB
    _cursor.execute(
        '''CREATE TABLE ProjectStatus_tbl (
            projectStatusId INTEGER PRIMARY KEY
        ,   projectStatusName TEXT NOT NULL
        )'''
    )
    project_statuses = [
        ("New Project",),
        ("Estimate Created",),
        ("Deposit Paid",),
        ("Purchase Order Sent",),
        ("Materials Received",),
        ("Installation Scheduled",),
        ("Installation Complete",),
        ("Final Invoice Paid",),
    ]
    _cursor.executemany(
        '''INSERT INTO ProjectStatus_tbl (
            projectStatusName
        ) VALUES (
            ?
        )''',
        project_statuses
    )
    _cursor.execute(
        '''CREATE TABLE Project_tbl (
            projectId INTEGER PRIMARY KEY
        ,   customerName TEXT NOT NULL
        ,   customerAddress TEXT NOT NULL
        ,   projectStatusId INTEGER NOT NULL DEFAULT 1
        
        ,   FOREIGN KEY(projectStatusId) REFERENCES ProjectStatus_tbl(projectStatusId)
        )'''
    )
    _connection.commit()


def closeDB():
    _cursor.close()
    _connection.close()


def postNewProject(customer_name: str, customer_address: str):
    _cursor.execute(
        '''INSERT INTO Project_tbl (
            customerName
        ,   customerAddress
        ) VALUES (
            ?
        ,   ?
        )''',
        (
            customer_name,
            customer_address,
        )
    )
    _connection.commit()
    return _cursor.lastrowid


def _getProjectFromRow(row: Sequence):
    return {
        'projectId': row[0],
        'customerName': row[1],
        'customerAddress': row[2],
        'projectStatusId': row[3],
    }


def getAllProjects():
    projects = _cursor.execute(
        '''SELECT
            projectId
        ,   customerName
        ,   customerAddress
        ,   projectStatusId
        FROM Project_tbl
        '''
    ).fetchall()
    return [_getProjectFromRow(row) for row in projects]


def getProject(project_id: int):
    project = _cursor.execute(
        '''SELECT
            projectId
        ,   customerName
        ,   customerAddress
        ,   projectStatusId
        FROM Project_tbl
        WHERE projectId = ?
        ''',
        (
            project_id,
        )
    ).fetchone()
    if not project:
        return None
    return _getProjectFromRow(project)


def updateProjectStatus(project_id: int, project_status: int | str | None = None):
    if type(project_status) == 'str':
        # grab and convert to int
        pass
    if project_status is None:
        # grab current and += 1
        pass
    _cursor.execute(
        '''UPDATE Project_tbl
        SET projectStatusId = ?
        WHERE projectId = ?
        ''',
        (
            project_status,
            project_id,
        )
    )
