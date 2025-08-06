# Desabilitar áudio completamente
import disable_audio

import discord
from discord.ext import commands
import json
from datetime import datetime

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Carregar configurações - Prioridade para variáveis de ambiente
def load_config():
    # Tentar carregar de variáveis de ambiente primeiro
    if os.getenv('DISCORD_TOKEN'):
        config = {
            'token': os.getenv('DISCORD_TOKEN'),
            'guild_id': int(os.getenv('GUILD_ID', '0')),
            'whitelist_channel_id': int(os.getenv('WHITELIST_CHANNEL_ID', '0')),
            'whitelist_team_channel_id': int(os.getenv('WHITELIST_TEAM_CHANNEL_ID', '0')),
            'whitelist_role_id': int(os.getenv('WHITELIST_ROLE_ID', '0')),
            'questions': [
                "Qual é o seu nome completo?",
                "Qual é a sua idade?",
                "Você já jogou roleplay antes? Se sim, conte sua experiência.",
                "O que você entende por roleplay?",
                "Como você se comportaria em uma situação de conflito no jogo?",
                "Você tem disponibilidade para jogar regularmente?",
                "Qual é o seu horário de jogo preferido?",
                "Você tem microfone e fone de ouvido?",
                "Como você se comunicaria com outros jogadores?",
                "Você conhece as regras básicas de roleplay?",
                "O que você faria se visse alguém quebrando as regras?",
                "Como você contribuiria para a comunidade?",
                "Você tem experiência com jogos de simulação?",
                "Como você lidaria com situações estressantes no jogo?",
                "Você está disposto a aprender e melhorar?",
                "Qual é sua motivação para entrar na whitelist?",
                "Como você se vê contribuindo para o roleplay da cidade?",
                "Você tem algum personagem em mente? Se sim, descreva-o.",
                "Como você reagiria a críticas construtivas?",
                "Você tem alguma dúvida sobre o servidor ou as regras?"
            ]
        }
        print("✅ Configuração carregada de variáveis de ambiente")
        return config
    else:
        # Fallback para config.json (desenvolvimento local)
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                print("✅ Configuração carregada de config.json")
                return config
        except FileNotFoundError:
            # Configuração padrão para desenvolvimento
            config = {
                'token': 'SEU_TOKEN_AQUI',  # Configure via variável de ambiente DISCORD_TOKEN
                'guild_id': 0,  # Configure via variável de ambiente GUILD_ID
                'whitelist_channel_id': 0,  # Configure via variável de ambiente WHITELIST_CHANNEL_ID
                'whitelist_team_channel_id': 0,  # Configure via variável de ambiente WHITELIST_TEAM_CHANNEL_ID
                'whitelist_role_id': 0,  # Configure via variável de ambiente WHITELIST_ROLE_ID
                'questions': [
                    "Qual é o seu nome completo?",
                    "Qual é a sua idade?",
                    "Você já jogou roleplay antes? Se sim, conte sua experiência.",
                    "O que você entende por roleplay?",
                    "Como você se comportaria em uma situação de conflito no jogo?",
                    "Você tem disponibilidade para jogar regularmente?",
                    "Qual é o seu horário de jogo preferido?",
                    "Você tem microfone e fone de ouvido?",
                    "Como você se comunicaria com outros jogadores?",
                    "Você conhece as regras básicas de roleplay?",
                    "O que você faria se visse alguém quebrando as regras?",
                    "Como você contribuiria para a comunidade?",
                    "Você tem experiência com jogos de simulação?",
                    "Como você lidaria com situações estressantes no jogo?",
                    "Você está disposto a aprender e melhorar?",
                    "Qual é sua motivação para entrar na whitelist?",
                    "Como você se vê contribuindo para o roleplay da cidade?",
                    "Você tem algum personagem em mente? Se sim, descreva-o.",
                    "Como você reagiria a críticas construtivas?",
                    "Você tem alguma dúvida sobre o servidor ou as regras?"
                ]
            }
            print("✅ Configuração padrão carregada")
            return config
        except json.JSONDecodeError as e:
            print(f"❌ Erro no formato do config.json: {e}")
            exit(1)
        except Exception as e:
            print(f"❌ Erro ao carregar config.json: {e}")
            exit(1)

