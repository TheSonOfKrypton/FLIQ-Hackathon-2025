# Quantum Error Correction with the Surface-17 Code

This Jupyter Notebook provides a full hands-on walkthrough of implementing a distance-3 surface code, the **Surface-17** code, using Qiskit 2.0+. It is designed as a tutorial to teach how quantum error correction (QEC) works at the circuit level and how to run QEC routines on real IBM Quantum hardware.

## Overview

Quantum computers are inherently noisy. The surface code is the leading error-correcting code that offers fault tolerance using only local, nearest-neighbor interactions. In this tutorial, I:

- Explain stabilizer codes and syndrome extraction
- Construct and simulate the Surface-17 layout
- Inject and decode single-qubit errors
- Build a simple lookup decoder
- Run simplified experiments on real IBM Quantum devices

The notebook is beginner-friendly but detailed enough for intermediate quantum engineers. I hope you enjoy learning about Quantum Error Correction just how I did!

## Requirements

I recommend using the provided Python packages that I used in my virtual environment for reproducibility. You can find them in "requirements.txt".

The test.py file ensures that the functions used on IBM's hardware work before submitting the job. If you update a function in notebook for an exercise, ensure you make the respective update in the test.py file and run it first before submitting a job on IBM's hardware.

Happy Qhacking!
