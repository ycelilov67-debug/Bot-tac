# Gereksinimler: discord.py 2.x, aiohttp, flask
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
import re
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ----------------- AYARLAR (KENDİ DEĞERLERİNİZİ YERİNE KOYUN) -----------------
# ⚠️ GÜVENLİĞİNİZ İÇİN BU DEĞERLERİ KİMSEYLE PAYLAŞMAYIN!
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ROBLOX_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoEEAQYASIcCgRkdWlkEhQxNjE0NDExMjQwOTU3MTAwNTcyMiIVCgV1bmFtZRIMVFJBUlVUQkVCT1QxIhIKA3VpZBILMTA5MTEwOTE1MjcoAw.8G-o281mMdCMqIHh-YKlIxnP80sr2n5xvFWc4RCrrf7rXj0SMz6mlnKXW8tuXGEv1kUzYKMpPSpg_i_hyZSgqMq7VjtdnkKSjib-SfaoAJG6u3nmFdC9i22_0z99uEVSoyaXJbY2jb1aPUdLpmNEVG5nmGVIqd5a3iHciciH6D-A8aTw4Yzw9f1gr3eZQKU9G169K10bHYax3NyP_xcSv3HXgf64EwzbZJgYtHQRH3_BnBc2YMo9rfFzHO9sm2zhyIoqkqGvWRyzwq_HTBdfzNEv5EScwc6EMt4r0aLLBworpY3AZ9dFZ0PxD6UA6YY3GNTVZu4dNIsQ4o32X_oJi6_CoVfLcqMBl6p4wnnvOXZJ92YLjY_oHv9m8-FDmyXIc-ilxa_iG_c5t3mCz8umW0FDo-ILtQrvkcncZNa94D00VKi08J-E76N-hCXA9zqJLpF1ykMbEFbJeJkbtKu-ItjtNg9IoWqKeqoK11Vh8Rp39hRkQdB8Morq4yfuScB6vJUjt3imbh0XI2dLNS-sgoGoTUvkLqh7JcJf7ngTrcClTgab6uUWRjFmmk6MFJMevlrV78EdyBmNZcK5rbc_Ust-BPLRIki7_iYCHBwOu_7weXYbfQs7VX1ghzMJejqF5HtwLpgLWZktW4KeJEx6QWnquomyWCUA_Yzlok6fv4a8KWkilwKUZ7cyZQbfHXmfiVwUm_QP-uAompu5rb4Eh-r41OVp0tTG9fKqSiD2-SDIPgPsmX1Qn-TQS4ov2s4QRQYCQVL0WfAC7bGNH4Jos8iSWG9_iCretek1AfZfJoWDikzB0ZwHfPNqG_JrVmvhh-lLZXNDOSOKsW-5U65HenolqDjuPYoX1a1B6jw2CyE.VEoR8vTG2YdI0sUhUEaKM6NLKB0"

GROUP_ID = 33158504               # Roblox Grup ID'niz
PLACE_ID = 119353056891810         # Aktiflik sorgusu için birincil Oyun ID'si
PLACE_LABEL = "TAC"               # Oyunun kısaltma/görünecek ismi (Örn: BTF)
LOG_CHANNEL_ID = 1546405253920858122    # Logların gönderileceği kanalın ID'si

# Komutları kullanabilmek için sahip olunması gereken EN DÜŞÜK Roblox Rank Değeri (0-254)
MIN_REQUIRED_RANK = 30 

