import time
import random

class External:
    @staticmethod
    def foo(request):
        # For demonstration purpose, it will randomly return one of the three possible responses
        responses = [
            {'result': 'success', 'response': 'some data'},
            {'result': 'ValidationError', 'response': 'request error'},
            {'result': 'InternalError', 'response': 'retry again'}
        ]
        # return responses[2]
        return random.choice(responses)
    

# function that will implement a retry with exponential backoff strategy
def retry_external_service(request, retry_strategy):

    max_retries = retry_strategy['max_retries']
    initial_backoff = retry_strategy['initial_backoff']
    backoff_multiplier = retry_strategy['backoff_multiplier']

    for attempt in range(max_retries + 1):
        response = External.foo(request)
        if response['result'] == 'success':
            return response
        elif response['result'] == 'ValidationError':
            return response
        elif response['result'] == 'InternalError':
            if attempt < max_retries:
                backoff_time = initial_backoff * (backoff_multiplier ** attempt)
                print(f"Internal error, retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                raise Exception("All retries failed")
        else:
            raise Exception("Unknown response from External.foo service")
        

retry_strategy = {
    'max_retries': 5,
    'initial_backoff': 1, 
    'backoff_multiplier': 2
}

request = {'some': 'data'}
response = retry_external_service(request, retry_strategy)
print(response)