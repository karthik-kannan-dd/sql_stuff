# Time Fraud Model V2 - Golden Dataset

## Context
This is an improvement on the existing time fraud model (v1). V2 aims to build a better golden dataset for more accurate fraud adjudication.

## Purpose
Construct a golden dataset to train/evaluate a time fraud model. The model receives late delivery cases and must decide whether they constitute fraud or not.

## What is a Golden Dataset?
A representative sample of all different types of fraud and non-fraud cases that helps the model adjudicate cases properly. It should cover:
- Clear fraud cases (various fraud patterns)
- Clear non-fraud cases (legitimate lateness)
- Edge cases / ambiguous scenarios

## Background
This project builds on the lateness analysis work in `../lateness_analysis/`, which established:
- Lateness distribution patterns
- Tier definitions for lateness severity
- Analysis of egregious, moderate, and mild lateness cases

## Key Context
- Late cases come from deliveries where actual times deviate from expected times
- The model needs labeled examples of fraud vs legitimate lateness to learn patterns
- Golden dataset should be balanced and representative across fraud types and severity tiers
