# PTV - Process Tree Verifier

This directory contains the extraction prototype which are two simple scripts that use the OpenAI API for prompting their models.

A valid key (with a payed account) will be required to test the functionality. Insert your key into the respective field for each script.

For the singleRequirementPrompt.py script you can pass any requirement after the script to test it out like so:

`python3 singleRequirementPrompt.py "This is a requirement of a process"`
You can find example results in CollectionSingleRequirement.txt

For the textualProcessDescription.py you can pass any textual process description inside the script. Currently it contains two textual
process descriptions of the processes used for the user study already. Either try it with those or add a different one and change to it in
the prompt then execute the script using:
`python3 textualProcessDescriptions.py`

Both scripts use effectively the same prompting strategy.

The only required packages should be openai and argparse with can be installed using:
`pip install openai`
and
`pip install argparse`
