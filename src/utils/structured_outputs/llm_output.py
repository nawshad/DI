'''
Here we will write the pydantic classes
for structured output using llms.
'''


zeroshot_triple_schema={
    'triples': [{
            'subject': 'subject name',
            'relationship': 'relationship name between subject and object',
            'object': 'object name',
        }]
}