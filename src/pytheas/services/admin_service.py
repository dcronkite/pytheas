from pytheas.tasks.load_data import load_data

TASKS = {
    'load_data': load_data
}


def get_tasks():
    return [
        {'value': 'load_data', 'name': 'Load Data'}
    ]


def run_task(task):
    TASKS[task]()
