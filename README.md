# pyrelalg

During my study of Database design, I had some troubles with relational algebra.\
I tried some tools but they did not satisfy me, so I decided to write this very simple library (if it can be called that) in order to debug the relational algebra expressions I needed.

This "library" is provided as-is, without any warranty, the code might need some more polish, I'll see if I can improve it in the future.


## How to use

Please, check the "various-tests/exercise-example.py" file in order to see a sample program.\
In order to use the library WITHOUT installing, you can use the script `add_python_path.sh` by calling it with:

```
. add_python_path.sh
```

This way, you may execute any pyrelalg script, whatever your current working directory is!\
Once the shell is closed of course, you will have to do that again...\
Please note that bash 3+ is needed for the BASH_SOURCE variable is used (also dirname and realpath).
