# PromptShield Dataset Schema

## Dataset Purpose

This dataset is designed to evaluate the ability of PromptShield to distinguish between benign prompts and potentially malicious prompts.

## Categories

### 1. benign

Normal prompts that do not attempt to manipulate or bypass the AI system.

### 2. prompt_injection

Prompts that attempt to override, ignore, or manipulate existing instructions.

### 3. jailbreak

Prompts that attempt to bypass restrictions or change the intended behavior of the AI system.

### 4. system_prompt_extraction

Prompts that attempt to reveal hidden system instructions, internal rules, or confidential configuration.

### 5. sql_injection

Prompts or payloads containing SQL command tokens designed to manipulate databases (e.g., SELECT, UNION, DROP).

### 6. cross_site_scripting

Client-side script injection payloads (XSS) targeting script execution in web UI boundaries.

### 7. command_injection

System commands chained inside inputs to execute unauthorized commands on host terminals (e.g., cat, rm, whoami).

## Labels

0 = Benign

1 = Attack

## Severity Levels

none = Benign prompt

high = Potentially dangerous attack

critical = Attempt to expose confidential system information

## Dataset Columns

prompt_id

prompt_text

attack_category

label

severity

source