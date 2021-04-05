from emoji import UNICODE_EMOJI
from google_trans_new import LANGUAGES, google_translator
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

from MashaRoBot import dispatcher
from MashaRoBot.modules.disable import DisableAbleCommandHandler


@run_async
def totranslate(update: Update, context: CallbackContext):
    message = update.effective_message
    problem_lang_code = []
    for key in LANGUAGES:
        if "-" in key:
            problem_lang_code.append(key)

    try:
        if message.reply_to_message:
            args = update.effective_message.text.split(None, 1)
            if message.reply_to_message.text:
                text = message.reply_to_message.text
            elif message.reply_to_message.caption:
                text = message.reply_to_message.caption

            try:
                source_lang = args[1].split(None, 1)[0]
            except (IndexError, AttributeError):
                source_lang = "id"

        else:
            args = update.effective_message.text.split(None, 2)
            text = args[2]
            source_lang = args[1]

        if source_lang.count("-") == 2:
            for lang in problem_lang_code:
                if lang in source_lang:
                    if source_lang.startswith(lang):
                        dest_lang = source_lang.rsplit("-", 1)[1]
                        source_lang = source_lang.rsplit("-", 1)[0]
                    else:
                        dest_lang = source_lang.split("-", 1)[1]
                        source_lang = source_lang.split("-", 1)[0]
        elif source_lang.count("-") == 1:
            for lang in problem_lang_code:
                if lang in source_lang:
                    dest_lang = source_lang
                    source_lang = None
                    break
            if dest_lang is None:
                dest_lang = source_lang.split("-")[1]
                source_lang = source_lang.split("-")[0]
        else:
            dest_lang = source_lang
            source_lang = None

        exclude_list = UNICODE_EMOJI.keys()
        for emoji in exclude_list:
            if emoji in text:
                text = text.replace(emoji, "")

        trl = google_translator()
        if source_lang is None:
            detection = trl.detect(text)
            trans_str = trl.translate(text, lang_tgt=dest_lang)
            return message.reply_text(
                f"*Diterjemahkan dari bahasa* `{detection[0]}` *ke bahasa*  `{dest_lang}`:\n\n`{trans_str}`",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            trans_str = trl.translate(text, lang_tgt=dest_lang, lang_src=source_lang)
            message.reply_text(
                f"*Diterjemahkan dari bahasa* `{source_lang}` *ke bahasa* `{dest_lang}`:\n\n`{trans_str}`",
                parse_mode=ParseMode.MARKDOWN,
            )

    except IndexError:
        update.effective_message.reply_text(
            "_Balas pesan yang ingin diterjemahkan_ ​​_ke bahasa yang diinginkan._\n\n"
            "*Contoh:* `/tr en-id` _untuk menerjemahkan dari bahasa Inggris ke Indonesia._\n"
            "*Atau gunakan:* `/tr id` _otomatis menerjemahkan ke bahasa Indonesia._\n"
            "*Lihat* [disini](https://t.me/canzu/20) *daftar kode bahasa yang tersedia._",
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
    except ValueError:
        update.effective_message.reply_text("Bahasa yang dimaksud tidak ditemukan!")
    else:
        return


__help__ = """
 ❍ /tr atau /tl (kode bahasa)*:* untuk menerjemahkan teks
*Contoh:* 
 ❍ /tr id*:* menerjemahkan teks ke bahasa Indonesia
 ❍ /tr en-id*:* menerjemahkan dari bahasa Inggris ke Indonesia

*Kode Bahasa*
`af,am,ar,az,be,bg,bn,bs,ca,ceb,co,cs,cy,da,de,el,en,eo,es,
et,eu,fa,fi,fr,fy,ga,gd,gl,gu,ha,haw,hi,hmn,hr,ht,hu,hy,
id,ig,is,it,iw,ja,jw,ka,kk,km,kn,ko,ku,ky,la,lb,lo,lt,lv,mg,mi,mk,
ml,mn,mr,ms,mt,my,ne,nl,no,ny,pa,pl,ps,pt,ro,ru,sd,si,sk,sl,
sm,sn,so,sq,sr,st,su,sv,sw,ta,te,tg,th,tl,tr,uk,ur,uz,
vi,xh,yi,yo,zh,zh_CN,zh_TW,zu`
"""

TRANSLATE_HANDLER = DisableAbleCommandHandler(["tr", "tl"], totranslate)

dispatcher.add_handler(TRANSLATE_HANDLER)

__mod_name__ = "Kamus"
__command_list__ = ["tr", "tl"]
__handlers__ = [TRANSLATE_HANDLER]
