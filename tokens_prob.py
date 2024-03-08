import os
import re

import numpy as np
import panel as pn
import tastymap as tm
from openai import AsyncOpenAI
import os

os.environ["OPENAI_API_KEY"] = "sk-..."

pn.extension()

# COLORMAP = "viridis_r"
COLORMAP = "cool"
COLORMAP_REVERSE = False
NUM_COLORS = 10
# SYSTEM_PROMPT = """
# Based on the text, classify as one of these options:
# - Feature
# - Bug
# - Docs
# Answer in one word; no other options are allowed.
# """.strip()
SYSTEM_PROMPT = """
""".strip()
TOP_LOGPROBS = 5
def color_by_logprob(text, log_prob):
    linear_prob = np.round(np.exp(log_prob) * 100, 2)
    # select index based on probability
    color_index = int(linear_prob // (100 / (len(colors) - 1)))

    # Generate HTML output with the chosen color
    if "'" in text:
        # html_output = f'<span style="text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;color: {colors[color_index]}">{text}</span>'
        html_output = f'<span style="color: {colors[color_index]}"><b>{text}</span>'

    else:
        # html_output = f"<span style='text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;color: {colors[color_index]}'>{text}</span>"
        html_output = f"<span style='color: {colors[color_index]}'><b>{text}</span>"

    return html_output


def custom_serializer(content):
    pattern = r"<span.*?>(.*?)</span>"
    matches = re.findall(pattern, content)
    if not matches:
        return content
    return matches[0]
pss = []

async def respond_to_input(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        aclient.api_key = api_key_input.value
    elif not os.environ["OPENAI_API_KEY"]:
        instance.send("Please provide an OpenAI API key", respond=False, user="ChatGPT")

    # add system prompt
    if system_input.value:
        system_message = {"role": "system", "content": system_input.value}
        messages = [system_message]
    else:
        messages = []

    # gather messages for memory
    if memory_toggle.value:
        messages += instance.serialize(custom_serializer=custom_serializer)
    else:
        messages.append({"role": "user", "content": contents})

    # call API
    response = await aclient.chat.completions.create(
        model=model_selector.value,
        messages=messages,
        top_logprobs=TOP_LOGPROBS,
        stream=True,
        logprobs=True,
        temperature=temperature_input.value,
        max_tokens=max_tokens_input.value,
        seed=seed_input.value,
    )

    # stream response
    message = ""
    cosa = """<br><strong><p style="color:dark-blue">"""
    async for chunk in response:
        
        choice = chunk.choices[0]
        ps=[]
        try:
            ps = [(x.token,np.round(np.exp(x.logprob) * 100, 2)) 
                  for x in chunk.choices[0].logprobs.content[0].top_logprobs]
            print(ps)
        except:
            pass
        # pss.append(ps)
        content = choice.delta.content
        log_probs = choice.logprobs
        
        if content and log_probs:
            log_prob = log_probs.content[0].logprob
            message += color_by_logprob(content, log_prob) 
            message += "&nbsp;"*(20-len(content))+ str(dict(ps)) + "<br>"
            cosa += content
            yield message + cosa+"</strong>"
    print("--*--*"*15)

tmap = tm.cook_tmap(COLORMAP, NUM_COLORS, COLORMAP_REVERSE)
colors = tmap.to_model("hex")

aclient = AsyncOpenAI()
api_key_input = pn.widgets.PasswordInput(
    name="OpenAi API Key",
    placeholder="sk-...",
    width=150,
)
system_input = pn.widgets.TextAreaInput(
    name="System Prompt",
    value=SYSTEM_PROMPT,
    rows=2,
    auto_grow=True,
)
model_selector = pn.widgets.Select(
    name="Model Selector",
    options=["gpt-3.5-turbo", "gpt-4"],
    width=150,
)
temperature_input = pn.widgets.FloatInput(
    name="Temperature", start=0, end=2, step=0.01, value=1, width=100
)
MAX_TOKENS = 20
max_tokens_input = pn.widgets.IntInput(name="Max Tokens", start=0, value=MAX_TOKENS, width=100)
seed_input = pn.widgets.IntInput(name="Seed", start=0, end=100, value=0, width=100)
memory_toggle = pn.widgets.Toggle(
    name="Include Memory", value=False,margin=(10, 5)
)
chat_interface = pn.chat.ChatInterface(
    callback=respond_to_input,
    callback_user="ChatGPT",
    callback_exception="verbose",
    max_width=1300     
)

# v = pn.widgets.StaticText()
# v.value = pss
hv = """-"""
bar = f"""<div style="height: 8px;padding-left: 600px;">0%  {hv} 
        COLORMAP (Color intensity indicates token likelyhood)   
        {hv} 100%"""+re.findall("""<div class="cmap".*?</div>""", tmap._repr_html_())[0]+"""</div>"""
bar = re.sub("\" src=\"", "max-width: 400px;\" src=\"", bar)

template = pn.template.MaterialTemplate(
    title='~ToKEn viSuAl~'
    )
template.main.append(
    pn.Column(
        pn.Row(
            memory_toggle, 
            system_input,
            model_selector,
            temperature_input,
            max_tokens_input,
            seed_input,
            api_key_input,
            align="center",
        ),
        # pn.Row(v),
        pn.Row(bar, align="center"),
        chat_interface,
    ))

template.show();