# RÜTBE VERİTABANI MAPPING SİSTEMİ
RANK_MAPPING = {
    0: {"code": "", "name": "Guest"},

1: {"code": "OR-1", "name": "Er"},
2: {"code": "OR-2", "name": "Onbaşı"},
3: {"code": "OR-3", "name": "Uzman Onbaşı"},
4: {"code": "OR-4", "name": "Çavuş"},
5: {"code": "OR-5", "name": "Uzman Çavuş"},
6: {"code": "OR-6", "name": "Astsubay Çavuş"},
7: {"code": "OR-7", "name": "Astsubay Üstçavuş"},
8: {"code": "OR-8", "name": "Astsubay Başçavuş"},
9: {"code": "OR-9", "name": "Astsubay Kıdemli Başçavuş"},

10: {"code": "OF-1/A", "name": "Asteğmen"},
11: {"code": "OF-1/B", "name": "Teğmen"},
12: {"code": "OF-1/C", "name": "Üsteğmen"},
13: {"code": "OF-2", "name": "Yüzbaşı"},
14: {"code": "OF-3", "name": "Binbaşı"},
15: {"code": "OF-4", "name": "Yarbay"},
16: {"code": "OF-5", "name": "Albay"},
17: {"code": "OF-6", "name": "Tuğgeneral"},
18: {"code": "OF-7", "name": "Tümgeneral"},
19: {"code": "OF-8", "name": "Korgeneral"},
20: {"code": "OF-9", "name": "Orgeneral"},

21: {"code": "", "name": "Büyük Konsey"},
22: {"code": "", "name": "Ankara Heyeti"},
23: {"code": "", "name": "Yönetim Kurulu"},
24: {"code": "", "name": "Yönetim Kurulu Başkanı"},
25: {"code": "", "name": "Yüksek Askeri Şura"},
26: {"code": "", "name": "Genelkurmay"},
27: {"code": "", "name": "GenelKurmay Başkanı"},
28: {"code": "", "name": "Başkumandan"},
29: {"code": "", "name": "Lider"},
30: {"code": "", "name": "Yönetim Kurulu"},
31: {"code": "", "name": "Yönetim Kurulu Başkan Yardımcısı"},
32: {"code": "", "name": "Yönetim Kurulu"},
33: {"code": "", "name": "Başkomutan"},

34: {"code": "", "name": "Yardımcı Grup Sahibi"},
37: {"code": "", "name": "OF-10 Mareşal"},
38: {"code": "", "name": "Grup Sahibi"},
99: {"code": "", "name": "Holder"},
197: {"code": "", "name": "Developer"},
255: {"code": "", "name": "TAC"},
}
# --------------------------------------------------------------------------

HTTP_TIMEOUT = 12
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def ensure_session():
    if not hasattr(bot, "http_session") or bot.http_session.closed:
        bot.http_session = aiohttp.ClientSession()
    return bot.http_session

async def aio_request(method, url, *, json_data=None, headers=None, params=None):
    session = await ensure_session()
    try:
        tm = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
        async with session.request(method, url, json=json_data, headers=headers, params=params, timeout=tm) as resp:
            if resp.status in (200, 201, 204):
                try: return await resp.json()
                except: return await resp.text()
            return resp
    except Exception:
        return None

# ---------- ROBLOX API YARDIMCILARI ----------
def _normalize_cookie(cookie: str) -> str:
    c = cookie.strip()
    if not c.startswith(".ROBLOSECURITY="):
        return f".ROBLOSECURITY={c}"
    return c

async def roblox_get_userid_by_username(username: str):
    username = str(username).strip()
    if not username: return None
    res = await aio_request("POST", "https://users.roblox.com/v1/usernames/users", json_data={"usernames": [username], "excludeBannedUsers": True})
    if isinstance(res, dict) and res.get("data"):
        return str(res["data"][0]["id"])
    return None

async def roblox_get_member_role_in_group(user_id: str, group_id: int):
    res = await aio_request("GET", f"https://groups.roblox.com/v1/users/{user_id}/groups/roles")
    if isinstance(res, dict) and res.get("data"):
        for g in res["data"]:
            if str(g.get("group", {}).get("id", "")) == str(group_id):
                return g.get("role", {})
    return None

async def roblox_change_rank(cookie: str, group_id: int, target_user_id: str, target_role_id: int):
    cookie_norm = _normalize_cookie(cookie)
    url = f"https://groups.roblox.com/v1/groups/{group_id}/users/{target_user_id}"
    headers = {"Cookie": cookie_norm, "Content-Type": "application/json"}
    
    session = await ensure_session()
    async with session.patch(url, json={"roleId": int(target_role_id)}, headers=headers) as resp:
        if resp.status in (401, 403):
            token = resp.headers.get("x-csrf-token")
            if token:
                headers["x-csrf-token"] = token
                async with session.patch(url, json={"roleId": int(target_role_id)}, headers=headers) as resp2:
                    return resp2.status in (200, 204)
        return resp.status in (200, 204)

