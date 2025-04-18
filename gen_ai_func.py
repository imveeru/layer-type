import enum
from pydantic import BaseModel, Field
from llama_index.llms.ollama import Ollama
from llama_index.core.program import LLMTextCompletionProgram

# Define the LayerType enumeration
class LayerType(str, enum.Enum):
    SHAPE = "SHAPE"
    IMAGE = "IMAGE"
    TEXT = "TEXT"

# Define the Pydantic model for structured output
class LayerClassification(BaseModel):
    layer_type: LayerType = Field(description="The type of the layer: SHAPE, IMAGE, or TEXT")

# Initialize the Ollama model
llm = Ollama(model="llama3.1:latest", request_timeout=120.0, temperature=0.1)

# Define the prompt template
prompt_template_str = """
Given the semantic label of a layer found in a graphic design poster, determine what type of layer it is.

Input Label: {label}

To help with classification:
- Labels such as text, typography, font, content, or quote fall under the TEXT layer type.
- Labels like shape, illustration, symbol, icon, logo, line, circle, or any other specific geometric form fall under the SHAPE layer type.
- All other labels—typically object names or general nouns—fall under the IMAGE layer type.

The classification should generalize to handle other relevant labels not explicitly listed here, based on their semantic meaning.

Respond with one of the following layer types: SHAPE, IMAGE, TEXT.
"""

# Set up the LLM program
program = LLMTextCompletionProgram.from_defaults(
    llm=llm,
    output_cls=LayerClassification,
    prompt_template_str=prompt_template_str,
    verbose=True,
)

# Define the classification function
def get_llm_res(label: str) -> LayerType:
    result = program(label=label)
    return result.layer_type.name.lower()

# label = "candle"
# layer_type = get_llm_res(label)
# print(f"The layer type for '{label}' is: {layer_type}")
