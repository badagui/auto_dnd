from openai import AsyncOpenAI
import tiktoken

class GPTController:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def send_query(self, messages, tools_prompt, tool_choice=None):
        model = "gpt-3.5-turbo-0125"
        # model = "gpt-4-turbo-preview"
        pricing = {
            "gpt-3.5-turbo-0125": [0.0005, 0.0015],
            "gpt-4-turbo-preview": [0.01, 0.03]
        }
        price = [pricing[model][0] if model in pricing else 0, 
            pricing[model][1] if model in pricing else 0]
        try:
            completion = await self.client.chat.completions.create(
                model = model,
                messages=messages,
                tools = tools_prompt,
                tool_choice = tool_choice
            )
            print('completion id ', completion.id)
            print('usage ', completion.usage)
            in_cents = completion.usage.prompt_tokens * price[0] / 1000 * 100
            print('in cents ', in_cents)
            out_cents = completion.usage.completion_tokens * price[1] / 1000 * 100
            print('out cents ', out_cents)
            return {'message': completion.choices[0].message, 'cost': in_cents + out_cents}
        except Exception as e:
            print('exception send query', e)
    
    async def send_img_query(self, prompt):
        price = 0.04 # per image
        try:
            response = await self.client.images.generate(
                model = "dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return {'url': response.data[0].url, 'cost': price}
        except Exception as e:
            print('exception send img query', e)

def preview_tokens_cost(messages, tools_prompt):
    message_tokens = count_messages_tokens(messages)
    tools_tokens = count_tools_tokens(tools_prompt)
    total_tokens = message_tokens + tools_tokens
    # print('message tokens: ', message_tokens)
    # print('tools tokens: ', tools_tokens)
    # print('total tokens: ', total_tokens)
    # print('cents: ', total_tokens * 0.01 / 1000 * 100)
    return total_tokens

def count_messages_tokens(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    token_count = 0
    prefix_tokens = 3
    for message in messages:
        token_count += prefix_tokens
        for k, v in message.items():
            if v == None: 
                continue
            if k == 'tool_calls': 
                token_count += 20 * len(v) # aprox. token count for a tool use
                continue
            token_count += len(encoding.encode(v))
    token_count += prefix_tokens # reply prefix
    return token_count

def count_tools_tokens(tools):
        encoding = tiktoken.get_encoding("cl100k_base")
        token_count = 0
        tool_tokens = 7
        prop_tokens = 3
        ending_tokens = 12
        for tool in tools:
            token_count += tool_tokens
            tool_name = tool['function']['name']
            tool_desc = tool['function']['description']
            if tool_desc.endswith("."):
                tool_desc = tool_desc[:-1]
            line = tool_name + ":" + tool_desc
            token_count += len(encoding.encode(line))
            if len(tool['function']['parameters']['properties']) > 0:
                token_count += prop_tokens
                for key in list(tool['function']['parameters']['properties'].keys()):
                    token_count += prop_tokens
                    p_name = key
                    p_type = tool['function']['parameters']['properties'][key]['type']
                    p_desc = tool['function']['parameters']['properties'][key]['description']
                    if "enum" in tool['function']['parameters']['properties'][key].keys():
                        token_count += prop_tokens
                        for item in tool['function']['parameters']['properties'][key]['enum']:
                            token_count += prop_tokens
                            token_count += len(encoding.encode(item))
                    if p_desc.endswith("."):
                        p_desc = p_desc[:-1]
                    line = f"{p_name}:{p_type}:{p_desc}"
                    token_count += len(encoding.encode(line))
        token_count += ending_tokens
        return token_count
