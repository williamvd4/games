(singular, plural, singular possessive, and plural possessive)


What would be a better way of implementing the drag and drop? The game is projected on an interactive board, but the items are difficult to move.   The students have to hold down on the item for a second before they are able to drage it.

Grid/Flex Improvements: Use CSS Grid for better alignment of drag areas. Ensure touch-friendly sizes (min 44px for buttons/draggables) for mobile.
Progress Indicator: Add a top bar showing lock progress (e.g., "Lock 3/10") with visual dots or a progress bar.

## Plan: 10 Activities on Singular, Plural, Singular Possessive, Plural Possessive

All activities below focus on helping 5th graders identify and use singular, plural, singular possessive, and plural possessive forms. Each activity can be implemented using your existing lock types.

### Steps

1. Review and select from the 10 activity ideas below.
2. For each, prepare prompts, answer sets, and worksheet tasks.
3. Implement as new locks in your `levels` array, using the most fitting type.
4. Test for clarity and grade-level appropriateness.

### 10 Activity Ideas

1. **Which Is Which? (multiple_choice)**

   - Scene: “Which is a singular possessive noun?”
   - Choices: “cats”, “cat’s”, “cats’”, “cat”
   - Answer: “cat’s”
   - Worksheet: “Write your own singular possessive noun.”
2. **Sort the Words (sorting_drag)**

   - Scene: “Sort each word into the correct group.”
   - Categories: “Singular”, “Plural”, “Singular Possessive”, “Plural Possessive”
   - Words: “dog”, “dogs”, “dog’s”, “dogs’”, “girl”, “girls”, “girl’s”, “girls’”
   - Worksheet: “Add one more word to each group.”
3. **Find the Plural Possessive (multiple_choice)**

   - Scene: “Which word is a plural possessive?”
   - Choices: “dogs”, “dog’s”, “dogs’”, “dog”
   - Answer: “dogs’”
   - Worksheet: “Write a sentence using a plural possessive.”
4. **Match the Form (matching_drag)**

   - Scene: “Match each description to the correct word.”
   - Pairs: “More than one cat” → “cats”, “Belonging to one cat” → “cat’s”, “Belonging to more than one cat” → “cats’”, “One cat” → “cat”
   - Worksheet: “Draw a picture for each match.”
5. **Fix the Sentence (multiple_choice)**

   - Scene: “Which sentence uses a plural possessive correctly?”
   - Choices: “The girls’ shoes are new.”, “The girl’s shoes are new.”, “The girls shoes are new.”, “The girls’s shoes are new.”
   - Answer: “The girls’ shoes are new.”
   - Worksheet: “Write your own sentence with a plural possessive.”
6. **Build the Word (reorder_sentences)**

   - Scene: “Drag the pieces to make a singular possessive word.”
   - Fragments: “dog”, “’”, “s”
   - Answer: “dog’s”
   - Worksheet: “Build a plural possessive word.”
7. **Who Owns It? (matching_drag)**

   - Scene: “Match the owner to what they own.”
   - Pairs: “The dog’s” → “bone”, “The dogs’” → “leashes”, “The girl’s” → “book”, “The girls’” → “backpacks”
   - Worksheet: “Write a sentence for each match.”
8. **Spot the Error (multiple_choice)**

   - Scene: “Which word is NOT a correct possessive?”
   - Choices: “cat’s”, “cats’”, “cats’s”, “dog’s”
   - Answer: “cats’s”
   - Worksheet: “Correct the mistake.”
9. **Sentence Sort (sorting_drag)**

   - Scene: “Sort each sentence by the type of noun it uses.”
   - Categories: “Singular”, “Plural”, “Singular Possessive”, “Plural Possessive”
   - Sentences: “The dog runs.”, “The dogs run.”, “The dog’s collar is red.”, “The dogs’ collars are red.”
   - Worksheet: “Write one new sentence for each group.”
10. **Choose the Right Form (multiple_choice)**

    - Scene: “Which word means ‘belonging to more than one girl’?”
    - Choices: “girls”, “girl’s”, “girls’”, “girl”
    - Answer: “girls’”
    - Worksheet: “Write a sentence using ‘girls’.’”

### Further Considerations

1. Would you like to include visual aids or keep activities text-only?
2. Should distractors always be real words, or can they be “nonsense” forms (like “cats’s”)?
