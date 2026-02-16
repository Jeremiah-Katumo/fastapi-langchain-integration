from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


examples = [
    {
        "input": "What is the capital of France?",
        "output": "Positive"
    },
    {
        "input": "What is the capital of Germany?",
        "output": "Positive"
    },
    {
        "input": "I love transformers. What are they?",
        "output": "Positive"
    },
    {
        "input": "I hate Legacies series.",
        "output": "Negative"
    }
]

example_template = """
Input: {input}
Output: {output}
"""

example_prompt = PromptTemplate(
    input_variables=["input", "output"], 
    template=example_template
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples, 
    example_prompt=example_prompt, 
    input_variables=["input"],
    prefix="Determine if the sentiment of the following input is positive or negative.", 
    suffix="Input: {input}\nOutput:",
    example_separator="\n"
)

formatted_prompt = few_shot_prompt.format(input="I dislike rainy days.")
print(formatted_prompt)

