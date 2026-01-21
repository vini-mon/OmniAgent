# This is the main file that runs the main program. It asks a question to the AI, allows it to use tools, and shows the final result.

# Import necessary modules from langchain
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

# Import the function to get the LLM with tools integrated module
from agents.general_agent import get_llm_with_tools

# Some example queries to try:
query_list_examples = [

    "1 + 2 - 3 + 4 - 5",
    "0 + 0.5 + 1.0 * 3",
    "2 + 3 + 5 * 2 / 0",
    "Calculate the addition of 15 and 27, then multiply the result by 3.",
    "What is the result of adding 100 and 250, and then multiplying that sum by 4?",
    "1 * 250, and then sum 4 to the result, finally multiply everything by 2.",
    "What is Star Wars?",
    "Who was Doctor Who?",
    "The answer to life, the universe, and everything...",
    "Tell me a random fact about cats."

]

def get_user_query():
    """
        Function to get the user query, either from a predefined list or manual input.
    """

    print("\n** Select a Query or Type Your Own **\n")

    print("0. Type your own query manually")

    for i, example in enumerate(query_list_examples, 1):
        print(f"{i}. {example}")
    
    choice = input("\n> Enter number: ").strip()
    
    # If a valid number from the list was chosen
    if choice.isdigit():

        idx = int( choice )

        if 1 <= idx <= len(query_list_examples):

            return query_list_examples[idx - 1]
        
        elif idx == 0:

            print(">> Selected Manual Input mode.")
            return input(">> Type your query here: ")
        
        else:

            print(">> Invalid choice. Quitting the program. Bye bye :)\n\n")
            exit(0)
    

