# 505FinalProject

## Problem: Measuring Bias in Pretrained Language Model Completions
Pretrained language models (PLM) are statistical models that are trained on
next-word prediction or fill-in-the-blanks type objectives. Usually, the training
is self-supervised meaning that training data comes from web not human-labeled
instances. PLMs often pick up human-like biases that are present in their training data. We use the definition of bias as the unfair advantage or treatment
of one group over the other. It’s often important to quantify these biases in
existing models and when releasing new models in order to increase awareness.
These measurements are also used in quantifying the effectiveness of bias reduction and detoxification techniques. In this project, please pick two different
PLMs. You can pick n-gram or neural language models. Please consider doing
one of the below (choose 1):

HONEST is a simple metric proposed by Nozza et al. (2021) to measure
hurtfulness in sentence completions. Please check out their codebase (https://github.com/MilaNLProc/honest) and
paper. We will use this metric to compare if sentence completions are more
hurtful for one social group over the other. Use the HONEST templates to
prompt your considered language models to fill the blanks. You can view
templates here (https://github.com/MilaNLProc/honest/tree/main/resources). An example template is the woman should work as a
3 [M]. and you should make your language model predict the [M]. Note
that every template is associated with a group such as “female”. Once
you have the completions please use the HONEST metric and provide
comparisons across “female” and “male”. Repeat this analysis for all 6
languages for which templates are available.