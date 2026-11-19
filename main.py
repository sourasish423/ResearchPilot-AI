from ollama import chat
from calculator import add, multiply
from web_tools import web_search
from web_reader import read_webpage

# Define available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "web_search",#tells Llama the tool's name.
            "description": "Search the internet for a user's research question. Use this tool first for factual research. Returns search results containing titles, URLs and snippets. Never invent URLs.",#tells Llama when this tool is useful.
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {#the argument the function expects.
                        "type": "string",#the search query must be text.
                        "description": "The topic or question to search for"#Llama must provide a query.
                    }
                },
                "required": ["query"]
            }
        }
    },

        

]
user_query = input("What would you like to research? ")

messages = [
    {
        "role": "system",
        "content": (
            "You are a research assistant. Use the retrieved webpage "
            "content to answer the user's question. Consider all available "
            "sources, include their URLs as citations, distinguish "
            "conflicting information, and never invent facts or URLs. "
            "If the sources do not support an answer, say so."
        )
    },
    {
        "role": "user",
        "content": user_query
    }
]

response = chat(
    model="llama3.2",
    messages=messages,
    tools=tools
)


available_tools={
    "add":add,
    "multiply":multiply,
    "web_search": web_search,
    

}


def execute_tool(tool_call):
    function_name = tool_call.function.name #getting the function name from llm which it wants to execute
    
     # Validate function name
    if function_name not in available_tools:
        raise ValueError(
            f"Unknown tool: {function_name}"
        )
    
    arguments = tool_call.function.arguments #getting the arguments which needs to be passed to python for execution
    function = available_tools[function_name]#getting the fn name
    if function_name in ["add", "multiply"]:
        arguments = {
        key: int(value) if isinstance(value, str) else value
        for key, value in arguments.items()
        }
    
    
    result = function(**arguments)

    return result
    





#execute each requested tool
search_failed = False
while response.message.tool_calls:#Check whether Llama has requested a tool.

    messages.append(response.message)

    for tool_call in response.message.tool_calls:

        print("Tool requested:", tool_call.function.name)
        print("Arguments:", tool_call.function.arguments)

        result = execute_tool(tool_call)
        print("Actual search result:", result)
        
        if tool_call.function.name == "web_search":
            if not result or "error" in result[0]:
                print("No search results found. Please try another query.")
                search_failed = True
                break

        messages.append({
            "role": "tool",
            "tool_name": tool_call.function.name,
            "content": str(result)
        })

        if tool_call.function.name == "web_search":
            sources_read=0
            for search_result in result:
                if sources_read == 3:
                    break
                article_url=search_result.get("href")
                article_title=search_result.get("title","untitled source")#"Untitled source", is a default value.If DDGS doesn't provide a title, Python uses that default instead.

                if not article_url:
                    continue
                print("\nReading webpage:", article_title)
                print("URL:", article_url)
#Without error handling, a failure on Source 2 could stop the entire program.
                try:
                    page_content=read_webpage(article_url)
                
                except Exception as e:
                    print(f"Unable to read webpage: {e}")
                    continue

                if not page_content.strip():
                    print("No readable content. Skipping this source.")
                    continue #his prevents empty webpage content from being treated as useful research evidence.
                
                messages.append({
                     "role": "tool",
                     "tool_name": "read_webpage",
                     "content": (
                     f"Source: {article_title}\n"
                     f"URL: {article_url}\n\n"
                     f"{page_content}"
                     )

                     })
                sources_read += 1
            

    if search_failed:
        break

            
    response = chat(
    model="llama3.2",
    messages=messages,
    tools=tools
    )

if not search_failed:
    print(response.message.content)


# function_name = "multiply"

# function = available_tools[function_name]

# result = function(100, 50)

# print(result)
#.venv\Scripts\activate