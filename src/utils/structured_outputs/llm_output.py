'''
Here we will write the pydantic classes/dictionaries
 for structured output using llms.
'''

zeroshot_triple_schema={
    'triples': [{
            'subject': 'subject name',
            'relationship': 'relationship name between subject and object',
            'object': 'object name',
        }]
}

zeroshot_summary_schema = {
    'summary' : 'summary of the provided text in few sentences'
}