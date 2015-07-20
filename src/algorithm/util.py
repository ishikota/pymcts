from sys import stdout

def show_progress(counter, max_num):
    stdout.flush()
    stdout.write("\rthinking...(%d/%d)" % (counter+1, max_num))

def fin_progress():
    stdout.write("\r\n")
