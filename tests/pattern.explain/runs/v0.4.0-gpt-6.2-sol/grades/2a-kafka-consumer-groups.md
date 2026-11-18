1 No lookups: Across the opening, body and closing list, the technical names receive plain-language explanations. Even “group ID” is introduced through the concrete name `shipping` that the consumers give Kafka, and each closing setting is explained on its own line. **Pass**

2 Linear: The explanation moves from stored orders to partitions, assignments and saved positions. The question “When partition 2 changes hands, how does its new consumer know where to start?” comes after the handover is explained, so the reader can understand the question before learning about offsets. **Pass**

3 Accurate: The assignment and restart examples remain consistent throughout. The one-consumer limit is qualified by “when the group is settled,” and committing 42 after processing through 41 correctly explains why a crash before the next commit can cause order 42 to be processed again. **Pass**

4 Proportional: The supplied count is 1,017 words, within the 2,200-word ceiling for this moderate input. **Pass**

5 No padding: “Even with three active consumers, an unusually busy partition still belongs to one of them” repeats the earlier point that “partition 0 stays together even if it contains most of the orders.” The three-consumer context is new, but the preceding sentences already establish what the third consumer can do. **Borderline**

6 Resumable: Both eligible sections reopen with what the reader already holds. “The shop has three partitions in `orders`” restores the assignment problem, and “A rebalance can give partition 2 to a different shipping consumer” restores the handover that makes a saved position necessary. **Pass**

7 Plain text: The entire article uses headings, prose and a flat three-item closing list. Its longest setting names appear as individual inline terms, with no table, link, image or wide code block to navigate. **Pass**

8 Not dumbed down: The shop remains the running example from order storage through shipment creation. It uses real Kafka terms throughout, with no invented character or analogy carrying the explanation. **Pass**

9 Trap handled: “A fourth shipping consumer has no partition to read” directly corrects the expectation that another consumer always adds capacity. The reporting example also shows why a consumer in a different group can still read the same order. **Pass**

10 Clean output: From the title through the final “partition assignor” entry, the output contains only the article, with no plan, source commentary or offer to expand. **Pass**

11a Complete: Every mechanism in “The whole picture” has a worked counterpart. `shipping` and `reporting` establish group identity and independent progress, the three partitions show assignment and reassignment, and the crash after shipment creation shows what a committed offset can recover. **Pass**

11b Unhurried: “Kafka runs on servers and stores records so that programs can read them independently” introduces the product, then “A named stream of records is called a *topic*” introduces a second term in the same paragraph. They are related, but they are not a pair defined against each other. **Borderline**

12 Unknown topic: This is input 2. The unknown-tool condition applies only to input 4. **Not applicable**

13 Source confidence: The graded source block is empty. **Not applicable**

Summary: 10 Pass, 2 Borderline, 0 Fail, 2 Not applicable; the more consequential weakness is the opening paragraph that asks the reader to absorb Kafka and *topic* together while first learning how orders are stored.