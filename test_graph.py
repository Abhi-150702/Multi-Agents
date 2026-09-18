from orchestrator.graph import get_workflow

app = get_workflow()

png_bytes = app.get_graph().draw_mermaid_png()

with open("workflow.png", "wb") as f:
    f.write(png_bytes)

print("Workflow saved to workflow.png")
