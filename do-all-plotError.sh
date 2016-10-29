#!/bin/bash

$(python plotErrorTest.py "$1 Pos" "ke Bias" "ke Bias Error")
$(python plotErrorTest.py "$1 Pos" "ke Resolution" "ke Resolution Error")
$(python plotErrorTest.py "$1 Pos" "x Bias" "x Bias Error")
$(python plotErrorTest.py "$1 Pos" "x Resolution" "x Resolution Error")
$(python plotErrorTest.py "$1 Pos" "y Bias" "y Bias Error")
$(python plotErrorTest.py "$1 Pos" "y Resolution" "y Resolution Error")
$(python plotErrorTest.py "$1 Pos" "z Bias" "z Bias Error")
$(python plotErrorTest.py "$1 Pos" "z Resolution" "z Resolution Error")
