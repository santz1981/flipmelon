# Flipmelon 🍈

**Seu Android em uma tela maior.** Flipmelon é um aplicativo de controle para Windows, com passo a passo para configurar a conexão USB e usar o espelhamento do Android por meio do [scrcpy](https://github.com/Genymobile/scrcpy).

## Recursos

- Primeira tela: escolha de idioma; **inglês é o padrão**.
- Interface em inglês, português, russo, espanhol e francês.
- Assistente de cinco etapas para habilitar a conexão e configurar o dispositivo.
- Barra de janela personalizada **somente no painel e nas configurações**.
- Logo animado diretamente do `logo.json` com RLottie.
- Espelhamento convencional e opção de tela virtual, conforme suporte do Android.

## Status

**v1.0.8.8** foi validada no Windows pelo mantenedor. O código-fonte mais recente é **v1.0.8.9-beta**, que inclui personalização da janela e idiomas. A nova versão ainda requer teste final no Windows antes de ser tratada como estável.

## Como instalar ou compilar

Quem só quer usar o Flipmelon deve baixar o pacote Windows **em Releases**, quando uma versão verificada estiver publicada. Quem quer desenvolver deve seguir o [guia de build](BUILD_WINDOWS.md).

Este repositório **não inclui** binários proprietários nem executáveis de terceiros no Git. Para compilar, baixe o pacote oficial do scrcpy pelo script `scripts/get-scrcpy.ps1`, que verifica SHA-256, e depois execute `build-windows.bat`.

## Código e marca

O código próprio do Flipmelon está preparado com uma **proposta** de licença MIT a confirmar antes da primeira publicação pública. A marca e as artes são tratadas separadamente em [BRANDING.md](../BRANDING.md). As bibliotecas externas mantêm suas próprias licenças; veja [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

[English README](../README.md) · [Contribuir](../CONTRIBUTING.md) · [Histórico](../CHANGELOG.md)
