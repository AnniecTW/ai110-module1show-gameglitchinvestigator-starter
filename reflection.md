# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

--- First, the difficulty labels don’t make sense because the number range for the hard level is smaller than the range for the normal level. Second, when I click the "New Game" button, only the answer changes. The attempt count stays the same. Also, the attempt count should be zero at the beginning of the game.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  One problem I solved was adjusting the difficulty labels so that the number range for hard difficulty is the largest among the three labels. To fix this, AI suggested changing hard's range from `1-50` to `1-200`, which made the difficulty distribution more reasonable. I verified the result by running three pytests added by Claude and by manually playing the game to confirm the behavior.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  So far I have not encountered any AI suggestions that were incorrect or misleading for the problems I asked about.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  For the difficulty issues, I ran the pytest written by Claude. It first created a helper function `_get_range_for_difficulty` to mirror app.py so the tests could stay self-contained without importing Streamlit.
  The three tests check whether the upper value in the tuple returned by `_get_range_for_difficulty` for the three difficulty levels is in the correct order:
  easy_high < normal_high < hard_high.
- Did AI help you design or understand any tests? How?
  Yes, it helped me understand the bugs and the tests design. It explained the cause of the issue and the purpose of the pytest cases in a clear way.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
