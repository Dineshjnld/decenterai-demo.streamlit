import sys


def get_notebook_cmd(starter_script: str, python_repl=sys.executable):
    # It will save executed notebook to your-notebook.nbconvert.ipynb file. You can specify the custom output name and custom output director
    cmd_string = 'jupyter nbconvert --execute --to notebook --output custom-name --output-dir /custom/path/ your-notebook.ipynb'

    cmd_string = (
        'jupyter nbconvert --execute --to notebook --allow-errors your-notebook.ipynb'
    )
    #  You can execute the notebook and save output into PDF or HTML format. Additionally, you can hide code in the final notebook. The example command that will execute notebook and save it as HTML file with code hidden.
    cmd_string = f'jupyter nbconvert --execute --to html --no-input {starter_script}'
    cmd_string = f'jupyter nbconvert --execute --to html --output {starter_script} {starter_script}'

    # cmd_string = f'jupyter nbconvert --execute --to notebook {starter_notebook}'
    command = cmd_string.split(' ')

    if python_repl is not None:
        command = [python_repl, '-m'] + command

    return command


def get_python_cmd(starter_script, python_interpreter=sys.executable):
    command = [python_interpreter, starter_script]
    return command
