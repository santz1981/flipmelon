<div align="center">

<img src="../assets/flipmelon-logo.png" alt="Logo do Flipmelon" width="340" />

### Seu Android em uma tela maior.

Aplicativo open source para **Windows e Linux Mint**, com espelhamento Android por meio do [scrcpy](https://github.com/Genymobile/scrcpy).

[![Windows x64](https://img.shields.io/badge/Windows-x64-DBFF00?style=flat-square&labelColor=111111)](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1) [![Linux Mint x64](https://img.shields.io/badge/Linux_Mint-x64-DBFF00?style=flat-square&labelColor=111111)](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1) [![Beta 1](https://img.shields.io/badge/Vers%C3%A3o-v1.0.8.9--beta.1-DBFF00?style=flat-square&labelColor=111111)](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1) [![MIT](https://img.shields.io/badge/C%C3%B3digo-MIT-DBFF00?style=flat-square&labelColor=111111)](../LICENSE)

[![Baixar para Windows](https://img.shields.io/badge/Baixar_para_Windows-Instalador_Beta-DBFF00?style=for-the-badge&logo=windows11&logoColor=111111)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Windows_Setup_COMPLETE.zip)
[![Baixar para Linux Mint](https://img.shields.io/badge/Baixar_para_Linux_Mint-DEB_Beta-DBFF00?style=for-the-badge&logo=linux&logoColor=111111)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Beta1-2_amd64.deb)

**[Windows portátil](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Portable_Windows.zip)** · **[ZIP Linux](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Linux.zip)** · **[Notas da versão](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1)** · **[English](../README.md)**

</div>

> **Beta:** a v1.0.8.9-beta.1 está disponível para Windows e Linux Mint. O instalador `.deb` foi testado pelo mantenedor no Linux Mint x86-64. Outras distribuições Linux não foram verificadas. Os executáveis Windows **não possuem assinatura digital**; não desative as proteções do sistema.

## O que é o Flipmelon?

O Flipmelon facilita a conexão USB de um celular Android a um computador Windows ou Linux Mint, por meio de um assistente e do [scrcpy](https://github.com/Genymobile/scrcpy), para espelhamento convencional ou tela Android virtual em aparelhos compatíveis. Foi desenvolvido em Python e PySide6. É um aplicativo independente, **não é o Samsung DeX para PC**.

## Recursos

- **Idioma primeiro:** inglês é o padrão para novas instalações, mas o usuário escolhe o idioma antes da configuração do Android.
- **Cinco idiomas:** English, Português, Русский, Español e Français.
- **Assistente de cinco etapas:** opções do desenvolvedor, depuração USB, autorização do aparelho e preferências de exibição.
- **Janela personalizada:** barra superior própria nas telas de passo a passo, painel e configurações; a janela do scrcpy continua nativa.
- **Modos de exibição:** espelhamento convencional ou tela virtual, conforme suporte do Android.
- **Animação Lottie original:** reproduzida com RLottie, sem GIF, MP4 ou Qt WebEngine.
- **Preferências salvas:** idioma e configurações de exibição armazenados localmente.

## Download e instalação

| Arquivo | Para que serve |
| --- | --- |
| **[Instalador Windows (Beta)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Windows_Setup_COMPLETE.zip)** | ZIP com EXE de instalação e dois arquivos BIN |
| **[Windows portátil (Beta)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Portable_Windows.zip)** | Executar sem instalação |
| **[Linux Mint DEB (Beta)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Beta1-2_amd64.deb)** | Instalador para Linux Mint x86-64 |
| **[ZIP Linux (Beta)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Linux.zip)** | Pacote Linux compactado |
| **[SHA-256 Windows](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/SHA256SUMS.txt)** | Verificar downloads do Windows |
| **[SHA-256 Linux](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_Linux_SHA256SUMS.txt)** | Verificar downloads do Linux |

**Requisitos:** Windows 10/11 x64 ou Linux Mint x86-64 (testado), celular Android, cabo USB de dados e depuração USB habilitada. O modo de tela virtual depende do aparelho; outras distribuições Linux ainda não foram verificadas.

### Como instalar no Windows

1. Baixe o [ZIP do instalador Windows](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Windows_Setup_COMPLETE.zip) e **extraia todos os arquivos na mesma pasta**.
2. Mantenha o **EXE junto dos dois arquivos BIN**; não execute o EXE dentro do ZIP.
3. Feche versões anteriores do Flipmelon e do scrcpy.
4. Execute **Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED.exe**.
5. Abra o Flipmelon, escolha o idioma (inglês por padrão) e siga o assistente de configuração.

### Versão portátil do Windows

Extraia o [ZIP portátil](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Portable_Windows.zip), abra a pasta **Flipmelon** e execute **Flipmelon.exe**. Mantenha a pasta completa, incluindo **_internal**.

**Segurança:** os executáveis Windows não são assinados digitalmente e podem gerar avisos de segurança. Não desative as proteções. Relate os avisos em [Issues](https://github.com/santz1981/flipmelon/issues).

### Como instalar no Linux Mint (x86-64)

1. Baixe o [instalador Linux Mint (.deb)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Beta1-2_amd64.deb).
2. Dê dois cliques no arquivo `.deb` e instale pelo gerenciador de pacotes do Mint.
3. Abra o **Flipmelon** pelo menu de aplicativos.
4. Conecte o Android pelo cabo USB, ative a depuração USB e autorize a conexão no celular.

Se preferir instalar pelo terminal, abra-o na pasta em que salvou o arquivo e execute:

```bash
sudo apt install ./Flipmelon_1.0.8.9_Beta1-2_amd64.deb
```

O Linux Mint foi testado pelo mantenedor, mas o aplicativo continua em **Beta**. Outras distribuições Linux ainda não foram verificadas. Também estão disponíveis o [ZIP Linux](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Linux.zip) e os [checksums SHA-256 do Linux](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_Linux_SHA256SUMS.txt).

## Prévia visual

<div align="center">
  <img src="../assets/flipmelon-splash.png" alt="Arte oficial de abertura do Flipmelon, não uma captura do aplicativo" width="680" />
  <p><sub>Arte oficial da splash — não é um screenshot da aplicação. Capturas reais da interface e do espelhamento serão adicionadas após validação visual.</sub></p>
</div>

## Compilar a partir do código-fonte

**Compilação do código-fonte para Windows:** Windows 10/11 x64, Python 3.11+, PowerShell, internet e Inno Setup 6 (opcional).

1. Clone ou baixe este repositório.
2. Siga o [guia de compilação Windows](BUILD_WINDOWS.md) para baixar o scrcpy oficial com verificação SHA-256 pelo script **scripts/get-scrcpy.ps1**.
3. Execute **build-windows.bat**.
4. Teste **dist/Flipmelon/Flipmelon.exe** antes de distribuir.
5. Os pacotes ficam em **output/**.

O pacote `.deb` para Linux Mint x86-64 está publicado e foi testado pelo mantenedor. As instruções de empacotamento Linux ainda não estão documentadas neste repositório. Consulte o [checklist de publicação](RELEASING.md).

## Status e próximos passos

- **v1.0.8.8:** última versão reportada como funcional no Windows pelo mantenedor, incluindo a splash RLottie.
- **v1.0.8.9-beta.1:** versões Windows e Linux Mint publicadas. O instalador `.deb` foi testado no Mint pelo mantenedor. Ainda são necessárias verificações adicionais antes da versão estável.
- **Próximas melhorias:** validar a beta, incluir capturas reais, aperfeiçoar acessibilidade e padronizar a compilação.

Consulte [CHANGELOG.md](../CHANGELOG.md) e [todas as Releases](https://github.com/santz1981/flipmelon/releases).

## Contribuições

Relatos de bugs, traduções e melhorias são bem-vindos. Leia [CONTRIBUTING.md](../CONTRIBUTING.md), consulte as [Issues](https://github.com/santz1981/flipmelon/issues) e [SECURITY.md](../SECURITY.md).

## Licença e créditos

O código-fonte original do Flipmelon está publicado sob a [licença MIT](../LICENSE). O uso da marca e das artes é tratado separadamente em [BRANDING.md](../BRANDING.md), cuja proposta ainda precisa de aprovação final do responsável. Bibliotecas e componentes externos mantêm suas licenças e obrigações de redistribuição: veja [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

O Flipmelon é independente e não possui vínculo nem endosso de Samsung, Google, Genymobile ou Qt.
