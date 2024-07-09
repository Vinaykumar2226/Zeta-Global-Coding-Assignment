import asyncio
import random

# External Service
class External:
    async def foo(self, request):
        # For demonstration purpose, it will randomly return one of the three possible responses
        responses = [
            {'result': 'success', 'response': 'some data'},
            {'result': 'validation_error', 'response': 'request error'},
            {'result': 'internal_error', 'response': 'retry again'}
        ]
        # return responses[2]
        return random.choice(responses)
    

# function that will implement a retry with exponential backoff strategy
async def retry_external_service(request, retry_strategy):
    max_retries = retry_strategy['max_retries']
    initial_backoff = retry_strategy['initial_backoff']
    backoff_multiplier = retry_strategy['backoff_multiplier']

    for attempt in range(max_retries + 1):
        external = External()
        response = await external.foo(request)
        if response['result'] == 'success':
            return response
        elif response['result'] == 'validation_error':
            return response
        elif response['result'] == 'internal_error':
            if attempt < max_retries:
                backoff_time = initial_backoff * (backoff_multiplier ** attempt)
                print(f"Internal error, retrying in {backoff_time} seconds...")
                await asyncio.sleep(backoff_time)
            else:
                raise RuntimeError("All retries failed")
        else:
            raise RuntimeError("Unknown response from External.foo service")

# main function
async def main():
    retry_strategy = {
        'max_retries': 5,
        'initial_backoff': 1,
        'backoff_multiplier': 2
    }
    request = {'any': 'request'}
    response = await retry_external_service(request, retry_strategy)
    print(response)

asyncio.run(main())