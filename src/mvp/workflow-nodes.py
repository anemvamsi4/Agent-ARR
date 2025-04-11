from pathlib import Path

from langchain_core.messages import HumanMessage

from extraction import PDFTextExtractor
from llms import get_llm
from prompts import planner_prompt
from output_structures import PlannerResponse

def extract_text(pdf_path: str, output_dir: str):
    markdown_file = str(Path.joinpath(output_dir, Path(pdf_path).stem, Path(pdf_path).stem)) + '.md'
    if Path.exists(markdown_file):
        with open(markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            
    markdown_text = PDFTextExtractor(pdf_path, Path.joinpath(output_dir, Path(pdf_path).stem)).extract()

    return markdown_text


def code_planner(context: str, llm, user_input: str = None) -> PlannerResponse:
    if user_input is None:
        user_input = "Give me a plan of codebase structure to reproduce results from this paper content"
    
    
    final_prompt = planner_prompt.format(context = context, user_input = user_input)
    planner_llm = llm.with_structured_output(PlannerResponse)
    plan_response = planner_llm.invoke(final_prompt)
    return plan_response