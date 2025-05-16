# Steps

- ensure you installed the azure function tools: <https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp>
- Initiate a new azure function project using the cli: `func init` and follow the prompts as 'python'
- Create a new function by `func new` then specify http trigger as the trigger, and follow the prompts, use anonymous authentication.

```bash
func new
Select a number for template:
1. Blob trigger
2. CosmosDB trigger
3. Dapr Publish Output Binding
4. Dapr Service Invocation Trigger
5. Dapr Topic Trigger
6. Blob trigger (using EventGrid source)
7. EventGrid trigger
8. EventHub trigger
9. HTTP trigger
10. Queue trigger
11. ServiceBus Queue trigger
12. ServiceBus Topic trigger
13. Timer Trigger
Choose option: 9
Function Name: [http_trigger] eraki_http_local-func
Function Name is not valid.
Function Name: [http_trigger] eraki-http-local-func
Function Name is not valid.
Function Name: [http_trigger] localHTTPfunc
Select a number for Auth Level:
1. FUNCTION
2. ANONYMOUS
3. ADMIN
Choose option: 2
Appending to /home/eraki/Documents/gitReposPersonal/azure-functions/01-local_function/function_app.py
The function "localHTTPfunc" was created successfully from the "HTTP trigger" template.
```

- once you are ready run the function using `func start` and navigate to the URL output.
- Parse the URL with your name: `http://localhost:7071/api/localHTTPfunc?name=mohamed+eraki`
