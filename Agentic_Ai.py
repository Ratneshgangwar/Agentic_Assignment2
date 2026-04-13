!pip install langchain==0.1.16 langchain-community==0.0.32 transformers wikipedia -q

import warnings
warnings.filterwarnings("ignore")

from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from transformers import pipeline
from langchain.llms import HuggingFacePipeline

# MODEL (SAFE SETTINGS)
pipe = pipeline(
    "text-generation",
    model="gpt2",
    max_new_tokens=150   # reduce output size
)

llm = HuggingFacePipeline(pipeline=pipe)

# TOOL
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [
    Tool(
        name="Wikipedia",
        func=wiki.run,
        description="Get factual information"
    )
]

# AGENT
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

# 🔥 FIXED FUNCTION (LIMIT INPUT)
def generate(topic):
    data = wiki.run(topic)

    # LIMIT DATA SIZE (IMPORTANT)
    data = data[:500]   # 👈 THIS FIXES ERROR

    prompt = f"""
    Topic: {topic}

    Explain clearly:
    {data}
    """

    return pipe(prompt)[0]["generated_text"]

# OUTPUTS
out1 = generate("Machine Learning in Healthcare")
out2 = generate("AI in Smart Education")

print("OUTPUT 1:\n", out1)
print("\nOUTPUT 2:\n", out2)

# SAVE
with open("out1.txt","w") as f:
    f.write(out1)

with open("out2.txt","w") as f:
    f.write(out2)

# DOWNLOAD
from google.colab import files
files.download("out1.txt")
files.download("out2.txt")
