import os, subprocess, shlex, Queue, time
import lorun

from config import JUDGE_RESULT,PRB_FOLDER,JUDGE_FOLDER, PYTHON_TIME_LIMIT_TIMES, PYTHON_MEMORY_LIMIT_TIMES, QUEUE_SIZE, WAIT_TIME
from models import Problem, Submit, User
from App import db


Q = Queue.Queue(QUEUE_SIZE)

def rm_tmp_file(runid):
	os.system(' '.join(['rm', os.path.join(JUDGE_FOLDER, str(runid))]))

def put_task_into_queue():
	while Q.empty():
		Q.join() 
		data = Submit.query.filter_by(result = 'Pending').order_by(Submit.runid).all()
		for submit in data:
			task = {
			'runid' : submit.runid,
			'pbid': submit.pbid,
			'userid' : submit.userid,
			'language' : submit.language
			}
			# print submit.runid
			Q.put(task)
			# print Q.qsize(), QUEUE_SIZE
			if(Q.qsize() == QUEUE_SIZE):
				break
		if(Q.qsize == QUEUE_SIZE):
				break
	# print 'test'
	time.sleep(WAIT_TIME) 

def worker():
    while not Q.empty():
        task = Q.get()  

        runid = task['runid']
        pbid = task['pbid']
        language = task['language']
        userid = task['userid']

        # print runid

        Submit.query.filter_by(runid = runid).update({'result': 'Runing'})
        result, rst = Judge(runid, pbid, language)
        print pbid,result, rst
        problem = Problem.query.get(pbid)
        user = User.query.get(userid)
        if result == 'Accepted':
            Submit.query.filter_by(runid = runid).update({'result': result})
            problem.accnt += 1
            user.accnt += 1
        else:
            Submit.query.filter_by(runid = runid).update({'result': result})

        # dblock.acquire()
        # update_result(result) 
        # dblock.release()
        problem.submitcnt += 1
        problem.ratio = problem.accnt * 1.0 / problem.submitcnt
        user.submission += 1
        db.session.commit()

        Q.task_done()
        rm_tmp_file(runid)
        


def Store_code(runid, name):
	f = open(os.path.join(JUDGE_FOLDER, name), 'w')
	f.write(Submit.query.get(runid).code)
	f.close()

def compile(runid, language):
	build_cmd = {
	'G++' : 'g++ main.cpp -o main -O2 -Wall -lm  -DONLINE_JUDGE',
	'C' : 'gcc main.c -o main -Wall -lm -O2 -std=c99 -DONLINE_JUDGE',
	'C++' : 'c++ main.cpp -o main -O2 -Wall -lm -DONLINE_JUDGE',
	'Python2.7' : 'python2.7 -m py_compile main.py'
	}
	p = subprocess.Popen(build_cmd[language], shell=True, cwd=JUDGE_FOLDER, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output,err =  p.communicate()
	if p.returncode == 0:
		return True
	else:
		error = u' '.join([output,err])
		Submit.query.filter_by(runid = runid).update({'CEmsg': error})
		db.session.commit()
		return False
    # dblock.acquire()
    # update_compile_info(solution_id,err+out) 
    # dblock.release()


def Judge(runid, pbid, language):
    name = {
    'G++' : 'main.cpp',
    'C' : 'main.c',
    'C++' : 'main.cpp',
    'Python2.7' : 'main.py'
    }
    Store_code(runid, name[language])
    inputfile = open(os.path.join(PRB_FOLDER, str(pbid)+'.in' ))
    outputfile = open(os.path.join(PRB_FOLDER, str(pbid)+'.out'))
    tmpfile = open(os.path.join(JUDGE_FOLDER, str(runid)), 'w')
    timelmt = Problem.query.get(pbid).timelmt
    memorylmt = Problem.query.get(pbid).memorylmt

    if not compile(runid, language):
        return (JUDGE_RESULT[7], None)
    if language == 'Python2.7':
        timelmt *= PYTHON_TIME_LIMIT_TIMES
        memorylmt *= PYTHON_MEMORY_LIMIT_TIMES
        cmd = 'python2.7 %s' % (os.path.join(JUDGE_FOLDER, 'main.pyc'))
        main_exe = shlex.split(cmd)
    else:
        main_exe = [os.path.join(JUDGE_FOLDER, 'main'), ]

    runcfg = {
    'args': main_exe,
    'fd_in': inputfile.fileno(),
    'fd_out': tmpfile.fileno(),
    'timelimit': timelmt,
    'memorylimit': memorylmt
    }
    rst = lorun.run(runcfg)
    inputfile.close()
    tmpfile.close()
    tmpfile = open(os.path.join(JUDGE_FOLDER, str(runid)))

    #return ('Accepted', None)
    if rst['result'] == 0:
        crst = lorun.check(outputfile.fileno(), tmpfile.fileno())
#        #lorun.check() returns a number which means the final result
        outputfile.close()
        tmpfile.close()
        rst['result'] = crst
    return JUDGE_RESULT[rst['result']],rst
