import os


def in_directory(file, directory):
    #make both absolute
    directory = os.path.join(os.path.realpath(directory), ' ')
    file = os.path.realpath(file)

    return os.path.commonprefix([file, directory]) == directory

def in_sandbox(file):
    return True #TODO: figure out why this doesn't work.
    return in_directory(os.path.join("sandbox", file), "sandbox")

def log_err(error):
    with open("err_log",'w+', encoding="utf-8") as f:
        f.write(error+"\n")



def createfile(args):

    if(in_sandbox(args["name"])):
        # if the request is to make a file in a non existent sub-directory
        if(not os.path.exists(os.path.split(os.path.join("sandbox",args['name']))[0])):
            os.makedirs(os.path.split(os.path.join("sandbox",args['name']))[0], exist_ok=True)
        if(os.path.exists(os.path.join("sandbox", args["name"]))):
            log_err("Tried to make new file with existing name \""+args["name"]+"\"\n")
            return "ERROR! file already exists!"
        f = open(os.path.join("sandbox",args["name"]), mode='x', encoding="utf-8")
        f.close()
        return "File created succesfuly. It is currently empty."
    else:
        log_err("tried to create file \""+args["name"]+"\"\n")
        return "Error! file outside of bounds!"

def readfile(args):
    if(in_sandbox(args["name"])):
        if(not os.path.exists(os.path.join("sandbox", args["name"]))):
            log_err("tried to read non-existent file \""+args["name"]+"\"\n")
            return "ERROR! File does not exist."

        filetext="LINE\t|TEXT"
        
        with  open(os.path.join("sandbox",args["name"]), mode='r', encoding='utf-8') as f:
            lines_to_read = f.read().split("\n")
            for lines in range(max(0,args["firstline"]), min(args["lastline"], len(lines_to_read))):
                filetext+="\n"+str(lines)+"\t|"+lines_to_read[lines]
        return filetext
    else:
        log_err("tried to read out-of-bounds file \""+args["name"]+"\"\n")
        return "ERROR! File out of bounds."


def removefile(args):
    if(os.path.exists(os.path.join('sandbox',args["name"]))):
        os.remove(args["name"])
        return "File removed succesfully."
    else:
        log_err("tried to remove non-existent file \""+args['name']+"\"\n")
        return "ERROR! file does not exist."

def insertlines(args):

    if(in_sandbox(args["name"])):
        with open(os.path.join("sandbox",args["name"]), "r") as f:
            lines = f.read().split("\n")
            line_len = len(lines)
            lines = "\n".join(lines[:args["firstline"]]+[args["text"]]+lines[args["firstline"]:])
        with open(os.path.join("sandbox", args["name"]), "w") as f:
            f.write(lines)

        return "Lines inserted successfully. Area now looks like:\n"+readfile({'name':args['name'], 'firstline':args['firstline']-5, 'lastline':args['firstline']+line_len+5})
    log_err("Tried to insert lines into \""+args['name']+"\"\n")
    return "ERROR! file out of bounds!"


def replaceline(args):

    if(in_sandbox(args["name"])):
        if(not os.path.exists(os.path.join("sandbox", args["name"]))):
            log_err("tried to replace line in non-existent file \""+args["name"]+"\"\n")
            return "ERROR! File does not exist."
        with open(os.path.join("sandbox",args["name"]), 'r') as f:
            lines = f.read().split("\n")
        lines[args["line"]] = args["text"]
        with open(os.path.join("sandbox", args["name"]), 'w') as f:
            f.write("\n".join(lines))

        return "Line succesfully replaced. New line:\n" + readfile({'name':args['name'], 'firstline':args['line']-5, 'lastline':args['line']+5})

def removelines(args):

    if(in_sandbox(args["name"])):
        if(not os.path.exists(os.path.join("sandbox", args["name"]))):
            log_err("Tried to remove lines from \""+args['name']+"\"\n")
            return "ERROR! file does not exist."
        with open(os.path.join("sandbox", args["name"]), 'r') as f:
            lines = f.read().split("\n")
        lines = lines[:args['firstline']] + lines[args['lastline']:]
        
        with open(os.path.join("sandbox", args["name"]), 'w') as f:
        
            f.write("\n".join(lines))
        return "Succesfully removed lines. Area now looks like:\n"+readfile({'name':args['name'], 'firstline':args['firstline']-5, 'lastline':args['firstline']+5})
    log_err("Tried to remove lines out of \""+args['name']+"\"\n")
    return "ERROR! file out of bounds."

def runlisp(args):
    
    if(in_sandbox(args['name'])):
        if(not os.path.exists(os.path.join('sandbox', args['name']))):
            log_err("Tried to run file \""+args['name']+"\"\n")
            return "ERROR! File does not exist."
        return os.system("sbcl --script "+args['name'])
    log_err("Tried to run file \""+args['name']+"\"\n")
    return "ERROR! File out of bounds."



