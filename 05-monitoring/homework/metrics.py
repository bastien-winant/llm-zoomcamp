def calculate_cost(usage, model="gpt-5.4-mini"):
	cost = 0
	if "gpt-5.4-mini" in model:
		cost = (usage.input_tokens * 0.15 + usage.output_tokens * 0.60) / 1_000_000
	return cost