async def _get_active_players(place_id: int):
    try:
        u_res = await aio_request("GET", f"https://apis.roblox.com/universes/v1/places/{place_id}/universe")
        if isinstance(u_res, dict) and u_res.get("universeId"):
            uid = u_res["universeId"]
            g_res = await aio_request("GET", f"https://games.roblox.com/v1/games?universeIds={uid}")
            if isinstance(g_res, dict) and g_res.get("data"):
                return g_res["data"][0].get("playing", 0)
    except: pass
    return 0

# ---------- YETKİ VE FORMATLAMA KONTROLÜ ----------
def format_rank_string(rank_number: int, default_name: str) -> str:
    cfg = RANK_MAPPING.get(int(rank_number))
    if cfg:
        return f"{cfg['code']} {cfg['name']} ({rank_number})"
    return f"{default_name} ({rank_number})"

async def check_authority(interaction: discord.Interaction):
    invoker_name = interaction.user.nick or interaction.user.display_name
    invoker_roblox_id = await roblox_get_userid_by_username(invoker_name)

    if not invoker_roblox_id:
        await interaction.followup.send(f"❌ Roblox hesabınız bulunamadı. Lütfen RoWifi ile doğrulama yaptığınızdan emin olun.", ephemeral=False)
        return None, None

    invoker_role = await roblox_get_member_role_in_group(invoker_roblox_id, GROUP_ID)
    if not invoker_role:
        await interaction.followup.send("❌ Roblox grubunda üye olarak bulunamadınız.", ephemeral=False)
        return None, None

    invoker_rank = int(invoker_role.get("rank", 0))

    if invoker_rank < MIN_REQUIRED_RANK:
        invoker_rank_str = format_rank_string(invoker_rank, invoker_role.get("name", "Yok"))
        min_role_data = RANK_MAPPING.get(MIN_REQUIRED_RANK, {"code": "YETKİLİ", "name": "Rütbe"})
        min_rank_str = f"{min_role_data['code']} {min_role_data['name']} ({MIN_REQUIRED_RANK})"

        err_msg = (
            f"Sizin (**{interaction.user.name}**) rütbe verebilmek için yeterli yetkiniz yok.\n\n"
            f"Sizin rütbeniz: **{invoker_rank_str}**\n"
            f"Sahip olmanız gereken en düşük rütbe: **{min_rank_str}**"
        )
        await interaction.followup.send(err_msg, ephemeral=False)
        return None, None

    return invoker_roblox_id, invoker_rank

