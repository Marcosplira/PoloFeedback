from .models import ConfiguracaoAcademia


def configuracao_academia(request):
    """
    Injeta as configurações white-label da academia em todos os templates.
    Se não houver configuração ativa, utiliza os valores padrão.
    """
    config = ConfiguracaoAcademia.objects.filter(ativo=True).first()
    return {
        "config_academia": config,
        "nome_academia_atual": config.nome_academia if config else "Polo Fit",
        "logo_academia_atual": config.logo.url if (config and config.logo) else None,
        "cor_primaria_atual": config.cor_primaria if config else "#a3e635",
        "cor_secundaria_atual": config.cor_secundaria if config else "#0a0a0a",
        "whatsapp_academia_atual": config.whatsapp if (config and config.whatsapp) else "5583986719438",
        "telefone_academia_atual": config.telefone if (config and config.telefone) else "(83) 98671-9438",
    }
