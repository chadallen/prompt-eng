# prompt-eng

This is an experiement in recursive prompt engineering. There has been a lot of discussion recently about the exponentailly increasing value of "prompt engineering" as a skill[1]. I wanted to know: is GPT any good at prompt engineering? If we give it some facts and a target answer, can it generate a question that, when posed back to itself, elicits the correct response? Sort of like Jeopardy for LLMs. 

My very naive approach here uses the SQuAD database[2], which is a giant set of: passages from Wikipedia, reading comprehension questions for those passages, answers to those questions. I give GPT the passages and then answers and tell it to come up with prompts that are likely to elecit the correct answer. Then I again give it the passages along with its newly generated questsions and ask it to answer those questions. I then compare this answer to the ground truth answer. Well, not really, becuase that would require me to do some kind of fuzzy matching to check that the answers have equivalent thruthiness even if they are not a string match. But what I can say is that just by eyeballing the answers it tends to get this right.

My fuzzy intuitions here are that this kind of training is important for any multi-layered systems where we expect LLMs to direct other LLMs. In those systems, the LLMs doing the directing need to be good prompt engineers.

Disclaimers: 

1. I'm not an engineer, so apologies if this code seems janky or hacky.
2. Don't blame me, GPT-4 wrote most of it.

[1] https://www.forbes.com/sites/craigsmith/2023/04/05/mom-dad-i-want-to-be-a-prompt-engineer/?sh=8b843559c8ef
[2] https://rajpurkar.github.io/SQuAD-explorer/