def main():

    # Start the OmniAgent with Local LLM and Tools
    print("\n>- Starting the OmniAgent with Local LLM and Tools\n")

    llm, tools_list = get_llm_with_tools()

    # Mapping tool names for reference
    tools_map = { t.name: t for t in tools_list }

    # Forcing sequential tool use (one at a time)
    system_instruction = """
    You are a math assistant equipped with tools and a personality.

    AVAILABLE TOOLS:
    - `add(a, b)`: Sum of a and b.
    - `sub(a, b)`: Subtraction (a - b).
    - `mul(a, b)`: Multiplication.
    - `divide(a, b)`: Division.
    - `get_random_cat_fact()`: Returns a random fact about cats. No arguments needed. This is your final answer when the user requests a cat fact.

    GENERAL HANDLING:
    - For math: USE TOOLS.
    - For cat facts: If the user asks for cat facts, use `get_random_cat_fact`. When the tool returns a fact, you MUST repeat the fact in your final answer. Do not just comment on it.
    - For general chat: Answer naturally, but be concise.
    
    CRITICAL PROTOCOL:
    1. You must use the provided tools for ANY calculation.
    2. When you receive a result from a tool (e.g., 42), check if there are more steps.
    3. If there is a next step, you MUST generate a NEW tool call immediately.
    4. DO NOT write "Now I will..." or "The result is...". Just trigger the tool.
    5. STRICTLY FORBIDDEN: Never simulate the "Tool Output". Never write the number yourself unless it is the final answer after all calculations.

    DECISION PROTOCOL:

    **CATS QUERIES**:
        - If the user asks for a cat fact, you MUST use the `get_random_cat_fact` tool.
        - Do not try to answer cat fact queries yourself.
        - When the tool returns a fact, you MUST REPEAT that fact in your final answer to the user. Not adding anything else.

    **ATOMIC ARGUMENTS**:
        - Tools accept ONLY plain numbers (e.g., 10, 3.5).
        - NEVER pass expressions or formulas as arguments (e.g., do NOT pass "(9 + 1)" or "5 * 2").
        - If you see parentheses `(a + b)`, you MUST call the appropriate tool to solve `a + b` FIRST. Use the result for the next step.

    **RESPECT PEMDAS**: You MUST follow the Order of Operations:
        - 1st: Parentheses
        - 2nd: Exponents
        - 3rd: Multiplication and Division (from left to right)
        - 4th: Addition and Subtraction (from left to right)

    **MATHEMATICAL QUERIES**:
        - If the query involves calculations, you MUST use the provided tools.
        - Perform ONE step at a time (sequential execution).
        - NEVER calculate mentally. ALWAYS rely on the tools.
        - After receiving a tool result, immediately call the next tool if needed.
        - If the tool output answers the user's question completely, STOP. Do not invent extra steps (like dividing by 1 or adding 0). Just output the final result.

    **SEQUENTIAL EXECUTION**:
        - Do one step at a time.
        - Wait for the tool output before deciding the next step.
        - If a tool returns an error, try to fix the argument and call it again.

    **GENERAL KNOWLEDGE**:
        - If the query is NOT mathematical OR about cats (e.g., "What is Star Wars?", "Write a poem"), answer directly using your internal knowledge.
        - DO NOT try to use tools for these questions.
        - Just provide a helpful and natural response.

    **OUTPUT RULES**:
        - Do NOT use LaTeX formatting (like \boxed{}).
        - Be concise and direct.
        - If you have the final number, just say: "The answer is: [number]".
       
    SPECIAL BEHAVIOR (EASTER EGGS):
        - If the user asks about "the answer to life...", respond DIRECTLY without using tools. Text: "The answer is 42. But do you know what the question is?"
        - If the user asks "What is the Matrix?", respond: "The Matrix is everywhere. It is all around us."
    """

    # Example queries for the user to choose
    query = get_user_query()
    print(f"\n>- User Query: {query}\n")

    print(">> (The answer may take a few moments to appear due to local LLM processing)\n")

    # Using HumanMessage to send the query
    messages = [

        SystemMessage( content = system_instruction ),  # System instructions to guide the LLM
        HumanMessage( content = query ),                # User query
    
    ]

    # The Execution Loop (Reason -> Act -> Reason...)
    while True:

        # Ask the LLM to process the messages, based on the history
        try:
            ai_msg = llm.invoke(messages)

        except Exception as e:

            print(f"ERROR: Invoking LLM: {e}")
            break

        # Forcing sequential tool calls: if more than one tool call is requested, keep only the first
        if ai_msg.tool_calls and len(ai_msg.tool_calls) > 1:

            print(f">- [SYSTEM NOTICE] Agent tried parallel calls. Forcing sequential execution.\n")

            # Keep only the first tool call
            ai_msg.tool_calls = [ai_msg.tool_calls[0]]
        
        messages.append( ai_msg )

        # The LLM asked to use a tool?
        if ai_msg.tool_calls:

            print(f">- [AI DECISION] Tool Call: {ai_msg.tool_calls[0]['name']}")

            # Passing through all tool calls requested by the LLM
            for tool_call in ai_msg.tool_calls:

                selected_tool_name = tool_call["name"]
                selected_tool_args = tool_call["args"]

                print(f">- [TOOL CALL] Tool selected: {selected_tool_name} with arguments {selected_tool_args}")

                if selected_tool_name in tools_map:

                    try:

                        tool_func = tools_map[ selected_tool_name ]
                        tool_result = tool_func.invoke( selected_tool_args )

                        print(f">> Tool Output: {tool_result}\n")

                        # Message that represents the tool output
                        tool_msg = ToolMessage(

                            content = str( tool_result ),
                            tool_call_id = tool_call["id"],
                            name = selected_tool_name

                        )

                        messages.append( tool_msg )

                    except Exception as e:

                        print(f">>> [TOOL ERROR] An error occurred while using the tool: {e}\n")

                        error_msg = ToolMessage(

                            content = f"Error using tool {selected_tool_name}: {e}",
                            tool_call_id = tool_call["id"],
                            name = selected_tool_name
                        
                        )

                        messages.append( error_msg )

                else:
                    print(f"ERROR: Tool {selected_tool_name} not found.")

        else:

            print(f"\n>- [Final Answer]: {ai_msg.content}")
            break

if __name__ == "__main__":
    main()