# Recon Atlas

**Custom scanners modulares para inventário autorizado de superfície de ataque.**

Recon Atlas é um toolkit defensivo em Python para avaliar ativos próprios ou explicitamente autorizados. Ele combina descoberta de subdomínios, varredura TCP de portas, enumeração conservadora de caminhos HTTP, resolução DNS, escopo obrigatório, rate limiting e relatórios reproduzíveis.

> **Uso autorizado somente.** O projeto não explora vulnerabilidades, não faz bypass de autenticação, não executa payloads e não deve ser usado contra terceiros sem autorização documentada.

## O que torna o projeto diferente

- **Scope firewall:** cada execução exige um arquivo de autorização com alvos, portas, caminhos, janela de tempo e limites.
- **Evidence cards:** cada achado guarda evidência, timestamp, método e nível de confiança.
- **Budget-aware:** requests e conexões possuem orçamento, concorrência máxima e atraso mínimo.
- **Passive-first:** subdomínios passivos usam apenas candidatos fornecidos pelo operador.
- **Noisy by design:** User-Agent identificável e header de contato configurável.
- **Reproducible runs:** configuração, versão, hash da scope e resultados ficam no artefato.
- **Three lenses:** DNS, portas e conteúdo HTTP são módulos independentes.

## Início rápido

```bash
python3 -m recon_atlas.cli init-scope --domain example.com --out scope.json
python3 -m recon_atlas.cli validate-scope --scope scope.json
python3 -m recon_atlas.cli scan --scope scope.json --module dns --out artifacts/run.json
python3 -m recon_atlas.cli report --input artifacts/run.json --format markdown --out artifacts/report.md
```

O primeiro comando cria um modelo para revisão. Edite `scope.json`, confirme propriedade/autorização e execute o scan somente depois.

## Autorização e limites

A scope valida alvo, porta, prefixo HTTP, janela de tempo, orçamento, concorrência, política de IP privado, operador e responsável pela autorização.

```json
{
  "scope_id": "customer-example-2026",
  "operator": "security@example.com",
  "authorized_by": "owner@example.com",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-12-31T23:59:59Z",
  "domains": ["example.com"],
  "hosts": [],
  "cidrs": [],
  "ports": [80, 443, 8080, 8443],
  "path_prefixes": ["/", "/robots.txt", "/sitemap.xml"],
  "max_requests": 250,
  "max_connections": 100,
  "min_delay_ms": 250,
  "max_concurrency": 4,
  "allow_private": false,
  "contact": "security@example.com",
  "user_agent": "ReconAtlas/0.1 (+security@example.com)"
}
```

Não coloque tokens, cookies, senhas ou chaves privadas no arquivo de scope.

## Instalação

Requer Python 3.10+ e não exige dependências externas no núcleo:

```bash
git clone https://github.com/SEU_USUARIO/recon-atlas.git
cd recon-atlas
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Uso

```bash
python -m recon_atlas.cli validate-scope --scope scope.json
python -m recon_atlas.cli subdomains --scope scope.json --wordlist data/subdomains.txt --mode passive --out artifacts/subdomains.json
python -m recon_atlas.cli ports --scope scope.json --host app.example.com --out artifacts/ports.json
python -m recon_atlas.cli paths --scope scope.json --url https://app.example.com --wordlist data/paths.txt --out artifacts/paths.json
python -m recon_atlas.cli report --input artifacts/ports.json --format html --out artifacts/ports.html
```

O módulo HTTP faz GET simples, respeita prefixos autorizados e não tenta autenticação, bypass, fuzzing de parâmetros ou exploração. O módulo TCP só estabelece conexões, sem payload de protocolo ou banner grabbing agressivo.

## Módulos

- `scope`: autorização, janela, escopo de hosts, portas, caminhos e orçamento.
- `dns`: resolução A/AAAA e descoberta de candidatos por wordlist.
- `ports`: conexões TCP com timeout, rate limit e concorrência limitada.
- `http_paths`: GET limitado, status, content-type, tamanho e título básico.
- `evidence`: cartões normalizados com confiança e método.
- `reports`: JSON, CSV, Markdown e HTML.

## Estrutura de um achado

```json
{
  "finding_id": "paths-1234abcd",
  "module": "paths",
  "target": "https://app.example.com/admin",
  "status": "interesting",
  "confidence": "medium",
  "observed_at": "2026-01-01T12:00:00Z",
  "evidence": {"http_status": 200, "content_type": "text/html", "content_length": 1842, "title": "Admin portal"},
  "method": "GET",
  "notes": "Discovery is not proof of authorization bypass."
}
```

Um finding é uma pista para revisão, não uma vulnerabilidade confirmada.

## Segurança operacional

- Execute somente em ativos próprios ou com autorização escrita.
- Comece com `--module dns` e escopos pequenos.
- Mantenha concorrência baixa e atraso alto em produção.
- Use User-Agent identificável e contato configurado.
- Proteja relatórios: hostnames, portas e caminhos podem ser sensíveis.
- Verifique a política do provedor de nuvem antes de scans externos.
- Pare se o proprietário, provedor ou monitoramento solicitar.

## Testes

```bash
python -m unittest discover -s tests -v
python -m compileall recon_atlas
```

Os testes usam validação local e mocks, sem varredura externa. O CI executa testes, compilação, validação de scope e procura por segredos acidentais.

## Estrutura do repositório

```text
recon-atlas/
|-- .github/workflows/ci.yml
|-- data/
|   |-- paths.txt
|   `-- subdomains.txt
|-- docs/
|   |-- architecture.md
|   |-- authorization.md
|   `-- responsible-use.md
|-- recon_atlas/
|   |-- __init__.py
|   |-- budget.py
|   |-- cli.py
|   |-- config.py
|   |-- dns.py
|   |-- evidence.py
|   |-- http_paths.py
|   |-- models.py
|   |-- ports.py
|   |-- reports.py
|   |-- scope.py
|   `-- subdomains.py
|-- examples/scope.example.json
|-- tests/
|-- .gitignore
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- pyproject.toml
`-- README.md
```

## Roadmap

### v0.1

- [x] Scope obrigatória e janela de autorização.
- [x] DNS/subdomínios, portas TCP e paths HTTP.
- [x] Rate limiting, orçamento e concorrência limitada.
- [x] Evidências e relatórios JSON/CSV/Markdown/HTML.
- [x] CI e testes sem varredura externa.

### v0.2

- [ ] Worker Go de portas com o mesmo contrato de scope.
- [ ] Persistência SQLite local e diff entre execuções.
- [ ] Importação de fontes CT configuradas pelo operador.
- [ ] Revisão de scope por pull request.

### v0.3

- [ ] Assinatura dos artefatos de evidência.
- [ ] Integração opcional com sistemas de tickets.
- [ ] Dashboard local sem envio automático de dados.

## Referências

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Attack Surface Identification](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/04-Attack_Surface_Identification)
- [RFC 9309 Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309)
- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final)
- [MITRE ATT&CK Reconnaissance](https://attack.mitre.org/tactics/TA0043/)

## Licença

MIT. Veja `LICENSE`.
