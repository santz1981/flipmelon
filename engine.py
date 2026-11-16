#!/usr/bin/env python3
"""Flipmelon MVP: ADB detection, guided setup, scrcpy session, reconnect."""
import json, os, platform, shutil, subprocess, sys, time
from pathlib import Path

APP = 'Flipmelon'
HOME = Path.home()
CONFIG_DIR = (Path(os.environ.get('APPDATA', HOME)) / APP) if os.name == 'nt' else (Path(os.environ.get('XDG_CONFIG_HOME', HOME / '.config')) / 'flipmelon')
CONFIG_FILE = CONFIG_DIR / 'config.json'
LEGACY_DIR = (Path(os.environ.get('APPDATA', HOME)) / 'AutoDock') if os.name == 'nt' else (Path(os.environ.get('XDG_CONFIG_HOME', HOME / '.config')) / 'autodock')
LEGACY_FILE = LEGACY_DIR / 'config.json'
DEFAULT = {'adb_path': 'adb', 'scrcpy_path': 'scrcpy', 'mode': 'virtual', 'resolution': '1920x1080', 'dpi': 120, 'max_size': 0, 'fullscreen': True, 'poll_seconds': 2, 'onboarding_complete': False, 'start_with_windows': True, 'clean_virtual': False, 'language': 'en'}

def save(c):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(c, indent=2, ensure_ascii=False), encoding='utf-8')

def load():
    c = dict(DEFAULT)
    source = CONFIG_FILE if CONFIG_FILE.exists() else LEGACY_FILE
    if source.exists():
        try:
            old = json.loads(source.read_text(encoding='utf-8'))
            if isinstance(old, dict):
                # Preserve previous preferences, but use the bundled binaries.
                # Migrate only supported mirroring preferences. Do not revive
                # FlipmelonOS or other experimental display-session settings.
                valid = set(DEFAULT) - {'adb_path', 'scrcpy_path'}
                c.update({k:v for k,v in old.items() if k in valid})
                if c['mode'] not in ('virtual', 'mirror'):
                    c['mode'] = 'virtual'
                if not isinstance(c.get('clean_virtual'), bool):
                    c['clean_virtual'] = False
                if c.get('language') not in ('en', 'pt', 'ru', 'es', 'fr'):
                    c['language'] = 'en'
        except (ValueError, OSError):
            print('Configuração inválida; usando padrões.')
    return c

def binary(name):
    path = Path(name).expanduser()
    if path.is_file(): return str(path.resolve())
    return shutil.which(name)

def run(args, timeout=10):
    try: return subprocess.run(args, text=True, capture_output=True, timeout=timeout, check=False, creationflags=(subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0))
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f'Erro: {exc}')
        return None

def devices(adb):
    p = run([adb, 'devices'], 8)
    result = {}
    if p and p.returncode == 0:
        for line in p.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] in ('device', 'unauthorized', 'offline'):
                result[parts[0]] = parts[1]
    return result

def guide():
    print('''\nPREPARAÇÃO DO ANDROID (uma vez por computador):
1. Samsung: Configurações > Sobre o telefone > Informações do software.
2. Toque 7 vezes em "Número de compilação" (outros fabricantes: caminho varia).
3. Abra Opções do desenvolvedor e habilite Depuração USB.
4. Conecte um cabo USB que transfira dados.
5. Desbloqueie o telefone e autorize a chave RSA deste computador.
6. Mantenha o aparelho desbloqueado na primeira autorização.

AVISO: autorize somente computadores confiáveis. Depuração USB amplia o acesso
que um computador autorizado tem ao telefone. Desative-a quando não precisar.
''')

