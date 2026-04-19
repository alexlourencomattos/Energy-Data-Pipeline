# Próximos passos (do código para produção)

Este guia mostra como sair do estado atual e publicar o dashboard com CI/CD.

## 1) Preparar o repositório no GitHub

1. Garanta qual é o branch padrão do repositório (`main` ou `master`).
2. Vá em **Settings → Actions → General** e permita workflow read/write.
3. Vá em **Settings → Actions → Runners** e use `ubuntu-latest` (default).

## 2) Validar localmente

> Recomendado: Python 3.11+

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
pytest -q
python main.py --stage all
streamlit run app.py
```

Se o `pytest` falhar por dependências, rode novamente após instalar tudo com `requirements.txt`.

## 3) Rodar via Docker

```bash
docker compose up --build
```

A aplicação ficará em: `http://localhost:8501`.

## 4) Ativar CI/CD (GitHub Actions)

O workflow já está em `.github/workflows/ci-cd.yml` e faz:
- Testes (`pytest -q`)
- Build de imagem Docker (também em pull request)
- Push para GHCR apenas em push no branch padrão (`main` ou `master`)

### Para push no GHCR

1. Em **Settings → Packages**, habilite publicação de pacotes.
2. Garanta que o workflow tenha `permissions: packages: write` (já configurado).
3. Faça merge no branch padrão.

Imagem esperada:

`ghcr.io/<seu_usuario_ou_org>/energy-data-pipeline:latest`

## 5) Publicar dashboard online

### Opção A — Streamlit Community Cloud

1. Conecte o repositório.
2. Main file: `app.py`.
3. Python requirements: `requirements.txt`.
4. Configure variáveis de ambiente (se usar paths customizados):
   - `FACT_FILE`
   - `GOLD_DIR`
   - `INGESTION_URL` / `INGESTION_YEAR`

### Opção B — Render/Railway/Fly.io (Docker)

1. Configure deploy por Dockerfile.
2. Porta do serviço: `8501`.
3. Command (se necessário):
   `streamlit run app.py --server.address=0.0.0.0 --server.port=8501`

## 6) Operação contínua (recomendado)

- Criar branch protection no branch padrão exigindo CI verde.
- Adicionar badge de status do workflow no README.
- Versionar imagem Docker por tag de release além de `latest`.
- Configurar monitoramento básico de falhas no app/ingestão.

## 7) Checklist de pronto para produção

- [ ] `pytest -q` passando no GitHub Actions
- [ ] Build Docker passando no Actions
- [ ] Imagem publicada no GHCR
- [ ] Dashboard acessível via URL pública
- [ ] Dados atualizados com pipeline executado

## 8) “Tá no GitHub com Actions, e agora?”

Se o workflow já está no ar, faça exatamente nesta ordem:

1. Abra a aba **Actions** e confirme que o último run está ✅ (job `test`).
2. Confirme também ✅ no job `docker` (em PR ele builda sem publicar).
3. Vá em **Packages** e valide a imagem:
   - `ghcr.io/<seu_usuario_ou_org>/energy-data-pipeline:latest`
4. Faça o deploy em um host:
   - **Streamlit Cloud** (mais simples), ou
   - **Render/Railway/Fly** com imagem do GHCR.
5. Defina variáveis de ambiente no host (`FACT_FILE`, `GOLD_DIR`, etc.).
6. Abra a URL pública e valide:
   - dashboard carrega,
   - gráficos aparecem,
   - filtro de subsistema funciona.

### Troubleshooting rápido (Actions)

- **Falha no `pytest`**: normalmente dependência ausente ou import path; rode localmente `pip install -r requirements.txt && pytest -q`.
- **Docker não publicou em PR**: esperado. Em PR ele só builda; publish acontece no push do branch padrão.
- **Falha no push GHCR**: confira permissões `packages: write` e push direto no branch padrão.
- **Deploy sobe, mas tela vazia**: geralmente `fact_ena.parquet` não gerado; rode `python main.py --stage all` antes.
- **`ModuleNotFoundError: duckdb` no Streamlit**: atualize para o último commit e redeploy; o dashboard já foi ajustado para ler parquet com `pandas` sem depender de `duckdb` em runtime.

## 9) Tela “Choose a registry” no GitHub Packages (normal)

Se você está vendo a página com cards (`npm`, `Containers`, `NuGet` etc.), isso significa apenas que **ainda não existe pacote publicado** na conta/repo.

Para o pacote `Containers` aparecer:

1. Faça um commit/push no branch padrão (`main` ou `master`).
2. Aguarde o workflow terminar com ✅ no job `docker`.
3. Abra o pacote em:
   - `https://github.com/<owner>?tab=packages&repo_name=Energy-Data-Pipeline`
   - ou no repositório: **Packages**.
4. Verifique se existe a imagem:
   - `ghcr.io/<owner>/energy-data-pipeline:latest`

Se não aparecer, revise:
- `Settings → Actions → General` (workflow permissions read/write),
- permissões de package (`packages: write` no workflow),
- branch do push (precisa ser o branch padrão).
