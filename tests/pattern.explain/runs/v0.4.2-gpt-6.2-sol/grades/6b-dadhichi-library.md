1 No lookups: The request opens with “Explain Kafka consumer groups for my train ride.” The reader encounters both “Kafka” and “consumer groups” before either is defined. **Fail**

2 Linear: “Kafka is the system in this example” and “A consumer group is a set of readers that share that work” supply the meaning of the request the reader has already encountered. The earlier description of programs sharing work gives the gist, but the reader needs the later sentences to interpret the request’s exact wording. **Fail**

3 Accurate: Across the architecture, engine, testing workflow, and worked example, the claims match the design. In particular, “pass more checks overall and preserve every check the previous version passed” captures both conditions for promotion, and the failed Kafka test is explicitly hypothetical. **Pass**

4 Proportional: The supplied count is 1,219 words, within the 2,200-word ceiling for this moderate topic. **Pass**

5 No padding: “The train example below uses the proposed workflow” overlaps with the next sentence, “It illustrates how the parts fit together without assuming the tests have already run.” The distinction between a design and a completed test matters, but the first sentence can go without losing it. **Borderline**

6 Resumable: All three eligible section openings recover the preceding step. They recall the train reader’s need for a linear explanation, the library’s places for the reusable parts, and the engine’s finished prompt with two starting points for tests. **Pass**

7 Plain text: The entire piece, including “The whole picture,” uses headings and short prose paragraphs. The precedence rule is the closest thing to a diagram, and its ordered sentence reads correctly on a narrow screen. **Pass**

8 Not dumbed down: The train example follows one request without introducing fictional characters. Across the piece, real terms such as “kernel” and “colleague test” stay intact, and a prompt that “can travel on its own” accurately conveys that it carries the context needed to use it elsewhere. **Pass**

9 Trap handled: “Several prompts that share most of their instructions” identifies the misconception that building a library means saving whole prompts. The next paragraph corrects it with “stores reusable instructions in separate parts.” **Pass**

10 Clean output: From title through closing paragraph, there is no visible plan, grading commentary, or offer to continue. “The design lays out a build and testing roadmap” describes Dadhichi’s development status and makes no reference to material supplied to the writer. **Pass**

11a Complete: Each step in “The whole picture” has a worked counterpart in the body. The engine assembles the train prompt, reviews it from a colleague’s perspective, supplies test inputs, and the hypothetical early use of “consumer group” illustrates how a revision is compared with its predecessor. **Pass**

11b Unhurried: The paragraph beginning “Suppose you ask” introduces two new terms, “Kafka” and “consumer group.” They are related, but their definitions describe a system and a group of readers rather than a pair defined against each other, so the rubric’s two-term convention applies. **Borderline**

12 Unknown topic: This is input 6. The check applies only to input 4. **Not applicable**

13 Source confidence: Across the design description, workflow, and testing example, no proposed result is presented as measured. The strongest apparent claim, “The engine has produced a prompt,” stays within the example introduced as a “proposed workflow,” and the version comparison starts with “Suppose.” **Pass**

Summary: 9 Pass, 2 Borderline, 2 Fail, 1 Not applicable. The main break comes when the quoted request introduces “Kafka consumer groups” before the reader can connect either term to the work-sharing example.