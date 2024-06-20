tools=[
    {
            'name':'createfile',
            'description':'create a new file with the specified name.',
            'input_schema':{
                'type':'object',
                'properties':{
                    'name':{
                        'type':'string',
                        'description':'name of the new file you wish to make'
            }
        },
        'required':['name'],
        }
    },
    {
            'name':'readfile',
            'description': 'read a portion of the file, with line numbers added in.',
            'input_schema':{
                'type':'object',
                'properties':{
                    'name':{
                        'type':'string',
                        'description':'name of the file you want to read'
                    },
                    'firstline':{
                        'type':'integer',
                        'description':'the first line to read.'
                    },
                    'lastline':{
                        'type':'integer',
                        'description':'the last line to read.'
                    }
                },
                'required':['name', 'firstline', 'lastline'],
            }
    },
    {
            'name':'removefile',
            'description':'deletes a file',
            'input_schema':{
                'type':'object',
                'properties':{
                    'name':{
                        'type':'string',
                        'description':'name of the file to delete'
                    }
                },
                'required':['name'],
            }
    },
    {
            'name':'insertlines',
            'description':'inserts new lines into a file, at a specified line',
            'input_schema':{
                'type':'object',
                'properties':{
                    'name':{
                        'type':'string',
                        'description':'name of the file you want to edit'
                    },
                    'firstline':{
                        'type':'integer',
                        'description':'at what line to insert the text.'
                    },
                    'text':{
                        'type':'string',
                        'description': 'the text to insert into the file.'
                    }
                },
                'required':['name', 'firstline', 'text']
            }
    },
    {
            'name':'replaceline',
            'description':'replaces a single line in a file',
            'input_schema':{
                'type':'object',
                'properties':{
                    'name':{
                        'type':'string',
                        'description':'name of the file which you will modify'
                    },
                    'line':{
                        'type':'integer', 
                        'description':'the line number of the line you will replace.'
                    },
                    'text':{
                        'type':'string',
                        'description':'the text that will replace the line'
                    }
                },
                'required':['name', 'line', 'text']
            }
    },
    {
            'name':'removelines',
            'description':'removes some lines from a file',
            'input_schema':{
                'type':'object',
                'properties':{
                    'name':{
                        'type':'string',
                        'description':'the name of the file'
                    },
                    'firstline':{
                        'type':'integer',
                        'description':'the first line to remove'
                    },
                    'lastline':{
                        'type':'integer',
                        'description':'the last line to remove'
                    }
                },
                'required':['name', 'firstline', 'lastline']
            }
    }
        
]