def wizard():
    c = load()
    print('=== Assistente de instalação Flipmelon ===')
    guide()
    for key, label in [('adb_path', 'Caminho do ADB'), ('scrcpy_path', 'Caminho do scrcpy')]:
        val = input(f'{label} [{c[key]}]: ').strip()
        if val: c[key] = val.strip('"')
    for key in ('adb_path', 'scrcpy_path'):
        path = binary(c[key])
        if not path:
            print(f'ATENÇÃO: {key} não encontrado: {c[key]}. Instale-o ou informe o caminho correto.')
        else:
            c[key] = path
            print(f'OK: {key} = {path}')
    mode = input('Modo: [1] tela virtual (padrão), [2] espelhamento: ').strip()
    c['mode'] = 'mirror' if mode == '2' else 'virtual'
    if c['mode'] == 'virtual':
        res = input(f'Resolução virtual [{c["resolution"]}]: ').strip()
        if res: c['resolution'] = res
        dpi = input(f'DPI [{c["dpi"]}]: ').strip()
        if dpi.isdigit() and int(dpi)>0: c['dpi'] = int(dpi)
    save(c)
    print(f'Configuração salva em: {CONFIG_FILE}')
    adb = binary(c['adb_path'])
    if adb:
        run([adb, 'start-server'])
        print('Dispositivos:', devices(adb))
    print('Execute: python flipmelon.py run')

def command(c, scrcpy, serial):
    args = [scrcpy, '--serial', serial]
    if c.get('mode') == 'virtual':
        args.append(f'--new-display={c["resolution"]}/{int(c["dpi"])}')
        # scrcpy enables virtual-display system decorations by default.
        # NEVER add --no-vd-system-decorations here: it can hide the dock/launcher.
        # A clean display is optional; original v0.9 behavior is preserved by default.
        if not c.get('clean_virtual', False):
            args.append('--no-vd-destroy-content')
    elif int(c.get('max_size',0))>0:
        args += ['--max-size', str(c['max_size'])]
    if c.get('fullscreen'): args.append('--fullscreen')
    return args

def mainloop():
    c = load()
    adb, scrcpy = binary(c['adb_path']), binary(c['scrcpy_path'])
    if not adb or not scrcpy:
        print('ADB ou scrcpy não encontrado. Execute primeiro: python flipmelon.py setup')
        return 1
    run([adb, 'start-server'])
    print('Flipmelon aguardando celular USB. Ctrl+C para sair.')
    last = None
    delay = max(1, int(c.get('poll_seconds', 2)))
    while True:
        found = devices(adb)
        state = tuple(sorted(found.items()))
        if state != last:
            print('Estado ADB:', dict(state) if state else 'nenhum aparelho')
            if 'unauthorized' in found.values(): print('Desbloqueie o celular e aceite a autorização de Depuração USB.')
            last = state
        ready = [serial for serial, status in found.items() if status == 'device']
        if not ready:
            time.sleep(delay)
            continue
        if len(ready) > 1:
            print('Mais de um aparelho conectado; desconecte os extras para evitar seleção incorreta.')
            time.sleep(delay)
            continue
        serial = ready[0]
        args = command(c, scrcpy, serial)
        print('Iniciando:', ' '.join(args))
        try:
            proc = subprocess.Popen(args)
            while proc.poll() is None:
                if devices(adb).get(serial) != 'device':
                    print('USB desconectado; encerrando sessão.')
                    proc.terminate()
                    try: proc.wait(timeout=4)
                    except subprocess.TimeoutExpired: proc.kill()
                    break
                time.sleep(delay)
            code = proc.poll()
            if code and code != 0:
                print('scrcpy terminou com erro. Verifique se sua versão suporta --new-display.')
                print('Para espelhamento, execute setup e escolha o modo 2.')
        except OSError as exc: print('Não foi possível iniciar scrcpy:', exc)
        # Avoid rapid respawn loops on unsupported flags or manually closed window.
        print('Aguardando desconexão para nova sessão...')
        while devices(adb).get(serial) == 'device': time.sleep(delay)
        last = None

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h','--help'):
        print('Uso: python flipmelon.py setup | run | check | guide')
        return 0
    action = sys.argv[1]
    if action == 'setup': wizard()
    elif action == 'guide': guide()
    elif action == 'check':
        c = load()
        for k in ('adb_path','scrcpy_path'): print(k, binary(c[k]) or 'NÃO ENCONTRADO')
        adb = binary(c['adb_path'])
        if adb: print('ADB:', devices(adb))
    elif action == 'run': return mainloop()
    else: print('Comando desconhecido:', action); return 2
    return 0

if __name__ == '__main__':
    try: sys.exit(main())
    except KeyboardInterrupt: print('\nFlipmelon encerrado.')