# Carregar configurações
config = load_config()

# Dicionário para armazenar sessões de whitelist ativas
active_sessions = {}

class WhitelistSession:
    def __init__(self, user_id, channel_id):
        self.user_id = user_id
        self.channel_id = channel_id
        self.current_question = 0
        self.current_message = None
        self.answers = []
        self.questions = config['questions']

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print(f'ID do Bot: {bot.user.id}')
    print('------')
    
    # Debug: Verificar servidores e canais
    await debug_channels()
    
    # Enviar embed de whitelist no canal de anúncios automaticamente
    await send_whitelist_embed()

async def debug_channels():
    """Função para debugar canais e servidores"""
    print("🔍 DEBUG: Verificando servidores e canais...")
    
    # Verificar se o bot está no servidor correto
    guild = bot.get_guild(int(config['guild_id']))
    if guild:
        print(f"✅ Servidor encontrado: {guild.name} ({guild.id})")
        
        # Listar todos os canais que o bot pode ver
        print("📋 Canais disponíveis:")
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                print(f"  - {channel.name} (ID: {channel.id})")
        
        # Verificar o canal específico
        target_channel = guild.get_channel(int(config['whitelist_channel_id']))
        if target_channel:
            print(f"✅ Canal de whitelist encontrado: {target_channel.name}")
        else:
            print(f"❌ Canal de whitelist NÃO encontrado! ID: {config['whitelist_channel_id']}")
            
    else:
        print(f"❌ Servidor não encontrado! ID: {config['guild_id']}")
        print("📋 Servidores onde o bot está presente:")
        for guild in bot.guilds:
            print(f"  - {guild.name} (ID: {guild.id})")
    
    print("------")

async def send_whitelist_embed():
    """Envia o embed principal de whitelist no canal de anúncios"""
    try:
        channel = bot.get_channel(config['whitelist_channel_id'])
        if not channel:
            print(f"❌ Canal de anúncios não encontrado! ID: {config['whitelist_channel_id']}")
            return
        
        print(f"✅ Canal encontrado: {channel.name} ({channel.id})")
        
        embed = discord.Embed(
            title="🏛️ Sistema de Whitelist - World City Roleplay",
            description="Esse servidor possui sistema de **WHITELIST SEMI-AUTOMÁTICO**. Uma maneira fácil, prática e rápida de entrar na whitelist.",
            color=0x5865F2,
            timestamp=datetime.now()
        )

        # Seção "Como Utilizar"
        embed.add_field(
            name="📋 COMO UTILIZAR:",
            value="• Para iniciar sua whitelist, clique no botão **INICIAR WHITELIST**\n"
                  "• Você será redirecionado para um chat privado com o bot\n"
                  "• Responda todas as perguntas com detalhes e sinceridade\n"
                  "• Aguarde a revisão da equipe (24-48 horas)",
            inline=False
        )

        # Seção "Informações Importantes"
        embed.add_field(
            name="⚠️ INFORMAÇÕES IMPORTANTES:",
            value="• Tenha paciência durante o processo\n"
                  "• Responda todas as perguntas com detalhes\n"
                  "• Mantenha-se ativo no Discord\n"
                  "• Respeite todos os membros da equipe\n"
                  "• Leia as regras do servidor antes de iniciar\n"
                  "• O sistema conta com revisão automática pela equipe",
            inline=False
        )

        embed.set_footer(text="World City Roleplay • Sistema de Whitelist Automático", icon_url=bot.user.avatar.url if bot.user.avatar else None)

        # Criar botão usando discord.ui
        class WhitelistView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
            
            @discord.ui.button(label="Iniciar Whitelist", style=discord.ButtonStyle.primary, emoji="📝")
            async def start_whitelist(self, interaction: discord.Interaction, button: discord.ui.Button):
                await handle_whitelist_start(interaction)
        
        await channel.send(embed=embed, view=WhitelistView())
        print("✅ Embed enviado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao enviar embed: {e}")

