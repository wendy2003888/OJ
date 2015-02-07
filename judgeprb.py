from App.judge import put_task_into_queue, worker
from App import db
from App.models import Submit

if __name__ == '__main__':
    switch = 0
    while True:
        if switch:
            worker()
        else:
            put_task_into_queue()
        switch ^= 1