# RLR: Hackathon Brief
## The problem
Every medical claim in South Africa needs an ICD-10 code that exactly matches the patient's diagnosis. Busy doctors and admin staff get this wrong because there are thousands of codes and the rules keep changing. Wrong codes lead to rejected claims, lost revenue and a lot of rework. The BHF says South African medical schemes lose around R30 billion a year to fraud, benefit abuse and improper billing. Not all of that is coding errors, but bad coding is a big part of it. Bad coding also hurts patients, because a code that doesn't map to a PMB condition gets the claim treated as non-PMB, with a co-payment imposed.  (businesstech)  (pages)
## Our solution
An AI tool that turns a doctor's plain-language note into the correct ICD-10 code in about 5 seconds.
The doctor types the problem in normal language.
The AI suggests the top 3 matching codes, each with a one-line reason.
Every code is checked against the official SA ICD-10 Master Industry Table, so the AI can't invent a code.
The doctor confirms with one tap.
Why it matters
Fewer rejected claims, because codes are right the first time.
Hospital wards recover revenue they would otherwise lose.
Our model is a 90/10 split, so wards fund themselves and can hire unemployed doctors without a new government budget.
What we build for the hackathon
Only the core feature: a text box, three code suggestions with reasons, and a confirm button. The 90/10 model is the pitch, not the demo