async def handle_whitelist_start(interaction):
    """Manipula o início da whitelist"""
    try:
        user = interaction.user
        print(f"🎯 Usuário {user.name} ({user.id}) iniciou whitelist")
        
        # Verificar se o usuário já tem uma sessão ativa
        if user.id in active_sessions:
            embed = discord.Embed(
                title="❌ Sessão Ativa",
                description="Você já possui uma sessão de whitelist ativa. Aguarde a conclusão ou entre em contato com a equipe.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Criar DM com o usuário
        try:
            dm_channel = await user.create_dm()
            print(f"✅ DM criada para {user.name}")
            
            # Iniciar sessão
            session = WhitelistSession(user.id, dm_channel.id)
            active_sessions[user.id] = session
            print(f"✅ Sessão iniciada para {user.name}")
            
            # Em DMs não é possível limpar mensagens antigas
            print(f"📋 Iniciando nova sessão de whitelist para {user.name}")
            
            # Enviar primeira pergunta imediatamente
            embed = discord.Embed(
                title="🎯 Iniciando Whitelist",
                description="Olá! Bem-vindo ao processo de whitelist da World City Roleplay.\n\n"
                           "Vou fazer algumas perguntas para conhecer você melhor. "
                           "Responda cada pergunta com detalhes e sinceridade.\n\n"
                           "**Vamos começar!**",
                color=0x00FF00
            )
            embed.set_footer(text="Responda a pergunta abaixo")
            
            await dm_channel.send(embed=embed)
            print(f"✅ Mensagem inicial enviada para {user.name}")
            
            # Enviar primeira pergunta imediatamente
            print(f"📝 Enviando primeira pergunta para {user.name}")
            await send_next_question(session)
            
            # Confirmar para o usuário (com tratamento de erro)
            try:
                confirm_embed = discord.Embed(
                    title="✅ Whitelist Iniciada",
                    description="Verifique suas mensagens privadas para continuar o processo de whitelist.",
                    color=0x00FF00
                )
                await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
            except Exception as e:
                print(f"⚠️ Erro ao confirmar interação: {e}")
                # Tentar enviar como followup se a interação já expirou
                try:
                    await interaction.followup.send(embed=confirm_embed, ephemeral=True)
                except:
                    pass
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível enviar mensagem privada. Verifique se suas DMs estão abertas.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"❌ DMs fechadas para {user.name}")
            
    except Exception as e:
        print(f"❌ Erro no processo de whitelist: {e}")
        try:
            embed = discord.Embed(
                title="❌ Erro Interno",
                description="Ocorreu um erro interno. Tente novamente ou entre em contato com a equipe.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass

async def send_next_question(session):
    """Envia a próxima pergunta para o usuário"""
    if session.current_question >= len(session.questions):
        await finish_whitelist(session)
        return
    
    question = session.questions[session.current_question]
    
    embed = discord.Embed(
        title=f"❓ Pergunta {session.current_question + 1}",
        description=question,
        color=0x0099FF
    )
    embed.set_footer(text="Responda com sua resposta detalhada")
    
    channel = bot.get_channel(session.channel_id)
    if channel:
        # Sempre enviar uma nova mensagem (mais confiável em DMs)
        session.current_message = await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Verificar se é uma DM e se o usuário tem uma sessão ativa
    if isinstance(message.channel, discord.DMChannel):
        user_id = message.author.id
        if user_id in active_sessions:
            session = active_sessions[user_id]
            print(f"💬 DM recebida de {message.author.name}: {message.content[:50]}...")
            
            # Processar resposta da pergunta atual
            print(f"📊 Progresso: {session.current_question + 1}/{len(session.questions)}")
            
            # Armazenar resposta
            session.answers.append(message.content)
            session.current_question += 1
            
            print(f"✅ Resposta armazenada. Próxima pergunta: {session.current_question}")
            
            # Em DMs não é possível apagar mensagens do usuário
            # Mas podemos apagar nossas próprias mensagens para manter o chat limpo
            print(f"📝 Resposta coletada: {message.content[:50]}...")
            
            # Apagar a mensagem anterior do bot para manter o chat limpo
            channel = bot.get_channel(session.channel_id)
            if channel and session.current_message:
                try:
                    await session.current_message.delete()
                    print(f"🧹 Mensagem anterior do bot apagada")
                except Exception as e:
                    print(f"⚠️ Não foi possível apagar mensagem anterior: {e}")
            
            # Verificar se ainda há perguntas para responder
            if session.current_question < len(session.questions):
                print(f"📝 Enviando pergunta {session.current_question + 1}")
                await send_next_question(session)
            elif session.current_question == len(session.questions):
                # Só finalizar quando responder a última pergunta
                print(f"🎯 Última pergunta respondida! Finalizando whitelist...")
                await finish_whitelist(session)
    
    await bot.process_commands(message)

async def finish_whitelist(session):
    """Finaliza o processo de whitelist e envia para a equipe"""
    user = bot.get_user(session.user_id)
    if not user:
        print(f"❌ Usuário não encontrado: {session.user_id}")
        return
    
    print(f"🎯 Finalizando whitelist para {user.name} - {len(session.answers)} respostas")
    
    # Enviar mensagem de conclusão para o usuário
    embed = discord.Embed(
        title="✅ Whitelist Concluída",
        description="Obrigado por responder todas as perguntas!\n\n"
                   "Sua whitelist foi enviada para a equipe de revisão. "
                   "Você receberá uma notificação em até 48 horas com o resultado.\n\n"
                   "**Aguarde pacientemente!**",
        color=0x00FF00
    )
    embed.set_footer(text="World City Roleplay")
    
    channel = bot.get_channel(session.channel_id)
    if channel:
        # Apagar a mensagem anterior do bot
        if session.current_message:
            try:
                await session.current_message.delete()
                print(f"🧹 Mensagem anterior do bot apagada")
            except Exception as e:
                print(f"⚠️ Não foi possível apagar mensagem anterior: {e}")
        
        # Enviar nova mensagem de conclusão
        await channel.send(embed=embed)
        print(f"✅ Mensagem de conclusão enviada para {user.name}")
    
    # Enviar para a equipe de whitelist
    print(f"📤 Enviando whitelist para equipe...")
    await send_to_team(session, user)

async def send_to_team(session, user):
    """Envia a whitelist para a equipe de revisão"""
    print(f"🔍 Enviando whitelist para equipe - Usuário: {user.name}")
    
    team_channel = bot.get_channel(config['whitelist_team_channel_id'])
    if not team_channel:
        print(f"❌ Canal da equipe não encontrado! ID: {config['whitelist_team_channel_id']}")
        return
    
    print(f"✅ Canal da equipe encontrado: {team_channel.name}")
    
    # Criar embed com todas as respostas
    embed = discord.Embed(
        title=f"📋 Nova Whitelist - {user.name}",
        description=f"**Usuário:** {user.mention} ({user.id})\n"
                   f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
                   f"**Status:** Aguardando Revisão\n\n"
                   f"**Equipe de Whitelist:** <@&{config['whitelist_role_id']}>",
        color=0xFFA500
    )
    
    print(f"📝 Adicionando {len(session.answers)} respostas ao embed")
    
    # Adicionar respostas
    if len(session.answers) != len(config['questions']):
        print(f"❌ Número de respostas ({len(session.answers)}) não corresponde ao número de perguntas ({len(config['questions'])})")
        return
    
    for i, (question, answer) in enumerate(zip(config['questions'], session.answers)):
        # Truncar resposta se for muito longa
        if len(answer) > 1024:
            answer = answer[:1021] + "..."
        
        embed.add_field(
            name=f"❓ Pergunta {i+1}",
            value=f"**Pergunta:** {question}\n\n**Resposta:** {answer}",
            inline=False
        )
        print(f"✅ Adicionada pergunta {i+1}: {question[:50]}...")
    
    embed.set_footer(text="Use os botões abaixo para aprovar ou reprovar")
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    
    # Criar botões de aprovação/reprovação
    class WhitelistReviewView(discord.ui.View):
        def __init__(self, session, user):
            super().__init__(timeout=None)
            self.session = session
            self.user = user
            print(f"🔘 Criando botões para {user.name}")
        
        @discord.ui.button(label="✅ Aprovar", style=discord.ButtonStyle.success, emoji="✅")
        async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            print(f"🔘 Botão Aprovar clicado por {interaction.user.name}")
            try:
                # Verificar se o usuário tem permissão
                if config['whitelist_role_id'] not in [role.id for role in interaction.user.roles]:
                    await interaction.response.send_message("❌ Você não tem permissão para aprovar whitelists.", ephemeral=True)
                    return
                
                await approve_whitelist(self.session, self.user)
                await interaction.response.send_message("✅ Whitelist aprovada com sucesso!", ephemeral=True)
                
                # Remover sessão
                if self.session.user_id in active_sessions:
                    del active_sessions[self.session.user_id]
            except Exception as e:
                print(f"❌ Erro ao aprovar whitelist: {e}")
                await interaction.response.send_message("❌ Erro interno ao aprovar whitelist.", ephemeral=True)
        
        @discord.ui.button(label="❌ Reprovar", style=discord.ButtonStyle.danger, emoji="❌")
        async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            print(f"🔘 Botão Reprovar clicado por {interaction.user.name}")
            try:
                # Verificar se o usuário tem permissão
                if config['whitelist_role_id'] not in [role.id for role in interaction.user.roles]:
                    await interaction.response.send_message("❌ Você não tem permissão para reprovar whitelists.", ephemeral=True)
                    return
                
                await reject_whitelist(self.session, self.user)
                await interaction.response.send_message("❌ Whitelist reprovada.", ephemeral=True)
                
                # Remover sessão
                if self.session.user_id in active_sessions:
                    del active_sessions[self.session.user_id]
            except Exception as e:
                print(f"❌ Erro ao reprovar whitelist: {e}")
                await interaction.response.send_message("❌ Erro interno ao reprovar whitelist.", ephemeral=True)
    
    # Enviar mensagem com botões
    mention_text = f"<@&{config['whitelist_role_id']}> - Nova whitelist para revisão!"
    print(f"📤 Enviando mensagem para equipe: {mention_text}")
    
    try:
        await team_channel.send(content=mention_text, embed=embed, view=WhitelistReviewView(session, user))
        print("✅ Mensagem enviada com sucesso para a equipe!")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para equipe: {e}")

# Sistema de reações removido - agora usa botões

async def approve_whitelist(session, user):
    """Aprova a whitelist do usuário"""
    embed = discord.Embed(
        title="🎉 Whitelist Aprovada!",
        description="Parabéns! Sua whitelist foi **APROVADA** pela equipe!\n\n"
                   "Você agora pode acessar o servidor e começar sua jornada na World City Roleplay.\n\n"
                   "**Bem-vindo à comunidade!**",
        color=0x00FF00
    )
    embed.set_footer(text="World City Roleplay")
    
    # Enviar DM para o usuário
    try:
        await user.send(embed=embed)
        print(f"✅ DM de aprovação enviada para {user.name}")
    except discord.Forbidden:
        print(f"❌ DMs fechadas para {user.name}")
    except Exception as e:
        print(f"❌ Erro ao enviar DM para {user.name}: {e}")
    
    # Notificar no canal da equipe
    team_channel = bot.get_channel(config['whitelist_team_channel_id'])
    if team_channel:
        notification = discord.Embed(
            title="✅ Whitelist Aprovada",
            description=f"A whitelist de {user.mention} foi aprovada.",
            color=0x00FF00
        )
        await team_channel.send(embed=notification)

async def reject_whitelist(session, user):
    """Rejeita a whitelist do usuário"""
    embed = discord.Embed(
        title="❌ Whitelist Reprovada",
        description="Infelizmente sua whitelist foi **REPROVADA** pela equipe.\n\n"
                   "Você pode tentar novamente em 30 dias, melhorando suas respostas.\n\n"
                   "**Obrigado pelo interesse!**",
        color=0xFF0000
    )
    embed.set_footer(text="World City Roleplay")
    
    # Enviar DM para o usuário
    try:
        await user.send(embed=embed)
        print(f"✅ DM de reprovação enviada para {user.name}")
    except discord.Forbidden:
        print(f"❌ DMs fechadas para {user.name}")
    except Exception as e:
        print(f"❌ Erro ao enviar DM para {user.name}: {e}")
    
    # Notificar no canal da equipe
    team_channel = bot.get_channel(config['whitelist_team_channel_id'])
    if team_channel:
        notification = discord.Embed(
            title="❌ Whitelist Reprovada",
            description=f"A whitelist de {user.mention} foi reprovada.",
            color=0xFF0000
        )
        await team_channel.send(embed=notification)

# Comando para configurar o sistema de whitelist
@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_whitelist(ctx):
    """Configura o sistema de whitelist no canal de anúncios"""
    await send_whitelist_embed()
    await ctx.send("✅ Sistema de whitelist configurado com sucesso!")

# Comando para reenviar o embed de whitelist
@bot.command(name='whitelist')
@commands.has_permissions(administrator=True)
async def resend_whitelist(ctx):
    """Reenvia o embed de whitelist no canal de anúncios"""
    await send_whitelist_embed()
    await ctx.send("✅ Embed de whitelist reenviado!")

# Comando para verificar configurações
@bot.command(name='verificar')
@commands.has_permissions(administrator=True)
async def check_config(ctx):
    """Verifica as configurações do bot"""
    embed = discord.Embed(
        title="🔍 Verificação de Configurações",
        color=0x0099FF
    )
    
    # Verificar canal de anúncios
    channel = bot.get_channel(config['whitelist_channel_id'])
    if channel:
        embed.add_field(
            name="✅ Canal de Anúncios",
            value=f"Nome: {channel.name}\nID: {channel.id}",
            inline=False
        )
    else:
        embed.add_field(
            name="❌ Canal de Anúncios",
            value=f"ID não encontrado: {config['whitelist_channel_id']}",
            inline=False
        )
    
    # Verificar canal da equipe
    team_channel = bot.get_channel(config['whitelist_team_channel_id'])
    if team_channel:
        embed.add_field(
            name="✅ Canal da Equipe",
            value=f"Nome: {team_channel.name}\nID: {team_channel.id}",
            inline=False
        )
    else:
        embed.add_field(
            name="❌ Canal da Equipe",
            value=f"ID não encontrado: {config['whitelist_team_channel_id']}",
            inline=False
        )
    
    # Verificar cargo da equipe
    guild = bot.get_guild(config['guild_id'])
    if guild:
        role = guild.get_role(config['whitelist_role_id'])
        if role:
            embed.add_field(
                name="✅ Cargo da Equipe",
                value=f"Nome: {role.name}\nID: {role.id}",
                inline=False
            )
        else:
            embed.add_field(
                name="❌ Cargo da Equipe",
                value=f"ID não encontrado: {config['whitelist_role_id']}",
                inline=False
            )
    else:
        embed.add_field(
            name="❌ Servidor",
            value=f"ID não encontrado: {config['guild_id']}",
            inline=False
        )
    
    embed.add_field(
        name="📊 Estatísticas",
        value=f"Sessões ativas: {len(active_sessions)}\nPerguntas configuradas: {len(config['questions'])}",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Comando para limpar sessões ativas
@bot.command(name='limpar_sessoes')
@commands.has_permissions(administrator=True)
async def clear_sessions(ctx):
    """Limpa todas as sessões ativas"""
    global active_sessions
    count = len(active_sessions)
    active_sessions.clear()
    await ctx.send(f"✅ {count} sessões foram limpas!")

# Executar o bot
if __name__ == "__main__":
    token = config['token']
    bot.run(token) 