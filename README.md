# EvaluationRules
*Evaluation rules! On the use of grammars and rule-based systems for NLG evaluation*

This folder provides code to analyse the extended WebNLG dataset. The code is part of the following paper: 

```
@inproceedings{evaluationrules,
	author = {Emiel van Miltenburg and Chris van der Lee and Thiago Castro-Ferreira and Emiel Krahmer},
	booktitle = {Proceedings of the First Workshop on Evaluating NLG Evaluation (EvalNLGEval)},
	publisher = {ACL},
	title = {Evaluation rules! On the use of grammars and rule-based systems for NLG evaluation},
	year = {2020}}
```

## Requirements
The code was run using Python 3.7.4. Other versions may work as well, but are untested. Libraries used:
* lxml 4.4.1
* seaborn 0.9.0
* matplotlib 3.1.1
* pandas 0.25.1

## How to use
1. Download [the Extended WebNLG repository](https://github.com/ThiagoCF05/webnlg), put it in this folder, and call it `webnlg-master`.
2. Run `python analyse_all_pred_freq.py`. This generates the main figure, and some statistics about the number of examples for each predicate.
3. Run `python analyse_templates.py`. All relevant information is printed in the Terminal.
