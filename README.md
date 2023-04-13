# prompt-eng

This is an experiement in recursive prompt engineering. There has been a lot of discussion recently about the exponentailly increasing value of "prompt engineering" as a skill[1]. I wanted to know: is GPT any good at prompt engineering? If we give it some facts and a target answer, can it generate a question that, when posed back to itself, elicits the correct response? Sort of like Jeopardy for LLMs. TL;DR, yes. My fuzzy intuitions here are that this kind of training is important for any multi-layer systems where we expect LLMs to direct other LLMs. In those systems, the LLMs doing the directing need to be good prompt engineers.

Disclaimers: 

1. I'm not an engineer, so apologies if this code seems janky or hacky.
2. Don't blame me, GPT-4 wrote most of it.

[1] https://www.forbes.com/sites/craigsmith/2023/04/05/mom-dad-i-want-to-be-a-prompt-engineer/?sh=8b843559c8ef
