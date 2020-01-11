import os
import subprocess

from app import options

"""
For some reason I failed to get PyQt threads working.
"""


def run_command(command):
    result = subprocess.run(
        command.split(),
        cwd=options.BASE_DIR,
        stdout=subprocess.PIPE,
    )
    return result.returncode, result.stdout.decode('utf8').strip()


def notify(text):
    if os.name == 'nt':
        os.system('start "" cmd /c "echo {}&echo(&pause"'.format(text))


def update():
    _, git_hash = run_command('git rev-parse HEAD')
    status, _ = run_command('git pull')
    if status:
        notify('Не удалось скачать обновление')
        return

    _, new_git_hash = run_command('git rev-parse HEAD')
    if len(git_hash) != len(new_git_hash):
        notify('Не удалось скачать обновление')
        return

    if git_hash == new_git_hash:
        notify('Нет доступных обновлений')
        return

    run_command('pip install -r requirements.txt')

    notify('Обновление завершено. Нужно перезагрузить программу.')


if __name__ == '__main__':
    update()
