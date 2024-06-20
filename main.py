import toolcalls, pickle, os


api="ant"

if(api == "openai"):
    from openai import OpenAI as openai
    import tooljson_openai as tooljson

    client = openai()
elif(api == 'ant'):
    from anthropic import Anthropic as anthropic
    import tooljson_ant as tooljson

    client = anthropic()


if(not os.path.exists("sandbox")):
    os.makedirs("sandbox")


if(os.path.exists("chatlog.pkl")):
    log = pickle.load(open("chatlog.pkl", 'rb'))
else:
    if(api == "openai"):
        log = [{"role":"system","content":open("prompt.txt",'r').read()}]
    else:
        log =[]

feedback =input("how would you improve this game?")


stop_reason=""
done=False
count=0
limit=25

if(api == 'openai'):
    log.append({"role":"user", "content": feedback })
elif(api == 'ant'):
    if os.path.exists("chatlog.pkl"):
        log[-1]['content'].append({'type':'text', 'text':feedback})
    else:
        log.append({'role':'user','content':feedback})


while(stop_reason!="content_filter" and not done and count<limit):
    

    if(api =='openai'):
        completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo',
                messages = log,
                tools = tooljson.tools,
                tool_choice = 'required'
        )
        response_message = completion.choices[0].message
    elif(api =='ant'):
        completion = client.messages.create(
                model='claude-3-5-sonnet-20240620',
                max_tokens=4096,
                system=open("prompt.txt",'r').read(),
                messages=log,
                tools = tooljson.tools,
                tool_choice={'type':'any'}
        )
        response_message = completion

    #response_message = completion.choices[0].message
    if api == 'openai':
        log.append(response_message)
    elif api == 'ant':
        log.append({'role':'assistant','content':response_message.content})
    

    if(api == 'openai'):
        tool_calls = response_message.tool_calls
    elif(api == 'ant'):
        tool_calls = response_message.content
        tool_content=[]


    for i in range(len(tool_calls)):
    
        tool_call_id = tool_calls[i].id
        func_name = tool_calls[i].function.name if(api == 'openai') else tool_calls[i].name
        # eval creates a dictionary, since the arguments are formatted as such.
        arguments = eval(tool_calls[i].function.arguments) if(api == 'openai') else tool_calls[i].input

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

        if(api == 'openai'):
            log.append({'role':'tool', 'content':result, 'tool_call_id':tool_call_id, 'name':func_name})
        elif(api == 'ant'):
            tool_content.append({'type':'tool_result', 'tool_use_id':tool_call_id, 'content':result})
    if(api == 'ant'):
        log.append({'role':'user', 'content':tool_content})


    count+=1
  
    print(response_message)
    
    with open('chatlog.pkl','wb') as f:
        pickle.dump( log, f)

    if(api == 'openai'):
        stop_reason = completion.choices[0].finish_reason
    elif(api == 'ant'):
        stop_reason= completion.stop_reason