async def get_all_group_roles():
    res = await aio_request("GET", f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles")
    if isinstance(res, dict) and res.get("roles"):
        return res["roles"]
    return []


# ---------- BOT OLAYLARI ----------
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
    except Exception as e:
        print("Slash sync hatası:", e)
    await ensure_session()
    print(f"{bot.user} hazır ve aktif!")

# ---------- KOMUTLAR ----------

# RÜTBE SORGU
@bot.tree.command(name="rütbe-sorgu", description="Belirtilen kullanıcının gruptaki rütbesini gösterir.")
@app_commands.describe(roblox_username="Roblox kullanıcı adı")
async def rutbe_sorgu(interaction: discord.Interaction, roblox_username: str):
    target_id = await roblox_get_userid_by_username(roblox_username)
    if not target_id:
        await interaction.response.send_message("❌ Kullanıcı bulunamadı.", ephemeral=True)
        return

    mrole = await roblox_get_member_role_in_group(target_id, GROUP_ID)
    if not mrole:
        await interaction.response.send_message("❌ Kullanıcı grupta değil.", ephemeral=True)
        return

    rank_str = format_rank_string(mrole.get("rank", 0), mrole.get("name", "Yok"))
    
    emb = discord.Embed(
        title="İşlem başarıyla tamamlandı",
        description=f"**{roblox_username} ({target_id})** isimli kişinin rütbesi: **{rank_str}**",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=emb)

# OTOMATİK TAMAMLAMA MOTORU
async def rank_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    choices = []
    for rank_num, info in RANK_MAPPING.items():
        label = f"{info['code']} {info['name']} ({rank_num})"
        if current.lower() in label.lower():
            choices.append(app_commands.Choice(name=label, value=str(rank_num)))
    return choices[:25]

# RÜTBE DEĞİŞTİR
@bot.tree.command(name="rütbe-değiştir", description="Hedef kullanıcının rütbesini değiştirir.")
@app_commands.describe(roblox_username="Roblox kullanıcı adı", rütbe="Verilecek yeni rütbeyi aratıp seçin", sebep="İşlem sebebi")
@app_commands.autocomplete(rütbe=rank_autocomplete)
async def rutbe_degistir(interaction: discord.Interaction, roblox_username: str, rütbe: str, sebep: str):

    await interaction.response.defer(ephemeral=False)

    invoker_id, invoker_rank = await check_authority(interaction)
    if not invoker_id:
        return

    target_id = await roblox_get_userid_by_username(roblox_username)
    if not target_id:
        await interaction.followup.send("❌ Hedef kullanıcı bulunamadı.", ephemeral=False)
        return

    if str(invoker_id) == str(target_id):
        await interaction.followup.send("❌ Kendi rütbenizi değiştiremezsiniz.", ephemeral=False)
        return

    target_role = await roblox_get_member_role_in_group(target_id, GROUP_ID)
    if not target_role:
        await interaction.followup.send("❌ Hedef grupta bulunmuyor.", ephemeral=False)
        return

    current_target_rank = int(target_role.get("rank", 0))
    if current_target_rank >= invoker_rank:
        await interaction.followup.send("❌ Sizden üst veya eşit rütbedeki birine işlem yapamazsınız.", ephemeral=False)
        return

    try:
        new_rank_num = int(rütbe)
    except ValueError:
        sayilar = re.findall(r'\d+', rütbe)
        if sayilar:
            new_rank_num = int(sayilar[-1])
        else:
            await interaction.followup.send("❌ Geçersiz rütbe formatı! Lütfen listeden geçerli bir rütbe seçin.", ephemeral=False)
            return

    if new_rank_num >= invoker_rank:
        await interaction.followup.send("❌ Bir kimseyi kendi rütbenize veya üstünüze ayarlayamazsınız.", ephemeral=False)
        return

    roles = await get_all_group_roles()
    target_role_obj = next((r for r in roles if int(r.get("rank", 0)) == new_rank_num), None)
    if not target_role_obj:
        await interaction.followup.send("❌ Belirtilen rütbe grupta bulunamadı.", ephemeral=False)
        return

    success = await roblox_change_rank(ROBLOX_COOKIE, GROUP_ID, target_id, target_role_obj["id"])
    if success:
        new_rank_str = format_rank_string(new_rank_num, target_role_obj["name"])
        old_rank_str = format_rank_string(current_target_rank, target_role.get("name", "Yok"))

        emb = discord.Embed(
            title="İşlem başarıyla tamamlandı",
            description=f"**{roblox_username} ({target_id})** isimli kişiye **{new_rank_str}** rütbesi başarıyla verildi.\n\nSebep: {sebep}.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=emb, ephemeral=False)

        log_chan = bot.get_channel(LOG_CHANNEL_ID)
        if log_chan:
            log_emb = discord.Embed(title="Rütbe Değişikliği Logu", color=discord.Color.blue())
            log_emb.add_field(name="Kullanıcı", value=f"**{roblox_username}** ({target_id})", inline=False)
            log_emb.add_field(name="Eski Rütbe", value=old_rank_str, inline=True)
            log_emb.add_field(name="Yeni Rütbe", value=new_rank_str, inline=True)
            log_emb.add_field(name="Yetkili", value=f"{interaction.user.mention}", inline=False)
            log_emb.add_field(name="Sebep", value=sebep, inline=False)
            await log_chan.send(embed=log_emb)
    else:
        await interaction.followup.send("❌ Rütbe değiştirme işlemi sırasında bir hata oluştu.", ephemeral=False)


import discord
from discord.ext import commands
from discord import app_commands
import re

# ----------------- ONAY VERECEK 2 KİŞİNİN DİSCORD İD'LERİ -----------------
ONAY_YETKILILERI = [1510340658206998588, 1528788816280813690]  # Buraya yetkililerin gerçek Discord ID'lerini yazın
# --------------------------------------------------------------------------

# Təsdiq düymələri üçün interaktiv View sinfi
class YasaklamaOnayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180) # 3 dəqiqə vaxt
        self.value = None

    @discord.ui.button(label="Təsdiq Et (Banla)", style=discord.ButtonStyle.green, emoji="✅")
    async def onay(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ONAY_YETKILILERI:
            await interaction.response.send_message("❌ Bu düyməni istifadə etmək üçün səlahiyyətiniz yoxdur!", ephemeral=True)
            return
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label="Rədd Et (Ləğv Et)", style=discord.ButtonStyle.red, emoji="❌")
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ONAY_YETKILILERI:
            await interaction.response.send_message("❌ Bu düyməni istifadə etmək üçün səlahiyyətiniz yoxdur!", ephemeral=True)
            return
        await interaction.response.defer()
        self.value = False
        self.stop()


# ---------- TAM YASAKLA KOMUTU ----------
@bot.tree.command(name="tam-yasakla", description="Kullanıcıyı botun bulunduğu tüm sunuculardan banlar ve Roblox rütbesini düşürür.")
@app_commands.describe(
    discord_kullanici="Yasaklanacak kişinin Discord adı, etiketi veya ID'si", 
    sebep="Yasaklama sebebi",
    kanit="İşlem için kanıt (Görsel veya metin linki)",
    roblox_kullanici_adi="Hedefin Roblox kullanıcı adı (Opsiyonel)"
)
async def tam_yasakla(interaction: discord.Interaction, discord_kullanici: str, sebep: str, kanit: str, roblox_kullanici_adi: str = None):
    await interaction.response.defer(ephemeral=False)

    # 1. Yetki ve Rütbe Kontrolü
    invoker_name = interaction.user.nick or interaction.user.display_name
    invoker_roblox_id = await roblox_get_userid_by_username(invoker_name)

    if not invoker_roblox_id:
        await interaction.followup.send("❌ Roblox hesabınız bulunamadı. Lütfen adınızın eşleştiğinden emin olun.", ephemeral=False)
        return

    invoker_role = await roblox_get_member_role_in_group(invoker_roblox_id, GROUP_ID)
    if not invoker_role:
        await interaction.followup.send("❌ Roblox grubunda üye olarak bulunamadınız.", ephemeral=False)
        return

    invoker_rank = int(invoker_role.get("rank", 0))
    MIN_REQUIRED_RANK = 30 # İsteğe göre değiştirebilirsiniz

    if invoker_rank < MIN_REQUIRED_RANK:
        invoker_rank_str = format_rank_string(invoker_rank, invoker_role.get("name", "Yok"))
        min_role_data = RANK_MAPPING.get(MIN_REQUIRED_RANK, {"code": "YETKİLİ", "name": "Yönetim Kurulu"})
        min_rank_str = f"{min_role_data['code']} {min_role_data['name']} ({MIN_REQUIRED_RANK})"

        err_msg = (
            f"Sizin rütbeniz: **{invoker_rank_str}**\n"
            f"Sahip olmanız gereken en düşük rütbe: **{min_rank_str}**"
        )
        await interaction.followup.send(err_msg, ephemeral=False)
        return

    # 2. Girilen metinden Discord kullanıcısını bulma
    hedef_uye = None
    temiz_id = re.findall(r'\d+', discord_kullanici)
    
    if temiz_id:
        try:
            hedef_uye = await bot.fetch_user(int(temiz_id[0]))
        except:
            pass
            
    if not hedef_uye:
        for guild in bot.guilds:
            m = guild.get_member_named(discord_kullanici)
            if m:
                hedef_uye = m
                break

    if not hedef_uye:
        hedef_uye = interaction.guild.get_member_named(discord_kullanici)

    if not hedef_uye:
        await interaction.followup.send(f"❌ **{discord_kullanici}** adında bir Discord kullanıcısı bulunamadı.", ephemeral=False)
        return

    if hedef_uye.id == interaction.user.id:
        await interaction.followup.send("❌ Kendinizi yasaklayamazsınız.", ephemeral=False)
        return

    # 3. Belirtilen 2 Yetkiliye DM ile Onay Gönderme
    talep_embed = discord.Embed(
        title="🚨 Yeni Tam Yasaklama Talebi",
        description=f"**{interaction.user.mention}** adlı yetkili bir kullanıcı için tam yasaklama talebinde bulundu.",
        color=discord.Color.orange()
    )
    talep_embed.add_field(name="Yasaklanacak Üye", value=f"{hedef_uye.mention} (`{hedef_uye.id}`)", inline=False)
    talep_embed.add_field(name="Sebep", value=sebep, inline=False)
    talep_embed.add_field(name="Kanıt", value=kanit, inline=False)
    talep_embed.set_footer(text="İşlemi onaylamak veya reddetmek için aşağıdaki düğmeleri kullanın.")

    view = YasaklamaOnayView()
    
    gonderilen_mesajlar = []
    for yetkili_id in ONAY_YETKILILERI:
        try:
            user_obj = await bot.fetch_user(yetkili_id)
            if user_obj:
                msg = await user_obj.send(embed=talep_embed, view=view)
                gonderilen_mesajlar.append(msg)
        except Exception:
            pass

    if not gonderilen_mesajlar:
        await interaction.followup.send("❌ Belirtilen onay yetkililerine DM gönderilemediği için işlem iptal edildi.", ephemeral=False)
        return

    await interaction.followup.send("⏳ Yasaklama talebi yetkili kişilere DM üzerinden onay için gönderildi. Yanıt bekleniyor...", ephemeral=False)

    await view.wait()

    # Gönderilen DM'lerdeki butonları devre dışı bırakma
    for msg in gonderilen_mesajlar:
        try:
            if view.value is True:
                await msg.edit(content="✅ **Talep Onaylandı ve İşleme Alındı.**", view=None)
            elif view.value is False:
                await msg.edit(content="❌ **Talep Reddedildi.**", view=None)
            else:
                await msg.edit(content="⌛ **Süre aşımı (3 dakika içinde yanıt verilmedi).**", view=None)
        except:
            pass

    if view.value is True:
        pass # İşleme devam et
    elif view.value is False:
        await interaction.followup.send("❌ Yetkililer yasaklama talebini **reddetti**.", ephemeral=False)
        return
    else:
        await interaction.followup.send("❌ Zamanında yanıt verilmediği için talep iptal edildi.", ephemeral=False)
        return

    # 4. Onay Verildikten Sonraki Asıl İşlemler (Roblox + Banlar)
    target_roblox_name = roblox_kullanici_adi or (hedef_uye.nick if hasattr(hedef_uye, 'nick') else None) or hedef_uye.name
    target_id = await roblox_get_userid_by_username(target_roblox_name)
    
    roblox_status_msg = ""
    if target_id:
        target_role = await roblox_get_member_role_in_group(target_id, GROUP_ID)
        if target_role:
            raw_roles = await get_all_group_roles()
            if raw_roles:
                sorted_roles = sorted(raw_roles, key=lambda x: int(x.get("rank", 0)))
                lowest_role_obj = sorted_roles[0]
                success = await roblox_change_rank(ROBLOX_COOKIE, GROUP_ID, target_id, lowest_role_obj["id"])
                if success:
                    new_rank_str = format_rank_string(int(lowest_role_obj["rank"]), lowest_role_obj["name"])
                    roblox_status_msg = f"Roblox grubundaki rütbesi başarıyla **{new_rank_str}** yapıldı."
                else:
                    roblox_status_msg = "Roblox rütbesi değiştirilemedi."
            else:
                roblox_status_msg = "Grup rolleri alınamadı."
        else:
            roblox_status_msg = "Hedef grupta bulunamadı."
    else:
        roblox_status_msg = "Hedefin Roblox hesabı Rowifi ile eşleşmediği için grup rütbesi düşürülemedi."

    # Tüm sunuculardan banlama
    banlanan_sunucular = []
    for guild in bot.guilds:
        try:
            member_obj = guild.get_member(hedef_uye.id) or await guild.fetch_member(hedef_uye.id)
            if member_obj:
                await guild.ban(member_obj, reason=f"Tam Yasaklama | Yetkili: {interaction.user.name} | Sebep: {sebep}")
                banlanan_sunucular.append(guild.name)
        except Exception:
            pass

    # Sunucu listesi formatı
    sunucu_metni = ""
    max_gosterim = 10
    for s in banlanan_sunucular[:max_gosterim]:
        sunucu_metni += f"• {s}\n"
    
    kalan_sayi = len(banlanan_sunucular) - max_gosterim
    if kalan_sayi > 0:
        sunucu_metni += f"\n*...ve {kalan_sayi} sunucuda daha.*"
    elif not sunucu_metni:
        sunucu_metni = "Hiçbir sunucudan banlanamadı."

    # Embed Gönderimi
    emb = discord.Embed(
        title="✅ TAM YASAKLANDI",
        color=discord.Color.green()
    )
    emb.add_field(name="Talep Eden", value=f"{interaction.user.name} (`{interaction.user.id}`)", inline=False)
    emb.add_field(name="Hedef", value=f"{hedef_uye.mention} (`{hedef_uye.id}`)", inline=False)
    emb.add_field(name="Sebep", value=sebep, inline=False)
    emb.add_field(name="Kanıt", value=kanit, inline=False)
    emb.add_field(name=f"Yasaklanan Sunucular ({len(banlanan_sunucular)}):", value=sunucu_metni, inline=False)
    emb.add_field(name="Roblox Grupları", value=roblox_status_msg, inline=False)

    await interaction.followup.send(embed=emb, ephemeral=False)

    # Log Kanalı
    log_chan = bot.get_channel(LOG_CHANNEL_ID)
    if log_chan:
        log_emb = discord.Embed(title="🚨 TAM YASAKLAMA ONAYLANDI VE LOGLANDI", color=discord.Color.dark_red())
        log_emb.add_field(name="Talep Eden", value=f"{interaction.user.mention}", inline=True)
        log_emb.add_field(name="Yasaklanan", value=f"{hedef_uye.mention} (`{hedef_uye.id}`)", inline=True)
        log_emb.add_field(name="Kanıt", value=kanit, inline=False)
        log_emb.add_field(name="Sebep", value=sebep, inline=False)
        log_emb.add_field(name="Roblox Durumu", value=roblox_status_msg, inline=False)
        log_emb.add_field(name="Sunucular", value=f"{len(banlanan_sunucular)} sunucuda uygulandı.", inline=False)
        await log_chan.send(embed=log_emb)

# RÜTBE SAYIMI
async def get_roles(group_id: int):
    url = f"https://groups.roblox.com/v1/groups/{group_id}/roles"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            return data.get("roles", [])


@bot.tree.command(
    name="rutbe-sayimi",
    description="Girilen Roblox grup ID'sindeki tüm rütbeleri ve üye sayılarını gösterir."
)
@app_commands.describe(
    group_id="Roblox grup ID",
    limit="Kaç rütbe gösterilsin"
)
async def rutbe_sayimi(interaction: discord.Interaction, group_id: int, limit: int = 40):
    await interaction.response.defer()

    roles = await get_roles(group_id)
    if not roles:
        return await interaction.followup.send("❌ Roller alınamadı.")

    roles = sorted(
        roles,
        key=lambda x: int(x.get("rank", 0)),
        reverse=True
    )

    text = ""
    for r in roles[:limit]:
        name = r.get("name", "Bilinmiyor")
        rank = r.get("rank", 0)
        count = r.get("memberCount", 0)
        text += f"• **{name}** | `{rank}` | `{count}` üye\n"

    embed = discord.Embed(
        title=f"Rütbe Sayımı — {group_id}",
        description=text if text else "Veri yok.",
        color=0x2b2d31
    )
    embed.set_footer(
        text=f"Sorgulayan: {interaction.user.display_name}"
    )
    await interaction.followup.send(embed=embed)


# ---------- TERFİ / TENZİL MOTORU (GÜVENLİ HALE GETİRİLDİ) ----------
async def relative_rank_change(interaction: discord.Interaction, roblox_username: str, direction: int, sebep: str):
    await interaction.response.defer(ephemeral=False)

    invoker_id, invoker_rank = await check_authority(interaction)
    if not invoker_id: 
        return 

    target_id = await roblox_get_userid_by_username(roblox_username)
    if not target_id:
        await interaction.followup.send("❌ Kullanıcı bulunamadı.", ephemeral=False)
        return

    target_role = await roblox_get_member_role_in_group(target_id, GROUP_ID)
    if not target_role:
        await interaction.followup.send("❌ Hedef grupta değil.", ephemeral=False)
        return

    current_target_rank = int(target_role.get("rank", 0))
    if current_target_rank >= invoker_rank:
        await interaction.followup.send("❌ Sizden üst veya eşit rütbedeki birine işlem yapamazsınız.", ephemeral=False)
        return

    # Tüm grup rütbelerini çekip küçükten büyüğe sıralıyoruz
    raw_roles = await get_all_group_roles()
    if not raw_roles:
        await interaction.followup.send("❌ Grup rütbe listesi API'den çekilemedi.", ephemeral=False)
        return
    
    sorted_roles = sorted(raw_roles, key=lambda x: int(x.get("rank", 0)))

    # Hedef kullanıcının sıralamadaki rütbe indeksini buluyoruz
    current_index = next((i for i, r in enumerate(sorted_roles) if int(r["rank"]) == current_target_rank), None)
    
    if current_index is None:
        await interaction.followup.send("❌ Hedef rütbe mevcut sıralamada bulunamadı.", ephemeral=False)
        return

    # İndeksi yön doğrultusunda kaydırıyoruz (direkt +1/-1 matematiksel rütbe farkı yerine listedeki ardışık elemana geçiyoruz)
    new_index = current_index + direction

    if new_index < 0 or new_index >= len(sorted_roles):
        await interaction.followup.send("❌ Bu işlem sınırların dışına çıkıyor (Zaten en düşük veya en yüksek rütbede).", ephemeral=False)
        return

    target_role_obj = sorted_roles[new_index]
    new_rank_num = int(target_role_obj["rank"])

    if new_rank_num >= invoker_rank:
        await interaction.followup.send("❌ Kullanıcıyı kendi rütbenize veya üstünüze yükseltemezsiniz.", ephemeral=False)
        return

    # Roblox üzerinde rütbe değiştirme işlemi
    success = await roblox_change_rank(ROBLOX_COOKIE, GROUP_ID, target_id, target_role_obj["id"])

    if success:
        new_rank_str = format_rank_string(new_rank_num, target_role_obj["name"])
        old_rank_str = format_rank_string(current_target_rank, target_role.get("name", "Yok"))

        emb = discord.Embed(
            title="İşlem başarıyla tamamlandı",
            description=f"**{roblox_username} ({target_id})** isimli kişiye **{new_rank_str}** rütbesi başarıyla verildi.\n\nSebep: {sebep}.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=emb, ephemeral=False)

        log_chan = bot.get_channel(LOG_CHANNEL_ID)
        if log_chan:
            log_emb = discord.Embed(title="Rütbe Değişikliği Logu", color=discord.Color.blue())
            log_emb.add_field(name="Kullanıcı", value=f"**{roblox_username}** ({target_id})", inline=False)
            log_emb.add_field(name="Eski Rütbe", value=old_rank_str, inline=True)
            log_emb.add_field(name="Yeni Rütbe", value=new_rank_str, inline=True)
            log_emb.add_field(name="Yetkili", value=f"{interaction.user.mention}", inline=False)
            log_emb.add_field(name="Sebep", value=sebep, inline=False)
            await log_chan.send(embed=log_emb)
    else:
        await interaction.followup.send("❌ İşlem başarısız oldu. Roblox API rütbeyi güncelleyemedi.", ephemeral=False)


@bot.tree.command(name="rütbe-terfi", description="Kullanıcıyı bir üst rütbe kademesine terfi ettirir.")
@app_commands.describe(roblox_username="Roblox kullanıcı adı", sebep="Terfi sebebi")
async def rutbe_terfi(interaction: discord.Interaction, roblox_username: str, sebep: str):
    await relative_rank_change(interaction, roblox_username, +1, sebep)


@bot.tree.command(name="rütbe-tenzil", description="Kullanıcının rütbesini bir alt rütbe kademesine düşürür.")
@app_commands.describe(roblox_username="Roblox kullanıcı adı", sebep="Tenzil sebebi")
async def rutbe_tenzil(interaction: discord.Interaction, roblox_username: str, sebep: str):
    await relative_rank_change(interaction, roblox_username, -1, sebep)


# AKTİFLİK SORGU
@bot.tree.command(name="aktiflik-sorgu", description="Ayarlanmış oyunun anlık aktif oyuncu sayısını gösterir.")
async def aktiflik_sorgu(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)

    count = await _get_active_players(PLACE_ID)
    emb = discord.Embed(
        title=f"{PLACE_LABEL} oyununun aktifliği: {count}",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=emb, ephemeral=False)


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Lütfen Render Environment Variables hissəsinə BOT_TOKEN əlavə edin!")
    else:
        keep_alive()  # Flask serverini arxa fonda başladır ki, Render portu görsün
        bot.run(BOT_TOKEN)
