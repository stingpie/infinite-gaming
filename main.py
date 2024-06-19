import toolcalls, tooljson, pickle, os
from openai import OpenAI as openai

client = openai()


if(not os.path.exists("sandbox")):
    os.makedirs("sandbox")


if(os.path.exists("chatlog.pkl")):
    log = pickle.load(open("chatlog.pkl", 'rb'))
else:
    log = [{"role":"system","content":open("prompt.txt",'r').read()}]


feedback =input("how would you improve this game?")


stop_reason=""
done=False
count=0
limit=25

log.append({"role":"user", "content": feedback })

while(stop_reason!="content_filter" and not done and count<limit):
    completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=log,
            tools = tooljson.tools,
            tool_choice="required"
    )
    response_message = completion.choices[0].message
    
    log.append(response_message)
    

    tool_calls = response_message.tool_calls
    for i in range(len(tool_calls)):
    
        tool_call_id = tool_calls[i].id
        func_name = tool_calls[i].function.name
        # eval creates a dictionary, since the arguments are formatted as such.
        arguments = eval(tool_calls[i].function.arguments)

        if(func_name == "createfile"):
            result = toolcalls.createfile(arguments)
        elif(func_name == "readfile"):
            result = toolcalls.readfile(arguments)
        elif(func_name == "removefile"):
            result = toolcalls.removefile(arguments)
        elif(func_name == "removelines"):
            result = toolcalls.removelines(arguments)
        elif(func_name == "insertlines"):
            result = toolcalls.insertlines(arguments)
            if(arguments['name'] == "changelog.txt"):
                done=True
                
        elif(func_name == "replaceline"):
            result = toolcalls.replaceline(arguments)
        else:
            toolcalls.log_err("function "+func_name+" does not exist.")

        log.append({'role':'tool', 'content':result, 'tool_call_id':tool_call_id, 'name':func_name})

    count+=1
  
    print(log)
    
    with open('chatlog.pkl','wb') as f:
        pickle.dump( log, f)
    stop_reason = completion.choices[0].finish_reason
    


